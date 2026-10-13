"""Owner-run account administration; passwords are entered without echo."""
import argparse
import getpass
from client import Client
from manage import credentials

parser = argparse.ArgumentParser()
parser.add_argument('action', choices=['create', 'reset-password', 'disable'])
parser.add_argument('--id', help='PocketBase account record ID for reset/disable')
args = parser.parse_args()
secret = credentials()['admin']
client = Client()
client.login(secret['username'], secret['password'])
if args.action == 'create':
    username = input('Username: ').strip()
    name = input('Display name: ').strip()
    role = input('Role (admin/member): ').strip()
    member_id = input('Member key (required for member role): ').strip()
    password = getpass.getpass('Initial password (12+ characters): ')
    result = client.request('POST', '/api/meshlink/accounts', {'username': username, 'name': name, 'role': role, 'memberId': member_id, 'password': password})
    print('Created account ID:', result['id'])
else:
    if not args.id:
        parser.error('--id is required')
    body = {'action': args.action}
    if args.action == 'reset-password':
        body['password'] = getpass.getpass('New password (12+ characters): ')
    client.request('POST', f'/api/meshlink/accounts/{args.id}', body)
    print('Account action saved. Earlier assignments/messages remain recorded.')
