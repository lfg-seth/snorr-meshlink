# Local development

Use Linux, macOS or WSL with Python 3.14.3 and Node 22.23.1 (`.nvmrc`). Run commands from the repository root.

## Start

```sh
python3 backend/launch.py
```

Starts the demo PocketBase, simulation worker and frontend. Stop with **Ctrl+C**; saved demo data remains. Ports 5173 and 8092 must be free.

- **Portal:** http://127.0.0.1:5173
- **Database dashboard:** http://127.0.0.1:8092/_/

## First-time setup

Run once before starting:

```sh
python3 backend/manage.py install
python3 backend/demo_database.py init
npm --prefix portal ci
```

Skip `init` if the demo is already initialized. It refuses to overwrite existing data. Run `npm --prefix portal ci` again when dependencies change.

## Demo credentials

All these accounts use password **`fictional-demo-only-password`**:

| Where | Username / email |
| --- | --- |
| Portal admin | `meshlink-admin` |
| Portal member | `meshlink-member` |
| Portal second member | `meshlink-member2` |
| PocketBase dashboard | `demo-admin@example.invalid` |

The portal opens as demo admin automatically. To review member access, exit the demo and sign in with a member account. These credentials are public and only for the local demo.

## Build and check

```sh
# Build the frontend into portal/dist/
npm --prefix portal run build

# Run frontend tests, type checking and build
npm --prefix portal run check
```

## Demo data

The frontend reads the writable database at `local-data/demo/pb_data/data.db`. Edit sample records in the PocketBase dashboard; the frontend polls every two seconds.

The original synthetic checkpoint is tracked at `backend/demo/data.db`. Local edits persist without changing that checkpoint. Production stays on the VM.

More detail: [demo database guide](backend/demo/README.md).
