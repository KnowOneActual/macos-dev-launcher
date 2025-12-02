import sys
import os
import subprocess
import argparse
import shlex
import logging
import json
from pathlib import Path
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler

# --- DEFAULT CONFIGURATION ---
DEFAULT_CONFIG = {
    "terminals": ["Ghostty", "Kitty", "Warp", "Wave"],
    "editors": ["VSCodium"],
    "app_args": {},
    "logging": {
        "enabled": True,
        "level": "INFO",
        "file": "~/Library/Logs/macos-dev-launcher.log",
        "max_bytes": 1048576,
        "backup_count": 7
    },
    "behavior": {
        "auto_open_editor": True,
        "remember_choices": False,
        "combined_dialog": False  # PHASE 3.1
    }
}

# Config file location
CONFIG_DIR = Path.home() / ".config" / "macos-dev-launcher"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

# --- CONFIGURATION LOADING ---

def load_config(config_path=None, verbose=False):
    """Load configuration from JSON file with fallback to defaults."""
    config = DEFAULT_CONFIG.copy()
    
    if config_path is None:
        config_path = CONFIG_FILE
    else:
        config_path = Path(config_path).expanduser()
    
    if verbose:
        print(f"Looking for config at: {config_path}")
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                user_config = json.load(f)
            
            # Deep merge
            for key, value in user_config.items():
                if key in config and isinstance(config[key], dict) and isinstance(value, dict):
                    config[key].update(value)
                else:
                    config[key] = value
            
            # Backward compatibility
            if "editor" in user_config and "editors" not in user_config:
                if user_config["editor"]:
                    config["editors"] = [user_config["editor"]]
                else:
                    config["editors"] = []
                if verbose:
                    print(f"  Converted legacy 'editor' config to 'editors' list")
            
            if verbose:
                print(f"✓ Loaded config from {config_path}")
            
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Could not load config from {config_path}: {e}", file=sys.stderr)
            print(f"Using default configuration", file=sys.stderr)
    else:
        if verbose:
            print(f"Config file not found, using defaults")
    
    return config

def create_example_config(verbose=False):
    """Create example configuration file at default location."""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        
        if verbose:
            print(f"✓ Created config file at: {CONFIG_FILE}")
            print(f"Edit this file to customize your settings")
        
        return True
    except (OSError, PermissionError) as e:
        print(f"Error: Could not create config file: {e}", file=sys.stderr)
        return False

# Load configuration
config = load_config()

# Extract values
TERMINAL_APPS = config["terminals"]
EDITOR_APPS = config["editors"]
APP_ARGS = config.get("app_args", {})
LOGGING_ENABLED = config["logging"]["enabled"]
LOG_LEVEL = config["logging"]["level"]
LOG_FILE = Path(config["logging"]["file"]).expanduser()
LOG_DIR = LOG_FILE.parent
LOG_MAX_BYTES = config["logging"]["max_bytes"]
LOG_BACKUP_COUNT = config["logging"]["backup_count"]
AUTO_OPEN_EDITOR = config["behavior"]["auto_open_editor"]
REMEMBER_CHOICES = config["behavior"]["remember_choices"]
COMBINED_DIALOG = config["behavior"].get("combined_dialog", False)  # PHASE 3.1

# --- LOGGING SETUP ---

def setup_logging(enabled=True, verbose=False, level=None):
    """Configure logging with rotation."""
    logger = logging.getLogger('macos-dev-launcher')
    
    if verbose:
        log_level = logging.DEBUG
    elif level:
        log_level = getattr(logging, level.upper(), logging.INFO)
    else:
        log_level = logging.INFO
    
    logger.setLevel(log_level)
    logger.handlers.clear()
    
    if enabled:
        try:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                LOG_FILE,
                maxBytes=LOG_MAX_BYTES,
                backupCount=LOG_BACKUP_COUNT
            )
            file_handler.setLevel(logging.DEBUG)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            
        except (OSError, PermissionError) as e:
            print(f"Warning: Could not set up logging: {e}", file=sys.stderr)
    
    if verbose:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

logger = logging.getLogger('macos-dev-launcher')

# --- PHASE 2.4: HISTORY/MEMORY FUNCTIONS ---

