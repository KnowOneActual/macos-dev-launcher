#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse
from pathlib import Path

# --- CONFIGURATION ---
TERMINAL_APPS = ["Ghostty", "Kitty", "Warp", "Wave"] 
EDITOR_APP = "VSCodium"

# --- HELPER FUNCTIONS ---

def app_exists(app_name):
    """
    Check if an application exists in /Applications.
    
    Args:
        app_name (str): Name of the application (without .app extension)
    
    Returns:
        bool: True if app exists, False otherwise
    """
    app_path = Path(f"/Applications/{app_name}.app")
    return app_path.exists() and app_path.is_dir()

def get_available_terminals():
    """
    Filter the configured terminal list to only include installed apps.
    
    Returns:
        list: List of installed terminal app names
    """
    available = [app for app in TERMINAL_APPS if app_exists(app)]
    return available

def show_error_dialog(title, message):
    """
    Display an error dialog to the user.
    
    Args:
        title (str): Dialog title
        message (str): Error message to display
    """
    script = f"""
    display dialog "{message}" buttons {{"OK"}} default button "OK" with title "{title}" with icon stop
    """
    try:
        subprocess.run(['osascript', '-e', script], check=True)
    except subprocess.CalledProcessError:
        # If dialog fails, at least print to stderr
        print(f"ERROR: {title} - {message}", file=sys.stderr)

def ask_terminal_choice(verbose=False):
    """
    Pops up a list of available terminals to choose from.
    Only shows terminals that are actually installed.
    
    Args:
        verbose (bool): If True, print debug information
    
    Returns:
        str: Selected terminal name, or None if cancelled/no terminals available
    """
    # Get only installed terminals
    available_terminals = get_available_terminals()
    
    if verbose:
        print(f"Configured terminals: {TERMINAL_APPS}")
        print(f"Available terminals: {available_terminals}")
    
    # Handle case where no valid terminals are found
    if not available_terminals:
        show_error_dialog(
            "No Terminals Found",
            "None of the configured terminal applications are installed. "
            f"Please install one of: {', '.join(TERMINAL_APPS)}"
        )
        return None
    
    # AppleScript list format: {"Ghostty", "Kitty", "Warp", "Wave"}
    options_str = "{" + ", ".join([f'"{app}"' for app in available_terminals]) + "}"
    
    # Default to the first available item
    script = f"""
    set appList to {options_str}
    set choice to choose from list appList with prompt "🚀 Open project in which terminal?" default items {{"{available_terminals[0]}"}}
    if choice is false then
        return "CANCEL"
    else
        return item 1 of choice
    end if
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        if verbose:
            print(f"User selected: {result}")
        return None if result == "CANCEL" else result
    except subprocess.CalledProcessError as e:
        show_error_dialog("Terminal Selection Failed", f"Could not display terminal picker: {e}")
        return None

def ask_open_editor(project_name, verbose=False):
    """
    Asks if the user wants to open the configured editor.
    Only asks if the editor is actually installed.
    
    Args:
        project_name (str): Name of the project folder
        verbose (bool): If True, print debug information
    
    Returns:
        bool: True if user wants to open editor and it exists, False otherwise
    """
    # Check if editor exists before asking
    if not app_exists(EDITOR_APP):
        if verbose:
            print(f"Editor {EDITOR_APP} not installed, skipping...")
        # Silently skip if editor not installed (don't interrupt workflow)
        return False
    
    if verbose:
        print(f"Editor {EDITOR_APP} is available")
    
    script = f"""
    display dialog "Open '{project_name}' in {EDITOR_APP} too?" buttons {{"No", "Yes"}} default button "Yes" with icon note
    return button returned of result
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        if verbose:
            print(f"User chose to open editor: {result == 'Yes'}")
        return result == "Yes"
    except subprocess.CalledProcessError:
        # If dialog fails, default to not opening editor
        return False

