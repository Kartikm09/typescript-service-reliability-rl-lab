set -euo pipefail
rm -rf dist
"$1" --project tsconfig.json --pretty false --typeRoots "$3/node_modules/@types"
node --test "dist/tests/$2.test.js"