def load_history():
    """Load user's choice history."""
    if not HISTORY_FILE.exists():
        logger.debug(f"History file does not exist: {HISTORY_FILE}")
        return {}
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
        logger.debug(f"Loaded history with {len(history)} projects")
        return history
    except (json.JSONDecodeError, OSError) as e:
        logger.warning(f"Could not load history: {e}")
        return {}

def save_choice(project_path, terminal, editor):
    """Save user's choice for this project."""
    if not REMEMBER_CHOICES:
        logger.debug("remember_choices disabled, not saving")
        return
    
    try:
        history = load_history()
        
        path_key = str(project_path)
        history[path_key] = {
            "terminal": terminal,
            "editor": editor,
            "last_used": datetime.now().isoformat()
        }
        
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
        
        logger.info(f"Saved choice: terminal={terminal}, editor={editor}")
        
    except (OSError, PermissionError, json.JSONDecodeError) as e:
        logger.warning(f"Could not save choice: {e}")

def get_last_choice(project_path):
    """Get last terminal/editor used for this project."""
    if not REMEMBER_CHOICES:
        return None, None
    
    history = load_history()
    path_key = str(project_path)
    
    if path_key in history:
        choice = history[path_key]
        terminal = choice.get("terminal")
        editor = choice.get("editor")
        logger.debug(f"Found history: terminal={terminal}, editor={editor}")
        return terminal, editor
    else:
        logger.debug(f"No history found")
        return None, None

# --- HELPER FUNCTIONS ---

def app_exists(app_name):
    """Check if application exists in /Applications."""
    if not app_name:
        return False
    app_path = Path(f"/Applications/{app_name}.app")
    exists = app_path.exists() and app_path.is_dir()
    logger.debug(f"Checking {app_name}: {exists}")
    return exists

def sanitize_path(path_str, verbose=False):
    """Sanitize and validate a path."""
    logger.debug(f"Sanitizing path: {path_str}")
    
    try:
        path = Path(path_str).expanduser().resolve()
        
        if verbose:
            print(f"Sanitizing: {path_str}")
            print(f"  Resolved: {path}")
        
        if not path.exists():
            logger.warning(f"Path does not exist: {path}")
            if verbose:
                print(f"  ✗ Does not exist")
            return None
        
        if not path.is_dir():
            logger.warning(f"Not a directory: {path}")
            if verbose:
                print(f"  ✗ Not a directory")
            return None
        
        logger.info(f"Path validated: {path}")
        if verbose:
            print(f"  ✓ Valid")
        
        return path
        
    except (OSError, RuntimeError, ValueError) as e:
        logger.error(f"Path sanitization failed: {e}")
        if verbose:
            print(f"  ✗ Failed: {e}")
        return None

def get_available_terminals():
    """Get list of installed terminals."""
    available = [app for app in TERMINAL_APPS if app_exists(app)]
    logger.info(f"Available terminals: {available}")
    return available

def get_available_editors():
    """Get list of installed editors."""
    available = [app for app in EDITOR_APPS if app_exists(app)]
    logger.info(f"Available editors: {available}")
    return available

def show_error_dialog(title, message):
    """Display error dialog."""
    logger.error(f"Error: {title} - {message}")
    
    safe_message = message.replace('"', '\\\\"')
    safe_title = title.replace('"', '\\\\"')
    
    script = f"""
    display dialog "{safe_message}" buttons {{"OK"}} default button "OK" with title "{safe_title}" with icon stop
    """
    try:
        subprocess.run(['osascript', '-e', script], check=True)
    except subprocess.CalledProcessError:
        print(f"ERROR: {title} - {message}", file=sys.stderr)

# --- PHASE 3.1: COMBINED DIALOG ---

