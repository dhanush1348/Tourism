#!/usr/bin/env bash
set -Eeuo pipefail

# One-command deploy helper for PythonAnywhere.
# Default behavior: install deps, run migrations, collect static files.

PROJECT_DIR="${PROJECT_DIR:-$HOME/tours_project}"
VENV_NAME="${VENV_NAME:-toursenv}"
PYTHON_BIN="${PYTHON_BIN:-/usr/bin/python3.10}"
BOOTSTRAP_VENV="false"
SKIP_COLLECTSTATIC="false"
SKIP_MIGRATE="false"
SKIP_INSTALL="false"

usage() {
  cat <<'EOF'
Usage: ./scripts/pythonanywhere_deploy.sh [options]

Options:
  --bootstrap-venv        Create virtualenv if missing (mkvirtualenv required)
  --project-dir PATH      Project directory (default: ~/tours_project)
  --venv-name NAME        Virtualenv name (default: toursenv)
  --python-bin PATH       Python binary for virtualenv creation (default: /usr/bin/python3.10)
  --skip-install          Skip pip install -r requirements.txt
  --skip-migrate          Skip python manage.py migrate
  --skip-collectstatic    Skip python manage.py collectstatic --noinput
  -h, --help              Show this help

Examples:
  ./scripts/pythonanywhere_deploy.sh
  ./scripts/pythonanywhere_deploy.sh --bootstrap-venv
  ./scripts/pythonanywhere_deploy.sh --project-dir /home/dhanush1348/tours_project --venv-name toursenv
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bootstrap-venv)
      BOOTSTRAP_VENV="true"
      shift
      ;;
    --project-dir)
      PROJECT_DIR="$2"
      shift 2
      ;;
    --venv-name)
      VENV_NAME="$2"
      shift 2
      ;;
    --python-bin)
      PYTHON_BIN="$2"
      shift 2
      ;;
    --skip-install)
      SKIP_INSTALL="true"
      shift
      ;;
    --skip-migrate)
      SKIP_MIGRATE="true"
      shift
      ;;
    --skip-collectstatic)
      SKIP_COLLECTSTATIC="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Project directory not found: $PROJECT_DIR" >&2
  exit 1
fi

if ! command -v workon >/dev/null 2>&1; then
  # shellcheck disable=SC1091
  if [[ -f "$HOME/.virtualenvs/$VENV_NAME/bin/activate" ]]; then
    # Fallback when workon is unavailable.
    # shellcheck disable=SC1091
    source "$HOME/.virtualenvs/$VENV_NAME/bin/activate"
  else
    echo "virtualenvwrapper not initialized and no venv found at ~/.virtualenvs/$VENV_NAME" >&2
    echo "Open a PythonAnywhere Bash console and run: source ~/.virtualenvs/$VENV_NAME/bin/activate" >&2
    exit 1
  fi
else
  if [[ "$BOOTSTRAP_VENV" == "true" ]] && [[ ! -d "$HOME/.virtualenvs/$VENV_NAME" ]]; then
    mkvirtualenv --python="$PYTHON_BIN" "$VENV_NAME"
  fi
  workon "$VENV_NAME"
fi

cd "$PROJECT_DIR"

echo "Using project: $PROJECT_DIR"
echo "Using virtualenv: $VENV_NAME"
python --version

if [[ ! -f "requirements.txt" ]]; then
  echo "requirements.txt not found in $PROJECT_DIR" >&2
  exit 1
fi

if [[ "$SKIP_INSTALL" == "false" ]]; then
  echo "Installing dependencies..."
  pip install --upgrade pip setuptools wheel
  pip install -r requirements.txt
fi

if [[ "$SKIP_MIGRATE" == "false" ]]; then
  echo "Running migrations..."
  python manage.py migrate
fi

if [[ "$SKIP_COLLECTSTATIC" == "false" ]]; then
  echo "Collecting static files..."
  python manage.py collectstatic --noinput
fi

echo "Done. Next: reload your web app from the PythonAnywhere Web tab."
