"""Verify the immutable private cache. Restore absent entries only on explicit request."""
import argparse
from pathlib import Path
import hashlib
import json
from urllib.request import urlopen
import shutil

def verify_sources(root,restore=False):
    records=json.loads((root/'inputs/sources.json').read_bytes())
    for record in records['files']:
        p=root/'source'/record['file']
        if not p.is_file() and restore:
            if not record.get('url'):
                raise ValueError(f"Restore the preserved local source {p.name} from backup.")
            tmp=p.with_suffix(p.suffix+'.part')
            with urlopen(record['url'],timeout=180) as response,tmp.open('wb') as out:
                shutil.copyfileobj(response,out)
            with tmp.open('rb') as f:
                if hashlib.file_digest(f,'sha256').hexdigest()!=record['sha256']:
                    raise ValueError(f"Provider returned a different version of {p.name}. See the pinned manifest.")
            tmp.replace(p)
        with p.open('rb') as f:
            if hashlib.file_digest(f,'sha256').hexdigest()!=record['sha256']:raise ValueError(f'Cache mismatch: {p.name}')

if __name__=='__main__':
    args=argparse.ArgumentParser()
    args.add_argument('directory',type=Path);args.add_argument('--restore',action='store_true')
    opts=args.parse_args();verify_sources(opts.directory,opts.restore)
