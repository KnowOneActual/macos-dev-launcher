#!/bin/bash

set -e

# Variables
INSTALL_DIR="$HOME/scripts"
SCRIPT_NAME="opendevenv.py"
CONFIG_DIR="$HOME/.config/macos-dev-launcher"
CONFIG_FILE="$CONFIG_DIR/config.json"
WORKFLOW_DIR="$HOME/Library/Services/Open Dev Environment.workflow"

BACKUP_SUFFIX=$(date +%Y%m%d%H%M%S)

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

usage() {
  echo "macOS Dev Environment Launcher - Installation Script"
  echo ""
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -d, --dir DIR       Installation directory (default: $INSTALL_DIR)"
  echo "  -s, --silent        Silent mode (no prompts, use defaults)"
  echo "  -f, --force         Force overwrite existing files"
  echo "  -u, --uninstall     Uninstall the launcher"
  echo "  --no-workflow       Skip Quick Action creation"
  echo "  -h, --help          Show this help message"
  echo ""
  echo "Examples:"
  echo "  $0                   Interactive installation"
  echo "  $0 --silent          Silent installation with defaults"
  echo "  $0 --dir bin         Install to custom directory"
  echo "  $0 --uninstall       Remove the launcher"
}

backup_workflow() {
  if [ -d "$WORKFLOW_DIR" ]; then
    BACKUP_DIR="${WORKFLOW_DIR}.backup-$BACKUP_SUFFIX"
    echo -e "${YELLOW}Backing up existing Quick Action to $BACKUP_DIR${NC}"
    mv "$WORKFLOW_DIR" "$BACKUP_DIR"
  fi
}

verify_workflow() {
  if [ -d "$WORKFLOW_DIR" ] && [ -f "$WORKFLOW_DIR/Contents/document.wflow" ]; then
    return 0
  else
    return 1
  fi
}

restore_backup() {
  BACKUP_DIR=$(ls -td ${WORKFLOW_DIR}.backup-* 2>/dev/null | head -n 1 || true)
  if [ -n "$BACKUP_DIR" ]; then
    echo -e "${YELLOW}Restoring backup Quick Action from $BACKUP_DIR${NC}"
    rm -rf "$WORKFLOW_DIR"
    mv "$BACKUP_DIR" "$WORKFLOW_DIR"
  fi
}

install_script() {
  echo -e "${GREEN}Installing Python script...${NC}"
  cp "scripts/$SCRIPT_NAME" "$INSTALL_DIR/"
  chmod +x "$INSTALL_DIR/$SCRIPT_NAME"
  echo -e "${GREEN}Script installed to $INSTALL_DIR/$SCRIPT_NAME${NC}"
}

install_config() {
  echo -e "${GREEN}Creating configuration file...${NC}"
  mkdir -p "$CONFIG_DIR"
  if [ ! -f "$CONFIG_FILE" ]; then
    cp "config.example.json" "$CONFIG_FILE"
    echo -e "${GREEN}Config file created at $CONFIG_FILE${NC}"
  else
    echo -e "${YELLOW}Config file already exists at $CONFIG_FILE, skipping creation.${NC}"
  fi
}

install_workflow() {
  backup_workflow

  echo -e "${GREEN}Creating Automator Quick Action...${NC}"

  # Remove old workflow directory if exists (after backup)
  rm -rf "$WORKFLOW_DIR"

  # Copy workflow directory from scripts or a prepared directory
  cp -R "scripts/Open Dev Environment.workflow" "$WORKFLOW_DIR" || true

  if verify_workflow; then
    echo -e "${GREEN}Quick Action created successfully.${NC}"
  else
    echo -e "${RED}Failed to create Quick Action!${NC}"
    restore_backup
    echo -e "${RED}Previous Quick Action restored.${NC}"
    echo -e "${RED}Please see manual setup instructions at https://github.com/KnowOneActual/macos-dev-launcher#manual-installation${NC}"
    exit 1
  fi
}

uninstall() {
  echo -e "${YELLOW}Uninstalling macOS Dev Environment Launcher...${NC}"
  rm -f "$INSTALL_DIR/$SCRIPT_NAME"
  rm -rf "$CONFIG_DIR"
  if [ -d "$WORKFLOW_DIR" ]; then
    echo -e "${YELLOW}Removing Quick Action...${NC}"
    rm -rf "$WORKFLOW_DIR"
  fi
  echo -e "${GREEN}Uninstallation complete.${NC}"
  exit 0
}

# Parse arguments
FORCE=0
SILENT=0
UNINSTALL=0
NO_WORKFLOW=0
CUSTOM_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -d|--dir)
      CUSTOM_DIR="$2"
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
    --no-workflow)
      NO_WORKFLOW=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option $1${NC}"
      usage
      exit 1
      ;;
  esac
done

if [ $UNINSTALL -eq 1 ]; then
  uninstall
fi

if [ -n "$CUSTOM_DIR" ]; then
  INSTALL_DIR="$CUSTOM_DIR"
fi

mkdir -p "$INSTALL_DIR"

if [ $SILENT -eq 0 ]; then
  echo "Installing macOS Dev Environment Launcher to ${INSTALL_DIR}"
  if [ $NO_WORKFLOW -eq 1 ]; then
    echo "Skipping Quick Action creation."
  fi
  if [ $FORCE -eq 0 ]; then
    read -p "Proceed? [Y/n]: " confirm
    if [[ "$confirm" =~ ^(n|N)$ ]]; then
      echo "Aborted."
      exit 0
    fi
  fi
fi

install_script
install_config

if [ $NO_WORKFLOW -eq 0 ]; then
  install_workflow
else
  echo -e "${YELLOW}Skipping Quick Action creation as requested.${NC}"
fi

echo -e "${GREEN}Verifying installation...${NC}"
python3 "$INSTALL_DIR/$SCRIPT_NAME" --test || echo -e "${YELLOW}Warning: Test script reported issues.${NC}"

echo -e "${GREEN}Installation complete!${NC}"
echo "Next steps:"
echo " 1. Restart Finder by running: killall Finder"
echo " 2. Use the Quick Action 'Open Dev Environment' by right-clicking folders in Finder"
echo " 3. Modify config at $CONFIG_FILE as needed"