def ask_combined_choice(project_path, project_name, verbose=False):
    """
    PHASE 3.1: Single dialog for both terminal and editor.
    
    Returns:
        tuple: (terminal_app, editor_app) or (None, None)
    """
    logger.debug("Combined choice dialog")
    
    terminals = get_available_terminals()
    editors = get_available_editors()
    
    if verbose:
        print(f"Combined dialog mode")
        print(f"  Terminals: {terminals}")
        print(f"  Editors: {editors}")
    
    if not terminals:
        logger.error("No terminals installed")
        show_error_dialog(
            "No Terminals",
            f"Please install one of: {', '.join(TERMINAL_APPS)}"
        )
        return None, None
    
    # Get last choices
    last_term, last_ed = get_last_choice(project_path)
    
    # Defaults
    default_term = last_term if last_term in terminals else terminals[0]
    
    editor_opts = ["None"] + editors
    if last_ed and last_ed in editors:
        default_ed = last_ed
    elif last_ed is None and REMEMBER_CHOICES:
        default_ed = "None"
    else:
        default_ed = editors[0] if editors else "None"
    
    # Build AppleScript lists
    term_list = "{" + ", ".join([f'"{t}"' for t in terminals]) + "}"
    ed_list = "{" + ", ".join([f'"{e}"' for e in editor_opts]) + "}"
    safe_name = project_name.replace('"', '\\\\"')
    
    script = f"""
    set termChoice to choose from list {term_list} with prompt "🚀 Terminal for '{safe_name}':" default items {{"{default_term}"}}
    if termChoice is false then return "CANCEL"
    
    set edChoice to choose from list {ed_list} with prompt "Terminal: " & (item 1 of termChoice) & return & return & "📝 Editor:" default items {{"{default_ed}"}}
    if edChoice is false then return "CANCEL"
    
    return (item 1 of termChoice) & "|" & (item 1 of edChoice)
    """
    
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        
        if result == "CANCEL":
            logger.info("User cancelled")
            if verbose:
                print("User cancelled")
            return None, None
        
        parts = result.split("|")
        if len(parts) != 2:
            logger.error(f"Unexpected result: {result}")
            return None, None
        
        terminal = parts[0]
        editor = None if parts[1] == "None" else parts[1]
        
        logger.info(f"Selected: terminal={terminal}, editor={editor}")
        if verbose:
            print(f"Selected: {terminal} + {editor or 'none'}")
        
        return terminal, editor
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Dialog failed: {e}")
        show_error_dialog("Selection Failed", f"Could not display dialog: {e}")
        return None, None

# --- ORIGINAL DIALOG FUNCTIONS ---

def ask_terminal_choice(project_path, verbose=False):
    """Show terminal picker dialog."""
    logger.debug("Terminal choice dialog")
    
    terminals = get_available_terminals()
    
    if verbose:
        print(f"Available terminals: {terminals}")
    
    if not terminals:
        logger.error("No terminals installed")
        show_error_dialog(
            "No Terminals",
            f"Install one of: {', '.join(TERMINAL_APPS)}"
        )
        return None
    
    last_term, _ = get_last_choice(project_path)
    default = last_term if last_term in terminals else terminals[0]
    
    options_str = "{" + ", ".join([f'"{app}"' for app in terminals]) + "}"
    
    script = f"""
    set appList to {options_str}
    set choice to choose from list appList with prompt "🚀 Open project in which terminal?" default items {{"{default}"}}
    if choice is false then
        return "CANCEL"
    else
        return item 1 of choice
    end if
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        if result == "CANCEL":
            logger.info("User cancelled")
            return None
        logger.info(f"Selected: {result}")
        if verbose:
            print(f"Selected: {result}")
        return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Dialog failed: {e}")
        show_error_dialog("Failed", f"Could not display picker: {e}")
        return None

def ask_editor_choice(project_name, project_path, verbose=False):
    """Ask which editor to open."""
    logger.debug(f"Editor choice for: {project_name}")
    
    if not AUTO_OPEN_EDITOR:
        logger.info("auto_open_editor disabled")
        return None
    
    editors = get_available_editors()
    
    if verbose:
        print(f"Available editors: {editors}")
    
    if not editors:
        logger.info("No editors installed")
        return None
    
    _, last_ed = get_last_choice(project_path)
    
    # Single editor: Yes/No dialog
    if len(editors) == 1:
        editor = editors[0]
        safe_name = project_name.replace('"', '\\\\"')
        
        default_btn = "Yes" if last_ed == editor else ("No" if last_ed is None else "Yes")
        
        script = f"""
        display dialog "Open '{safe_name}' in {editor} too?" buttons {{"No", "Yes"}} default button "{default_btn}" with icon note
        return button returned of result
        """
        try:
            result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
            if result == "Yes":
                logger.info(f"Chose {editor}")
                return editor
            logger.info("Chose not to open editor")
            return None
        except subprocess.CalledProcessError:
            return None
    
    # Multiple editors: picker
    safe_name = project_name.replace('"', '\\\\"')
    editor_list = ["None"] + editors
    options_str = "{" + ", ".join([f'"{e}"' for e in editor_list]) + "}"
    
    if last_ed and last_ed in editors:
        default = last_ed
    elif last_ed is None and REMEMBER_CHOICES:
        default = "None"
    else:
        default = editors[0]
    
    script = f"""
    set appList to {options_str}
    set choice to choose from list appList with prompt "📝 Open '{safe_name}' in which editor?" default items {{"{default}"}}
    if choice is false then
        return "CANCEL"
    else
        return item 1 of choice
    end if
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        if result == "CANCEL" or result == "None":
            logger.info("Chose not to open editor")
            return None
        logger.info(f"Selected: {result}")
        return result
    except subprocess.CalledProcessError:
        return None

