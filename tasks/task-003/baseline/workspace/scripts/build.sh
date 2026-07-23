set -euo pipefail
rm -rf dist
"$1" --project tsconfig.json --pretty false --typeRoots "$2/node_modules/@types"
