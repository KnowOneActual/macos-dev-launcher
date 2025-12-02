#!/bin/bash

# macOS Dev Environment Launcher - Installation Script
# Phase 3.2: Automated setup for new users
# Usage: ./install.sh [OPTIONS]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
DEFAULT_INSTALL_DIR="$HOME/scripts"
SCRIPT_NAME="open_dev_env.py"
QUICK_ACTION_NAME="Open Dev Environment"
CONFIG_DIR="$HOME/.config/macos-dev-launcher"
CONFIG_FILE="$CONFIG_DIR/config.json"

# Command line flags
INSTALL_DIR="$DEFAULT_INSTALL_DIR"
SILENT_MODE=false
UNINSTALL=false
FORCE=false

# Print functions
print_header() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}======================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Show usage
show_usage() {
    cat << EOF
macOS Dev Environment Launcher - Installation Script

Usage: ./install.sh [OPTIONS]

Options:
    -d, --dir DIR       Installation directory (default: ~/scripts)
    -s, --silent        Silent mode (no prompts, use defaults)
    -f, --force         Force installation (overwrite existing files)
    -u, --uninstall     Uninstall the launcher
    -h, --help          Show this help message

Examples:
    ./install.sh                    # Interactive installation
    ./install.sh --silent           # Silent installation with defaults
    ./install.sh --dir ~/bin        # Install to custom directory
    ./install.sh --uninstall        # Remove the launcher

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--dir)
            INSTALL_DIR="$2"
            shift 2
            ;;
        -s|--silent)
            SILENT_MODE=true
            shift
            ;;
        -f|--force)
            FORCE=true
            shift
            ;;
        -u|--uninstall)
            UNINSTALL=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Uninstall function
uninstall() {
    print_header "Uninstalling macOS Dev Environment Launcher"
    
    local removed_count=0
    
    # Remove script
    if [ -f "$INSTALL_DIR/$SCRIPT_NAME" ]; then
        rm "$INSTALL_DIR/$SCRIPT_NAME"
        print_success "Removed script: $INSTALL_DIR/$SCRIPT_NAME"
        ((removed_count++))
    fi
    
    # Remove config directory (ask first unless silent)
    if [ -d "$CONFIG_DIR" ]; then
        if [ "$SILENT_MODE" = true ] || [ "$FORCE" = true ]; then
            rm -rf "$CONFIG_DIR"
            print_success "Removed config directory: $CONFIG_DIR"
            ((removed_count++))
        else
            read -p "Remove config directory (includes history)? [y/N]: " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                rm -rf "$CONFIG_DIR"
                print_success "Removed config directory: $CONFIG_DIR"
                ((removed_count++))
            else
                print_info "Kept config directory: $CONFIG_DIR"
            fi
        fi
    fi
    
    # Remove Automator Quick Action
    local automator_dir="$HOME/Library/Services"
    local quick_action="$automator_dir/$QUICK_ACTION_NAME.workflow"
    
    if [ -d "$quick_action" ]; then
        rm -rf "$quick_action"
        print_success "Removed Quick Action: $quick_action"
        ((removed_count++))
    fi
    
    if [ $removed_count -eq 0 ]; then
        print_warning "Nothing to uninstall (not found)"
    else
        echo
        print_success "Uninstall complete! Removed $removed_count item(s)"
        print_info "You may need to restart Finder: killall Finder"
    fi
    
    exit 0
}

# Check if uninstall requested
if [ "$UNINSTALL" = true ]; then
    uninstall
fi

# Main installation
print_header "macOS Dev Environment Launcher - Installation"

echo
print_info "This script will install the Dev Environment Launcher:"
echo "  • Python script: $INSTALL_DIR/$SCRIPT_NAME"
echo "  • Automator Quick Action"
echo "  • Configuration file: $CONFIG_FILE"
echo

# Check if already installed
if [ -f "$INSTALL_DIR/$SCRIPT_NAME" ] && [ "$FORCE" = false ]; then
    print_warning "Script already exists at: $INSTALL_DIR/$SCRIPT_NAME"
    
    if [ "$SILENT_MODE" = false ]; then
        read -p "Overwrite existing installation? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled"
            exit 0
        fi
    else
        print_error "Use --force to overwrite existing installation"
        exit 1
    fi
fi

# Prompt for installation directory
if [ "$SILENT_MODE" = false ] && [ "$INSTALL_DIR" = "$DEFAULT_INSTALL_DIR" ]; then
    read -p "Installation directory [$DEFAULT_INSTALL_DIR]: " user_dir
    if [ -n "$user_dir" ]; then
        INSTALL_DIR="$user_dir"
    fi
fi

# Expand tilde
INSTALL_DIR="${INSTALL_DIR/#\~/$HOME}"

echo
print_header "Installing..."

# Step 1: Create installation directory
print_info "Creating installation directory..."
if mkdir -p "$INSTALL_DIR"; then
    print_success "Created: $INSTALL_DIR"
