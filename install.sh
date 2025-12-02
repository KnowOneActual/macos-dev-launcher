#!/bin/bash

# install.sh - Automated Installer for macOS Dev Environment Launcher

# Set default installation directory
DEFAULT_DIR="$HOME/scripts"
INSTALL_DIR=""
FORCE=0
SILENT=0
UNINSTALL=0

# Function to print usage
usage() {
  cat <<EOF
Usage: $0 [OPTIONS]

Options:
  -d, --dir DIR       Installation directory (default: $DEFAULT_DIR)
  -s, --silent        Silent mode (no prompts, use defaults)
  -f, --force         Force installation (overwrite existing files)
  -u, --uninstall     Uninstall the launcher
  -h, --help          Show this help message
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--dir)
      INSTALL_DIR="$2"
      shift 2
      ;;
    -s|--silent)
      SILENT=1
      shift
      ;;
    -f|--force)
      FORCE=1
      shift
      ;;
    -u|--uninstall)
      UNINSTALL=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

# Set installation directory
if [ -z "$INSTALL_DIR" ]; then
  INSTALL_DIR="$DEFAULT_DIR"
fi

# Function to create install directory
create_dir() {
  if [ -d "$1" ]; then
    if [ "$FORCE" -eq 1 ]; then
      echo "Overwriting existing directory: $1"
    else
      echo "Directory already exists: $1"
      if [ "$SILENT" -eq 1 ]; then
        echo "Use --force to overwrite."
        exit 1
      else
        read -p "Overwrite? [y/N]: " resp
        if [[ ! "$resp" =~ ^[Yy]$ ]]; then
          echo "Installation canceled."
          exit 1
        fi
      fi
    fi
  fi
  mkdir -p "$1"
  echo "Created: $1"
}

# Function to uninstall
uninstall() {
  echo "Uninstalling..."
  rm -f "$HOME/scripts/open_dev_env.py"
  # Remove launcher script if exists
  if [ -f "$HOME/scripts/install.sh" ]; then
    echo "Removing installer script."
    # Keep installer as it's part of repo
  fi
  # Remove Automator Quick Action manually:
  rm -f ~/Library/Services/"Open Dev Environment.workflow"
  echo "Removed Quick Action and scripts."
  echo "Uninstall complete."
  exit 0
}

# Main installation
if [ "$UNINSTALL" -eq 1 ]; then
  uninstall
fi

# Check existing installation
if [ -f "$INSTALL_DIR/open_dev_env.py" ] && [ "$FORCE" -ne 1 ]; then
  echo "Script already installed at $INSTALL_DIR/open_dev_env.py"
  if [ "$SILENT" -eq 1 ]; then
    echo "Use --force to reinstall."
    exit 0
  else
    read -p "Overwrite existing installation? [y/N]: " resp
    if [[ ! "$resp" =~ ^[Yy]$ ]]; then
      echo "Installation canceled."
      exit 0
    fi
  fi
fi

# Create install dir
create_dir "$INSTALL_DIR"

# Copy script
SCRIPT_SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/open_dev_env.py"
if [ ! -f "$SCRIPT_SRC" ]; then
  echo "Error: open_dev_env.py not found in script directory."
  exit 1
fi
cp "$SCRIPT_SRC" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/open_dev_env.py"
echo "Copied open_dev_env.py to $INSTALL_DIR"

# Create config directory and file if not exists
CONFIG_DIR="$HOME/.config/macos-dev-launcher"
mkdir -p "$CONFIG_DIR"

CONFIG_FILE="$CONFIG_DIR/config.json"
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Creating default config..."
  cat > "$CONFIG_FILE" <<EOF
{
  "terminals": ["Ghostty", "Kitty", "Warp", "Wave"],
  "editors": ["VSCodium"],
  "app_args": {},
  "logging": {
    "logfile": "$HOME/Library/Logs/macos-dev-launcher.log",
    "level": "INFO",
    "max_size_kb": 1024,
    "backup_count": 7
  },
  "behavior": {
    "auto_open_editor": true,
    "remember_choices": true
  }
}
EOF
else
  echo "Config already exists at $CONFIG_FILE"
fi

# Create manual instructions for Quick Action
cat > "$CONFIG_DIR/QUICK_ACTION_INSTRUCTIONS.md" <<EOF
# Manual Setup of Quick Action

macOS Automator workflows cannot be reliably created programmatically. To set up the Quick Action manually:

1. Open **Automator** app
2. Select **File > New** and choose **Quick Action**
3. Set "Workflow receives current" to **files or folders** in **Finder**
4. Add **"Run Shell Script"** action
5. Set **"Pass input"** to **as arguments**
6. Paste the following command:
```bash
/usr/bin/python3 "$HOME/scripts/open_dev_env.py" "$@"
