#!/usr/bin/env python3
import sys
import os
import subprocess
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

def ask_terminal_choice():
    """
    Pops up a list of available terminals to choose from.
    Only shows terminals that are actually installed.
    
    Returns:
        str: Selected terminal name, or None if cancelled/no terminals available
    """
    # Get only installed terminals
    available_terminals = get_available_terminals()
    
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
        return None if result == "CANCEL" else result
    except subprocess.CalledProcessError as e:
        show_error_dialog("Terminal Selection Failed", f"Could not display terminal picker: {e}")
        return None

def ask_open_editor(project_name):
    """
    Asks if the user wants to open the configured editor.
    Only asks if the editor is actually installed.
    
    Args:
        project_name (str): Name of the project folder
    
    Returns:
        bool: True if user wants to open editor and it exists, False otherwise
    """
    # Check if editor exists before asking
    if not app_exists(EDITOR_APP):
        # Silently skip if editor not installed (don't interrupt workflow)
        return False
    
    script = f"""
    display dialog "Open '{project_name}' in {EDITOR_APP} too?" buttons {{"No", "Yes"}} default button "Yes" with icon note
    return button returned of result
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        return result == "Yes"
    except subprocess.CalledProcessError:
        # If dialog fails, default to not opening editor
        return False

def open_project(path):
    """
    Main function to open a project in terminal and optionally editor.
    
    Args:
        path (str): Path to the project directory
    """
    project_name = os.path.basename(path)
    
    # 1. Ask for Terminal (with validation)
    terminal_app = ask_terminal_choice()
    if not terminal_app:
        return  # User cancelled or no terminals available

    # 2. Open Terminal
    try:
        # The 'open -a' command tells macOS to launch that specific app with this file/folder
        subprocess.run(["open", "-a", terminal_app, path], check=True)
    except subprocess.CalledProcessError as e:
        show_error_dialog(
            "Failed to Open Terminal",
            f"Could not launch {terminal_app}. Error: {e}"
        )
        return
    
    # 3. Ask for Editor (with validation)
    if ask_open_editor(project_name):
        try:
            subprocess.run(["open", "-a", EDITOR_APP, path], check=True)
        except subprocess.CalledProcessError as e:
            show_error_dialog(
                "Failed to Open Editor",
                f"Could not launch {EDITOR_APP}. Error: {e}"
            )
            # Continue anyway - terminal already opened successfully

if __name__ == "__main__":
    # Handle input from Automator
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            # Resolve to absolute path just in case
            abs_path = os.path.abspath(path)
            open_project(abs_path)
