set -euo pipefail
rm -rf dist
"$1" --project tsconfig.json --pretty false --typeRoots "$2/node_modules/@types"
node dist/src/benchmark.js > benchmark_result.json
cat benchmark_result.json
