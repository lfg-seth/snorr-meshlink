#!/usr/bin/env bash
set -euo pipefail

if [[ $# != 1 || ! $1 =~ ^[a-zA-Z0-9][a-zA-Z0-9_-]*$ ]]; then
    echo "Usage: $0 <PlatformIO environment>" >&2
    exit 2
fi
host=$(git config --get meshlink.buildHost) || {
    echo "Set meshlink.buildHost in this checkout's Git configuration." >&2
    exit 1
}
pin=$(git rev-parse HEAD:firmware)
[[ $pin =~ ^[0-9a-f]{40}$ ]]
ssh -o BatchMode=yes -o ForwardAgent=no -- "$host" \
    "runuser -u snorr-build -- flock /srv/snorr-build/build.lock bash -se -- $pin $1" <<'REMOTE'
set -o pipefail
cd /srv/snorr-build/firmware
export PATH="/srv/snorr-build/venv/bin:$PATH"
changes=$(git status --porcelain --untracked-files=normal)
if [[ -n $changes ]]; then
    echo "Remote firmware checkout has changes. Inspect before building." >&2
    exit 1
fi
git cat-file -e "$1^{commit}" 2>/dev/null || git fetch origin "$1"
git checkout --detach "$1"
git submodule update --init --recursive
mkdir -p "/srv/snorr-build/results/$1/$2"
result=$(mktemp -d "/srv/snorr-build/results/$1/$2/run.XXXXXXXX")
echo "Build results: $result"
pio run -e "$2" 2>&1 | tee "$result/build.log"
out=".pio/build/$2"
version=$(python bin/buildinfo.py long)
stem="$out/firmware-$2-$version"
artifacts=()
for path in "$stem".{bin,factory.bin,hex,uf2,zip}; do
    if [[ -s $path ]]; then
        artifacts+=("$path")
    fi
done
if (( ${#artifacts[@]} == 0 )); then
    echo "Build produced no packaged firmware images in $out" >&2
    exit 1
fi
for path in "$stem.mt.json" "$out/littlefs-$2-$version.bin"; do
    if [[ -s $path ]]; then
        artifacts+=("$path")
    fi
done
cp -- "${artifacts[@]}" "$result/"
cd "$result"
sha256sum -- "${artifacts[@]##*/}" > SHA256SUMS
sha256sum --check SHA256SUMS
echo "Verified build outputs: $result"
REMOTE