else
    print_error "Failed to create directory: $INSTALL_DIR"
    exit 1
fi

# Step 2: Copy/download script
print_info "Installing Python script..."

# Check if we're in the repo (script exists in current directory)
if [ -f "$SCRIPT_NAME" ]; then
    # We're in the repo, copy the file
    if cp "$SCRIPT_NAME" "$INSTALL_DIR/$SCRIPT_NAME"; then
        print_success "Copied script to: $INSTALL_DIR/$SCRIPT_NAME"
    else
        print_error "Failed to copy script"
        exit 1
    fi
else
    # Not in repo, try to download from GitHub
    print_info "Downloading from GitHub..."
    local github_url="https://raw.githubusercontent.com/KnowOneActual/macos-dev-launcher/main/open_dev_env.py"
    
    if command -v curl &> /dev/null; then
        if curl -fsSL "$github_url" -o "$INSTALL_DIR/$SCRIPT_NAME"; then
            print_success "Downloaded script to: $INSTALL_DIR/$SCRIPT_NAME"
        else
            print_error "Failed to download script from GitHub"
            print_info "Please clone the repository and run install.sh from there"
            exit 1
        fi
    else
        print_error "curl not found. Please install curl or clone the repository"
        exit 1
    fi
fi

# Step 3: Make script executable
print_info "Making script executable..."
if chmod +x "$INSTALL_DIR/$SCRIPT_NAME"; then
    print_success "Script is now executable"
else
    print_error "Failed to make script executable"
    exit 1
fi

# Step 4: Create config file
print_info "Creating configuration file..."
if "$INSTALL_DIR/$SCRIPT_NAME" --create-config &> /dev/null; then
    print_success "Created config: $CONFIG_FILE"
else
    print_warning "Config file creation failed (may already exist)"
fi

# Step 5: Create Automator Quick Action
print_info "Creating Automator Quick Action..."

local automator_dir="$HOME/Library/Services"
local quick_action="$automator_dir/$QUICK_ACTION_NAME.workflow"

# Create Services directory if it doesn't exist
mkdir -p "$automator_dir"

# Create the workflow
mkdir -p "$quick_action/Contents"

# Create Info.plist
cat > "$quick_action/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>NSServices</key>
	<array>
		<dict>
			<key>NSMenuItem</key>
			<dict>
				<key>default</key>
				<string>$QUICK_ACTION_NAME</string>
			</dict>
			<key>NSMessage</key>
			<string>runWorkflowAsService</string>
			<key>NSRequiredContext</key>
			<dict>
				<key>NSApplicationIdentifier</key>
				<string>com.apple.finder</string>
			</dict>
			<key>NSSendFileTypes</key>
			<array>
				<string>public.folder</string>
			</array>
		</dict>
	</array>
</dict>
</plist>
EOF

