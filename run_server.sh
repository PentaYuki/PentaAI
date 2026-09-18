
#!/bin/bash
set -e

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec python3 "$ROOT_DIR/pentami-core/backend/main.py"