def open_project(path, verbose=False):
    """
    Main function to open a project in terminal and optionally editor.
    
    Args:
        path (str): Path to the project directory
        verbose (bool): If True, print debug information
    """
    project_name = os.path.basename(path)
    
    if verbose:
        print(f"\nOpening project: {project_name}")
        print(f"Path: {path}")
    
    # 1. Ask for Terminal (with validation)
    terminal_app = ask_terminal_choice(verbose)
    if not terminal_app:
        if verbose:
            print("No terminal selected or available")
        return  # User cancelled or no terminals available

    # 2. Open Terminal
    try:
        if verbose:
            print(f"Launching {terminal_app}...")
        # The 'open -a' command tells macOS to launch that specific app with this file/folder
        subprocess.run(["open", "-a", terminal_app, path], check=True)
        if verbose:
            print(f"✓ {terminal_app} launched successfully")
    except subprocess.CalledProcessError as e:
        show_error_dialog(
            "Failed to Open Terminal",
            f"Could not launch {terminal_app}. Error: {e}"
        )
        return
    
    # 3. Ask for Editor (with validation)
    if ask_open_editor(project_name, verbose):
        try:
            if verbose:
                print(f"Launching {EDITOR_APP}...")
            subprocess.run(["open", "-a", EDITOR_APP, path], check=True)
            if verbose:
                print(f"✓ {EDITOR_APP} launched successfully")
        except subprocess.CalledProcessError as e:
            show_error_dialog(
                "Failed to Open Editor",
                f"Could not launch {EDITOR_APP}. Error: {e}"
            )
            # Continue anyway - terminal already opened successfully

def test_mode(verbose=False):
    """
    Test mode - validates configuration without launching anything.
    """
    print("=" * 60)
    print("macOS Dev Launcher - Configuration Test")
    print("=" * 60)
    
    print(f"\nConfigured Terminals: {', '.join(TERMINAL_APPS)}")
    available = get_available_terminals()
    
    if available:
        print(f"✓ Available Terminals: {', '.join(available)}")
    else:
        print("✗ No configured terminals found!")
        print(f"  Please install one of: {', '.join(TERMINAL_APPS)}")
    
    print(f"\nConfigured Editor: {EDITOR_APP}")
    if app_exists(EDITOR_APP):
        print(f"✓ Editor {EDITOR_APP} is installed")
    else:
        print(f"✗ Editor {EDITOR_APP} not found")
        print(f"  (Editor is optional - will be skipped)")
    
    print("\n" + "=" * 60)
    if available:
        print("Configuration looks good! Ready to use.")
    else:
        print("Please install at least one terminal to continue.")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Launch terminal and editor for a project directory',
        epilog='Note: When called without arguments, uses paths from Automator'
    )
    parser.add_argument(
        'paths',
        nargs='*',
        help='Project directory paths to open'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    parser.add_argument(
        '-t', '--test',
        action='store_true',
        help='Test mode - validate configuration without opening anything'
    )
    
    args = parser.parse_args()
    
    # Test mode
    if args.test:
        test_mode(args.verbose)
        sys.exit(0)
    
    # Handle paths
    if args.paths:
        # Paths provided as arguments
        for path in args.paths:
            # Resolve to absolute path
            abs_path = os.path.abspath(path)
            
            # Validate path exists
            if not os.path.exists(abs_path):
                print(f"Error: Path does not exist: {abs_path}", file=sys.stderr)
                continue
            
            if not os.path.isdir(abs_path):
                print(f"Error: Path is not a directory: {abs_path}", file=sys.stderr)
                continue
            
            open_project(abs_path, args.verbose)
    else:
        # No arguments - show usage
        print("No paths provided.")
        print("\nUsage examples:")
        print("  python3 open_dev_env.py ~/projects/my-app")
        print("  python3 open_dev_env.py --test")
        print("  python3 open_dev_env.py --verbose ~/projects/my-app")
        print("\nOr use via Automator Quick Action (right-click a folder in Finder)")
        sys.exit(1)