# Create document.wflow
cat > "$quick_action/Contents/document.wflow" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>AMApplicationBuild</key>
	<string>523</string>
	<key>AMApplicationVersion</key>
	<string>2.10</string>
	<key>AMDocumentVersion</key>
	<string>2</string>
	<key>actions</key>
	<array>
		<dict>
			<key>action</key>
			<dict>
				<key>AMAccepts</key>
				<dict>
					<key>Container</key>
					<string>List</string>
					<key>Optional</key>
					<true/>
					<key>Types</key>
					<array>
						<string>com.apple.cocoa.string</string>
					</array>
				</dict>
				<key>AMActionVersion</key>
				<string>2.0.3</string>
				<key>AMApplication</key>
				<array>
					<string>Automator</string>
				</array>
				<key>AMParameterProperties</key>
				<dict>
					<key>COMMAND_STRING</key>
					<dict/>
					<key>inputMethod</key>
					<dict/>
					<key>shell</key>
					<dict/>
					<key>source</key>
					<dict/>
				</dict>
				<key>AMProvides</key>
				<dict>
					<key>Container</key>
					<string>List</string>
					<key>Types</key>
					<array>
						<string>com.apple.cocoa.string</string>
					</array>
				</dict>
				<key>ActionBundlePath</key>
				<string>/System/Library/Automator/Run Shell Script.action</string>
				<key>ActionName</key>
				<string>Run Shell Script</string>
				<key>ActionParameters</key>
				<dict>
					<key>COMMAND_STRING</key>
					<string>/usr/bin/python3 "$INSTALL_DIR/$SCRIPT_NAME" "\$@"</string>
					<key>CheckedForUserDefaultShell</key>
					<true/>
					<key>inputMethod</key>
					<integer>1</integer>
					<key>shell</key>
					<string>/bin/bash</string>
					<key>source</key>
					<string></string>
				</dict>
				<key>BundleIdentifier</key>
				<string>com.apple.RunShellScript</string>
				<key>CFBundleVersion</key>
				<string>2.0.3</string>
				<key>CanShowSelectedItemsWhenRun</key>
				<false/>
				<key>CanShowWhenRun</key>
				<true/>
				<key>Category</key>
				<array>
					<string>AMCategoryUtilities</string>
				</array>
				<key>Class Name</key>
				<string>RunShellScriptAction</string>
				<key>InputUUID</key>
				<string>12345678-1234-1234-1234-123456789012</string>
				<key>Keywords</key>
				<array>
					<string>Shell</string>
					<string>Script</string>
					<string>Command</string>
					<string>Run</string>
					<string>Unix</string>
				</array>
				<key>OutputUUID</key>
				<string>87654321-4321-4321-4321-210987654321</string>
				<key>UUID</key>
				<string>ABCDEF12-ABCD-ABCD-ABCD-ABCDEF123456</string>
				<key>UnlocalizedApplications</key>
				<array>
					<string>Automator</string>
				</array>
				<key>arguments</key>
				<dict>
					<key>0</key>
					<dict>
						<key>default value</key>
						<integer>0</integer>
						<key>name</key>
						<string>inputMethod</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>0</string>
					</dict>
					<key>1</key>
					<dict>
						<key>default value</key>
						<false/>
						<key>name</key>
						<string>CheckedForUserDefaultShell</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>1</string>
					</dict>
					<key>2</key>
					<dict>
						<key>default value</key>
						<string></string>
						<key>name</key>
						<string>source</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>2</string>
					</dict>
					<key>3</key>
					<dict>
						<key>default value</key>
						<string></string>
						<key>name</key>
						<string>COMMAND_STRING</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>3</string>
					</dict>
					<key>4</key>
					<dict>
						<key>default value</key>
						<string>/bin/sh</string>
						<key>name</key>
						<string>shell</string>
						<key>required</key>
						<string>0</string>
						<key>type</key>
						<string>0</string>
						<key>uuid</key>
						<string>4</string>
					</dict>
				</dict>
				<key>isViewVisible</key>
				<integer>1</integer>
				<key>location</key>
				<string>449.000000:655.000000</string>
				<key>nibPath</key>
				<string>/System/Library/Automator/Run Shell Script.action/Contents/Resources/Base.lproj/main.nib</string>
			</dict>
			<key>isViewVisible</key>
			<integer>1</integer>
		</dict>
	</array>
	<key>connectors</key>
	<dict/>
	<key>workflowMetaData</key>
	<dict>
		<key>applicationBundleIDsByPath</key>
		<dict/>
		<key>applicationPaths</key>
		<array/>
		<key>inputTypeIdentifier</key>
		<string>com.apple.Automator.fileSystemObject.folder</string>
		<key>outputTypeIdentifier</key>
		<string>com.apple.Automator.nothing</string>
		<key>presentationMode</key>
		<integer>15</integer>
		<key>processesInput</key>
		<integer>0</integer>
		<key>serviceInputTypeIdentifier</key>
		<string>com.apple.Automator.fileSystemObject.folder</string>
		<key>serviceOutputTypeIdentifier</key>
		<string>com.apple.Automator.nothing</string>
		<key>serviceProcessesInput</key>
		<integer>0</integer>
		<key>systemImageName</key>
		<string>NSActionTemplate</string>
		<key>useAutomaticInputType</key>
		<integer>0</integer>
		<key>workflowTypeIdentifier</key>
		<string>com.apple.Automator.servicesMenu</string>
	</dict>
</dict>
</plist>
EOF

if [ -d "$quick_action" ]; then
    print_success "Created Quick Action: $QUICK_ACTION_NAME"
else
    print_error "Failed to create Quick Action"
    exit 1
fi

# Step 6: Verify installation
echo
print_header "Verifying Installation..."

print_info "Running test mode..."
if "$INSTALL_DIR/$SCRIPT_NAME" --test &> /dev/null; then
    print_success "Script test passed"
else
    print_warning "Script test had warnings (check configuration)"
fi

# Final success message
echo
print_header "Installation Complete!"
echo
print_success "Dev Environment Launcher is now installed!"
echo
print_info "Installed components:"
echo "  • Script: $INSTALL_DIR/$SCRIPT_NAME"
echo "  • Config: $CONFIG_FILE"
echo "  • Quick Action: $QUICK_ACTION_NAME"
echo
print_info "Next steps:"
echo "  1. Restart Finder to activate Quick Action:"
echo "     $ killall Finder"
echo
echo "  2. Test the installation:"
echo "     $ python3 $INSTALL_DIR/$SCRIPT_NAME --test"
echo
echo "  3. Configure your preferences:"
echo "     $ open $CONFIG_FILE"
echo
echo "  4. Use it! Right-click any folder in Finder"
echo "     → Quick Actions → $QUICK_ACTION_NAME"
echo
print_info "Documentation:"
echo "  • README: https://github.com/KnowOneActual/macos-dev-launcher"
echo "  • Config guide: https://github.com/KnowOneActual/macos-dev-launcher#configuration"
echo
print_success "Happy coding! 🚀"
echo
