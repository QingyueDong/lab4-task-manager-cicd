#!/usr/bin/env bash
# =============================================================================
# update_index.sh  (Lab 4 / Lecture 4 - Activity 5)
#
# Rewrites the <pre id="..."> blocks in index.html with the latest data:
#   <pre id="pending">    <- "ToDo Tasks:" section of todo.py output
#   <pre id="completed">  <- "Done Tasks:" section of todo.py output
#   <pre id="unittest">   <- the whole output of todo-test.py
#   <pre id="buildinfo">  <- who / when / which commit (new, not in the slides)
#
# Usage:  update_index.sh <todo_output.txt> <test_output.txt> [index.html]
#
# Changes vs. the slides (see CHANGES_vs_course_materials.md):
#   * No git config/add/commit/push here: the container has no credentials and
#     should not get any. The workflow commits on the runner instead.
#   * Content is passed to perl through environment variables and HTML-escaped,
#     so characters such as $, @, <, > or & in task titles / test output can no
#     longer break the replacement or the page.
#   * Fails loudly if index.html is missing (e.g. you forgot to mount the repo).
# =============================================================================
set -euo pipefail

TODO_OUTPUT="${1:?usage: update_index.sh <todo_output.txt> <test_output.txt> [index.html]}"
TEST_OUTPUT="${2:?usage: update_index.sh <todo_output.txt> <test_output.txt> [index.html]}"
HTML_FILE="${3:-${HTML_FILE:-index.html}}"

if [ ! -f "$HTML_FILE" ]; then
  echo "Error: $HTML_FILE not found in $(pwd)." >&2
  echo "In Docker, mount the repository and work there, e.g.:" >&2
  echo "  docker run --rm -v \"\$PWD:/workspace\" -w /workspace task-manager:latest" >&2
  exit 1
fi

# --- Extract tasks and test data and store them in local variables ----------
# Lines after "ToDo Tasks:" up to "Done Tasks:", skipping blank lines.
TODO_TASKS="$(awk '/^ToDo Tasks:/{f=1; next} /^Done Tasks:/{f=0} f && NF' "$TODO_OUTPUT")"
# Lines after "Done Tasks:" to the end, skipping blank lines.
DONE_TASKS="$(awk '/^Done Tasks:/{f=1; next} f && NF' "$TODO_OUTPUT")"
UNIT_TEST_RESULTS="$(cat "$TEST_OUTPUT")"

SHORT_SHA="${GITHUB_SHA:-local}"
SHORT_SHA="${SHORT_SHA:0:7}"
BUILD_INFO="Last updated by ${GITHUB_USER:-${GITHUB_ACTOR:-local-user}} on $(date '+%Y-%m-%d %H:%M:%S %Z') [Commit: ${SHORT_SHA}]"

# --- Function to update one <pre id="..."> ... </pre> block ------------------
update_pre() {
  local id="$1" content="$2" file="$3"
  if ! grep -q "<pre id=\"${id}\">" "$file"; then
    echo "Warning: <pre id=\"${id}\"> not found in ${file} - skipped" >&2
    return 0
  fi
  # -0777 reads the whole file at once so the match can span several lines.
  # The new content comes from $ENV{PRE_CONTENT}, so the shell never pastes raw
  # text into the perl program.
  PRE_ID="$id" PRE_CONTENT="$content" perl -0777 -i -pe '
    my $c = $ENV{PRE_CONTENT};
    $c =~ s/&/&amp;/g; $c =~ s/</&lt;/g; $c =~ s/>/&gt;/g;     # HTML-escape
    s{(<pre id="\Q$ENV{PRE_ID}\E">).*?(</pre>)}{$1\n$c\n$2}s;
  ' "$file"
}

update_pre "pending"   "$TODO_TASKS"         "$HTML_FILE"
update_pre "completed" "$DONE_TASKS"         "$HTML_FILE"
update_pre "unittest"  "$UNIT_TEST_RESULTS"  "$HTML_FILE"
update_pre "buildinfo" "$BUILD_INFO"         "$HTML_FILE"

echo "Updated ${HTML_FILE}: $(printf '%s\n' "$TODO_TASKS" | grep -c .) ToDo, $(printf '%s\n' "$DONE_TASKS" | grep -c .) Done task(s)."
