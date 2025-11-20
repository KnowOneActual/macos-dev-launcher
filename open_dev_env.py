#!/usr/bin/env python3
import sys
import os
import subprocess

# --- CONFIGURATION ---
# Added "Kitty" to the list
TERMINAL_APPS = ["Ghostty", "Kitty", "Warp", "Wave"] 
EDITOR_APP = "VSCodium"

def ask_terminal_choice():
    """
    Pops up a list of terminals to choose from.
    """
    # AppleScript list format: {"Ghostty", "Kitty", "Warp", "Wave"}
    options_str = "{" + ", ".join([f'"{app}"' for app in TERMINAL_APPS]) + "}"
    
    # We default to the first item in the list (Ghostty)
    script = f"""
    set appList to {options_str}
    set choice to choose from list appList with prompt "🚀 Open project in which terminal?" default items {{"{TERMINAL_APPS[0]}"}}
    if choice is false then
        return "CANCEL"
    else
        return item 1 of choice
    end if
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        return None if result == "CANCEL" else result
    except:
        return None

def ask_open_editor(project_name):
    """
    Asks if the user wants to open VS Codium.
    """
    script = f"""
    display dialog "Open '{project_name}' in {EDITOR_APP} too?" buttons {{"No", "Yes"}} default button "Yes" with icon note
    return button returned of result
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        return result == "Yes"
    except:
        return False

def open_project(path):
    project_name = os.path.basename(path)
    
    # 1. Ask for Terminal
    terminal_app = ask_terminal_choice()
    if not terminal_app:
        return # User cancelled

    # 2. Open Terminal
    # The 'open -a' command tells macOS to launch that specific app with this file/folder
    subprocess.run(["open", "-a", terminal_app, path])
    
    # 3. Ask for Editor
    if ask_open_editor(project_name):
        subprocess.run(["open", "-a", EDITOR_APP, path])

if __name__ == "__main__":
    # Handle input from Automator
    if len(sys.argv) > 1:
        for path in sys.argv[1:]:
            # Resolve to absolute path just in case
            abs_path = os.path.abspath(path)
            open_project(abs_path)