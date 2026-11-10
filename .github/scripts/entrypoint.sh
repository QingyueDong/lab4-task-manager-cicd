#!/usr/bin/env bash
# =============================================================================
# entrypoint.sh  (Lab 4 / Lecture 4 - Activity 6)
#
# Main script of the Docker image (ENTRYPOINT). It
#   1. runs todo.py       and saves its output   (tee = show in log AND save to file)
#   2. runs todo-test.py  and saves its output
#   3. runs update_index.sh to write both outputs into index.html
#   4. exits with an error code if the tests failed, so the CI job turns red
#
# Scripts live in the image (/app/.github/scripts). index.html lives in the
# repository, which ci.yml mounts at /workspace (the container's working dir).
# Output .txt files go to /tmp, so they are never committed by accident.
# =============================================================================
set -uo pipefail    # no `-e`: we still want index.html updated when tests fail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT_DIR="${OUT_DIR:-/tmp/task-manager}"
mkdir -p "$OUT_DIR"

banner() {
  echo "====================="
  echo "$1"
  echo "====================="
}

banner "Executing todo.py"
python3 "$SCRIPT_DIR/todo.py" | tee "$OUT_DIR/todo_output.txt"
TODO_STATUS=${PIPESTATUS[0]}          # exit code of python3, not of tee

banner "Executing todo-test.py"
python3 "$SCRIPT_DIR/todo-test.py" 2>&1 | tee "$OUT_DIR/test_output.txt"
TEST_STATUS=${PIPESTATUS[0]}

banner "Executing update_index.sh"
bash "$SCRIPT_DIR/update_index.sh" "$OUT_DIR/todo_output.txt" "$OUT_DIR/test_output.txt"
INDEX_STATUS=$?

if [ "$TODO_STATUS" -ne 0 ] || [ "$TEST_STATUS" -ne 0 ] || [ "$INDEX_STATUS" -ne 0 ]; then
  banner "FAILED (todo.py=$TODO_STATUS, tests=$TEST_STATUS, update_index=$INDEX_STATUS)"
  exit 1
fi

banner "Done!"
