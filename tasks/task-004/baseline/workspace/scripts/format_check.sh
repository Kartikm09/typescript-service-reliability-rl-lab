set -euo pipefail
if grep -R -n $'\t' src tests --include='*.ts'; then echo "TypeScript task sources contain tabs" >&2; exit 1; fi