# --- MAIN FUNCTION ---

def open_project(path, verbose=False):
    """Open project in terminal and editor."""
    logger.info(f"Opening: {path}")
    
    sanitized_path = sanitize_path(str(path), verbose)
    
    if not sanitized_path:
        error_msg = f"Invalid path: {path}"
        logger.error(error_msg)
        show_error_dialog("Invalid Path", error_msg)
        return
    
    path_str = str(sanitized_path)
    project_name = sanitized_path.name
    
    if verbose:
        print(f"\nOpening: {project_name}")
        print(f"Path: {path_str}")
    
    # PHASE 3.1: Combined or separate dialogs
    if COMBINED_DIALOG:
        terminal_app, editor_app = ask_combined_choice(sanitized_path, project_name, verbose)
        if not terminal_app:
            logger.info("No terminal selected")
            return
    else:
        terminal_app = ask_terminal_choice(sanitized_path, verbose)
        if not terminal_app:
            logger.info("No terminal selected")
            return
        editor_app = None  # Will ask after terminal launches
    
    # Launch terminal
    try:
        logger.info(f"Launching {terminal_app}")
        if verbose:
            print(f"Launching {terminal_app}...")
        
        cmd = ["open", "-a", terminal_app, path_str]
        if terminal_app in APP_ARGS:
            cmd.extend(["--args"] + APP_ARGS[terminal_app])
            logger.debug(f"Custom args: {APP_ARGS[terminal_app]}")
        
        subprocess.run(cmd, check=True)
        logger.info(f"Launched {terminal_app}")
        if verbose:
            print(f"✓ {terminal_app} launched")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to launch terminal: {e}")
        show_error_dialog("Failed", f"Could not launch {terminal_app}: {e}")
        return
    
    # Ask for editor if not already chosen
    if not COMBINED_DIALOG:
        editor_app = ask_editor_choice(project_name, sanitized_path, verbose)
    
    # Launch editor
    if editor_app:
        try:
            logger.info(f"Launching {editor_app}")
            if verbose:
                print(f"Launching {editor_app}...")
            
            cmd = ["open", "-a", editor_app, path_str]
            if editor_app in APP_ARGS:
                cmd.extend(["--args"] + APP_ARGS[editor_app])
                logger.debug(f"Custom args: {APP_ARGS[editor_app]}")
            
            subprocess.run(cmd, check=True)
            logger.info(f"Launched {editor_app}")
            if verbose:
                print(f"✓ {editor_app} launched")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to launch editor: {e}")
            show_error_dialog("Failed", f"Could not launch {editor_app}: {e}")
    else:
        logger.info("No editor")
    
    # Save choices
    save_choice(sanitized_path, terminal_app, editor_app)
    
    logger.info(f"Finished: {project_name}")

# --- TEST MODE ---

