#!/usr/bin/env bash
# Generate the API Reference pages from the Agnocast source code.
#
# Usage:
#   ./generate_api.sh                              # use default branch (api-reference)
#   ./generate_api.sh main                         # use main branch
#   ./generate_api.sh /path/to/local/agnocast      # use a local checkout
#
# Requirements: doxygen, python3, git

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

AGNOCAST_REPO="https://github.com/autowarefoundation/agnocast.git"
DEFAULT_BRANCH="api-reference"  # TODO: change to "main" after merge
CLONE_DIR=".agnocast_src"

# ── Resolve agnocast source path ──────────────────────────────────────────────

ARG="${1:-$DEFAULT_BRANCH}"

if [ -d "$ARG/src/agnocastlib" ]; then
  # Argument is a local directory
  AGNOCAST_SRC="$(cd "$ARG" && pwd)"
  echo "Using local source: $AGNOCAST_SRC"
else
  # Argument is a branch name — clone/fetch from GitHub
  BRANCH="$ARG"
  if [ -d "$CLONE_DIR/.git" ]; then
    echo "Fetching branch '$BRANCH' ..."
    git -C "$CLONE_DIR" fetch origin "$BRANCH" --depth 1
    git -C "$CLONE_DIR" checkout FETCH_HEAD --force
  else
    echo "Cloning branch '$BRANCH' ..."
    git clone --depth 1 --branch "$BRANCH" "$AGNOCAST_REPO" "$CLONE_DIR"
  fi
  AGNOCAST_SRC="$(cd "$CLONE_DIR" && pwd)"
  echo "Using cloned source: $AGNOCAST_SRC (branch: $BRANCH)"
fi

# ── Verify source ─────────────────────────────────────────────────────────────

HEADER_DIR="$AGNOCAST_SRC/src/agnocastlib/include/agnocast"
if [ ! -d "$HEADER_DIR" ]; then
  echo "Error: $HEADER_DIR not found. Is this a valid agnocast checkout?" >&2
  exit 1
fi

# ── Generate Doxyfile with resolved paths ─────────────────────────────────────

echo "Generating Doxyfile ..."
sed "s|../agnocast/src/agnocastlib/include/agnocast|$HEADER_DIR|g" Doxyfile > Doxyfile.generated

# ── Run Doxygen ───────────────────────────────────────────────────────────────

if ! command -v doxygen &>/dev/null; then
  echo "Error: doxygen is not installed." >&2
  exit 1
fi

echo "Running Doxygen ..."
doxygen Doxyfile.generated

# ── Generate API Reference pages ──────────────────────────────────────────────

echo "Generating API Reference markdown ..."
python3 generate_api_reference.py

# ── Clean up ──────────────────────────────────────────────────────────────────

rm -f Doxyfile.generated

echo "Done. API Reference pages are in docs/api/."