def test_mode(verbose=False):
    """Test configuration."""
    logger.info("Test mode")
    
    print("=" * 60)
    print("macOS Dev Launcher - Configuration Test")
    print("=" * 60)
    
    print("\nConfiguration:")
    print(f"  File: {CONFIG_FILE}")
    if CONFIG_FILE.exists():
        print(f"  ✓ Exists")
    else:
        print(f"  ✗ Not found (using defaults)")
    
    print(f"\nTerminals: {', '.join(TERMINAL_APPS)}")
    available = get_available_terminals()
    if available:
        print(f"✓ Available: {', '.join(available)}")
    else:
        print(f"✗ None installed")
    
    print(f"\nEditors: {', '.join(EDITOR_APPS) if EDITOR_APPS else '(none)'}")
    if EDITOR_APPS:
        available_eds = get_available_editors()
        if available_eds:
            print(f"✓ Available: {', '.join(available_eds)}")
        else:
            print(f"✗ None installed")
    
    print(f"\nCustom Args:")
    if APP_ARGS:
        for app, args in APP_ARGS.items():
            print(f"  {app}: {' '.join(args)}")
    else:
        print(f"  None")
    
    print(f"\nLogging:")
    print(f"  File: {LOG_FILE}")
    print(f"  Enabled: {LOGGING_ENABLED}")
    print(f"  Level: {LOG_LEVEL}")
    if LOG_FILE.exists():
        size = LOG_FILE.stat().st_size
        print(f"  Size: {size / 1024:.2f} KB")
    
    print(f"\nBehavior:")
    print(f"  Auto-open editor: {AUTO_OPEN_EDITOR}")
    print(f"  Remember choices: {REMEMBER_CHOICES}")
    print(f"  Combined dialog: {COMBINED_DIALOG}")  # PHASE 3.1
    
    print(f"\nHistory:")
    print(f"  File: {HISTORY_FILE}")
    if REMEMBER_CHOICES:
        print(f"  ✓ Enabled")
        if HISTORY_FILE.exists():
            history = load_history()
            print(f"  ✓ {len(history)} project(s)")
        else:
            print(f"  ⚠ Will be created on first use")
    else:
        print(f"  ✗ Disabled")
    
    print("\n" + "=" * 60)
    if available:
        print("✓ Ready to use")
    else:
        print("✗ Install at least one terminal")
    print("=" * 60)

# --- MAIN ---

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Launch terminal and editor')
    parser.add_argument('paths', nargs='*', help='Project paths')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('-t', '--test', action='store_true', help='Test configuration')
    parser.add_argument('--no-log', action='store_true', help='Disable logging')
    parser.add_argument('--config', type=str, help='Custom config file')
    parser.add_argument('--create-config', action='store_true', help='Create config file')
    
    args = parser.parse_args()
    
    if args.create_config:
        if create_example_config(verbose=True):
            sys.exit(0)
        else:
            sys.exit(1)
    
    if args.config:
        config = load_config(args.config, args.verbose)
        TERMINAL_APPS = config["terminals"]
        EDITOR_APPS = config["editors"]
        APP_ARGS = config.get("app_args", {})
        LOGGING_ENABLED = config["logging"]["enabled"]
        LOG_LEVEL = config["logging"]["level"]
        REMEMBER_CHOICES = config["behavior"]["remember_choices"]
        COMBINED_DIALOG = config["behavior"].get("combined_dialog", False)
    
    logger = setup_logging(
        enabled=LOGGING_ENABLED and not args.no_log,
        verbose=args.verbose,
        level=LOG_LEVEL
    )
    
    logger.info("=" * 50)
    logger.info("Started")
    logger.info(f"Args: {sys.argv[1:]}")
    logger.info(f"Combined dialog: {COMBINED_DIALOG}")
    
    try:
        if args.test:
            test_mode(args.verbose)
            sys.exit(0)
        
        if args.paths:
            for path in args.paths:
                open_project(path, args.verbose)
        else:
            print("No paths provided.")
            print("\nUsage:")
            print("  python3 open_dev_env.py ~/projects/my-app")
            print("  python3 open_dev_env.py --test")
            print("  python3 open_dev_env.py --create-config")
            logger.info("No paths")
            sys.exit(1)
    
    except Exception as e:
        logger.exception(f"Error: {e}")
        raise
    
    finally:
        logger.info("Finished")
        logger.info("=" * 50)