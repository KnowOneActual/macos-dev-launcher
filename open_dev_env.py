#!/usr/bin/env python3
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
# These are used if no config file exists or values are missing
DEFAULT_CONFIG = {
    "terminals": ["Ghostty", "Kitty", "Warp", "Wave"],
    "editor": "VSCodium",
    "logging": {
        "enabled": True,
        "level": "INFO",
        "file": "~/Library/Logs/macos-dev-launcher.log",
        "max_bytes": 1048576,  # 1 MB
        "backup_count": 7
    },
    "behavior": {
        "auto_open_editor": True,
        "remember_choices": False
    }
}

# Config file location
CONFIG_DIR = Path.home() / ".config" / "macos-dev-launcher"
CONFIG_FILE = CONFIG_DIR / "config.json"

# --- CONFIGURATION LOADING ---

def load_config(config_path=None, verbose=False):
    """
    Load configuration from JSON file with fallback to defaults.
    
    Args:
        config_path (Path): Optional path to config file. If None, uses default location.
        verbose (bool): If True, print debug information
    
    Returns:
        dict: Configuration dictionary with all values
    """
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
            
            # Merge user config with defaults (user config takes precedence)
            # Deep merge for nested dicts
            for key, value in user_config.items():
                if key in config and isinstance(config[key], dict) and isinstance(value, dict):
                    config[key].update(value)
                else:
                    config[key] = value
            
            if verbose:
                print(f"✓ Loaded config from {config_path}")
            
        except (json.JSONDecodeError, OSError) as e:
            print(f"Warning: Could not load config from {config_path}: {e}", file=sys.stderr)
            print(f"Using default configuration", file=sys.stderr)
    else:
        if verbose:
            print(f"Config file not found, using defaults")
            print(f"You can create a config file at: {config_path}")
            print(f"See config.example.json for reference")
    
    return config

def create_example_config(verbose=False):
    """
    Create example configuration file at default location.
    
    Args:
        verbose (bool): If True, print status information
    """
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

# Load configuration at module level
config = load_config()

# Extract configuration values
TERMINAL_APPS = config["terminals"]
EDITOR_APP = config["editor"]
LOGGING_ENABLED = config["logging"]["enabled"]
LOG_LEVEL = config["logging"]["level"]
LOG_FILE = Path(config["logging"]["file"]).expanduser()
LOG_DIR = LOG_FILE.parent
LOG_MAX_BYTES = config["logging"]["max_bytes"]
LOG_BACKUP_COUNT = config["logging"]["backup_count"]
AUTO_OPEN_EDITOR = config["behavior"]["auto_open_editor"]
REMEMBER_CHOICES = config["behavior"]["remember_choices"]

# --- LOGGING SETUP ---

def setup_logging(enabled=True, verbose=False, level=None):
    """
    Configure logging with rotation and appropriate level.
    
    Args:
        enabled (bool): Whether to enable file logging
        verbose (bool): If True, set to DEBUG level and also log to console
        level (str): Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger('macos-dev-launcher')
    
    # Determine log level
    if verbose:
        log_level = logging.DEBUG
    elif level:
        log_level = getattr(logging, level.upper(), logging.INFO)
    else:
        log_level = logging.INFO
    
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    if enabled:
        try:
            # Ensure log directory exists
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            
            # Create rotating file handler
            file_handler = RotatingFileHandler(
                LOG_FILE,
                maxBytes=LOG_MAX_BYTES,
                backupCount=LOG_BACKUP_COUNT
            )
            file_handler.setLevel(logging.DEBUG)
            
            # Create formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            
        except (OSError, PermissionError) as e:
            # If logging setup fails, print warning but continue
            print(f"Warning: Could not set up logging: {e}", file=sys.stderr)
    
    # Add console handler if verbose
    if verbose:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
    
    return logger

# Initialize logger (will be reconfigured in main)
logger = logging.getLogger('macos-dev-launcher')

# --- HELPER FUNCTIONS ---

def app_exists(app_name):
    """
    Check if an application exists in /Applications.
    
    Args:
        app_name (str): Name of the application (without .app extension)
    
    Returns:
        bool: True if app exists, False otherwise
    """
    if not app_name:  # Handle empty string (e.g., disabled editor)
        return False
    app_path = Path(f"/Applications/{app_name}.app")
    exists = app_path.exists() and app_path.is_dir()
    logger.debug(f"Checking if {app_name} exists: {exists}")
    return exists

def sanitize_path(path_str, verbose=False):
    """
    Sanitize and validate a path for safe usage.
    
    Args:
        path_str (str): Path string to sanitize
        verbose (bool): If True, print debug information
    
    Returns:
        Path: Sanitized pathlib.Path object, or None if invalid
    """
    logger.debug(f"Sanitizing path: {path_str}")
    
    try:
        # Convert to Path object and resolve to absolute path
        path = Path(path_str).expanduser().resolve()
        
        logger.debug(f"  Resolved to: {path}")
        logger.debug(f"  Is symlink: {path.is_symlink() or Path(path_str).is_symlink()}")
        
        if verbose:
            print(f"Sanitizing path: {path_str}")
            print(f"  Resolved to: {path}")
            print(f"  Is symlink: {path.is_symlink() or Path(path_str).is_symlink()}")
        
        # Validate path exists
        if not path.exists():
            logger.warning(f"Path does not exist: {path}")
            if verbose:
                print(f"  ✗ Path does not exist")
            return None
        
        # Validate it's a directory
        if not path.is_dir():
            logger.warning(f"Path is not a directory: {path}")
            if verbose:
                print(f"  ✗ Path is not a directory")
            return None
        
        # Security check: ensure path is not trying to escape user directory
        # This prevents malicious paths like "../../../etc"
        try:
            home = Path.home()
            # Allow paths in user home or common dev locations
            if not (str(path).startswith(str(home)) or 
                    str(path).startswith('/tmp') or
                    str(path).startswith('/var/folders')):
                logger.warning(f"Path outside user directory: {path}")
                if verbose:
                    print(f"  ⚠ Warning: Path outside user directory")
                # Don't block, but log warning
        except (RuntimeError, OSError) as e:
            logger.debug(f"Could not determine home directory: {e}")
            # Can't determine home, skip security check
            pass
        
        logger.info(f"Path validated successfully: {path}")
        if verbose:
            print(f"  ✓ Path is valid")
        
        return path
        
    except (OSError, RuntimeError, ValueError) as e:
        logger.error(f"Path sanitization failed for '{path_str}': {e}")
        if verbose:
            print(f"  ✗ Path sanitization failed: {e}")
        return None

def get_available_terminals():
    """
    Filter the configured terminal list to only include installed apps.
    
    Returns:
        list: List of installed terminal app names
    """
    available = [app for app in TERMINAL_APPS if app_exists(app)]
    logger.info(f"Available terminals: {available} (out of {TERMINAL_APPS})")
    return available

def show_error_dialog(title, message):
    """
    Display an error dialog to the user.
    
    Args:
        title (str): Dialog title
        message (str): Error message to display
    """
    logger.error(f"Error dialog: {title} - {message}")
    
    # Escape quotes in message for AppleScript
    safe_message = message.replace('"', '\\"')
    safe_title = title.replace('"', '\\"')
    
    script = f"""
    display dialog "{safe_message}" buttons {{"OK"}} default button "OK" with title "{safe_title}" with icon stop
    """
    try:
        subprocess.run(['osascript', '-e', script], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to display error dialog: {e}")
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
    logger.debug("Asking user to choose terminal")
    
    # Get only installed terminals
    available_terminals = get_available_terminals()
    
    if verbose:
        print(f"Configured terminals: {TERMINAL_APPS}")
        print(f"Available terminals: {available_terminals}")
    
    # Handle case where no valid terminals are found
    if not available_terminals:
        logger.error("No configured terminals are installed")
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
        if result == "CANCEL":
            logger.info("User cancelled terminal selection")
            if verbose:
                print(f"User selected: {result}")
            return None
        else:
            logger.info(f"User selected terminal: {result}")
            if verbose:
                print(f"User selected: {result}")
            return result
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to display terminal picker: {e}")
        show_error_dialog("Terminal Selection Failed", f"Could not display terminal picker: {e}")
        return None

def ask_open_editor(project_name, verbose=False):
    """
    Asks if the user wants to open the configured editor.
    Only asks if the editor is actually installed and auto_open_editor is enabled.
    
    Args:
        project_name (str): Name of the project folder
        verbose (bool): If True, print debug information
    
    Returns:
        bool: True if user wants to open editor and it exists, False otherwise
    """
    logger.debug(f"Asking if user wants to open editor for project: {project_name}")
    
    # Skip if auto_open_editor is disabled
    if not AUTO_OPEN_EDITOR:
        logger.info("auto_open_editor is disabled, skipping editor prompt")
        return False
    
    # Check if editor exists before asking
    if not app_exists(EDITOR_APP):
        logger.info(f"Editor {EDITOR_APP} not installed, skipping editor prompt")
        if verbose:
            print(f"Editor {EDITOR_APP} not installed, skipping...")
        # Silently skip if editor not installed (don't interrupt workflow)
        return False
    
    if verbose:
        print(f"Editor {EDITOR_APP} is available")
    
    # Escape project name for AppleScript
    safe_project_name = project_name.replace("'", "\\'").replace('"', '\\"')
    
    script = f"""
    display dialog "Open '{safe_project_name}' in {EDITOR_APP} too?" buttons {{"No", "Yes"}} default button "Yes" with icon note
    return button returned of result
    """
    try:
        result = subprocess.check_output(['osascript', '-e', script], text=True).strip()
        open_editor = result == "Yes"
        logger.info(f"User chose to open editor: {open_editor}")
        if verbose:
            print(f"User chose to open editor: {open_editor}")
        return open_editor
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to display editor prompt: {e}")
        # If dialog fails, default to not opening editor
        return False

def open_project(path, verbose=False):
    """
    Main function to open a project in terminal and optionally editor.
    
    Args:
        path (str or Path): Path to the project directory
        verbose (bool): If True, print debug information
    """
    logger.info(f"Opening project: {path}")
    
    # Sanitize the path first
    sanitized_path = sanitize_path(str(path), verbose)
    
    if not sanitized_path:
        error_msg = f"Invalid or inaccessible path: {path}"
        logger.error(error_msg)
        show_error_dialog("Invalid Path", error_msg)
        if verbose:
            print(f"✗ {error_msg}")
        return
    
    # Use sanitized path as string for subprocess
    path_str = str(sanitized_path)
    project_name = sanitized_path.name
    
    logger.info(f"Project name: {project_name}, Path: {path_str}")
    
    if verbose:
        print(f"\nOpening project: {project_name}")
        print(f"Path: {path_str}")
    
    # 1. Ask for Terminal (with validation)
    terminal_app = ask_terminal_choice(verbose)
    if not terminal_app:
        logger.info("No terminal selected, aborting")
        if verbose:
            print("No terminal selected or available")
        return  # User cancelled or no terminals available

    # 2. Open Terminal
    try:
        logger.info(f"Launching {terminal_app} for {project_name}")
        if verbose:
            print(f"Launching {terminal_app}...")
        # Use subprocess with list arguments (safer than shell=True)
        # Path is already sanitized, but subprocess handles it safely
        subprocess.run(["open", "-a", terminal_app, path_str], check=True)
        logger.info(f"Successfully launched {terminal_app}")
        if verbose:
            print(f"✓ {terminal_app} launched successfully")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to launch {terminal_app}: {e}")
        show_error_dialog(
            "Failed to Open Terminal",
            f"Could not launch {terminal_app}. Error: {e}"
        )
        return
    
    # 3. Ask for Editor (with validation)
    if ask_open_editor(project_name, verbose):
        try:
            logger.info(f"Launching {EDITOR_APP} for {project_name}")
            if verbose:
                print(f"Launching {EDITOR_APP}...")
            subprocess.run(["open", "-a", EDITOR_APP, path_str], check=True)
            logger.info(f"Successfully launched {EDITOR_APP}")
            if verbose:
                print(f"✓ {EDITOR_APP} launched successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to launch {EDITOR_APP}: {e}")
            show_error_dialog(
                "Failed to Open Editor",
                f"Could not launch {EDITOR_APP}. Error: {e}"
            )
            # Continue anyway - terminal already opened successfully
    else:
        logger.info("User chose not to open editor")
    
    logger.info(f"Finished opening project: {project_name}")

def test_mode(verbose=False):
    """
    Test mode - validates configuration without launching anything.
    """
    logger.info("Running in test mode")
    
    print("=" * 60)
    print("macOS Dev Launcher - Configuration Test")
    print("=" * 60)
    
    # Configuration file info
    print(f"\nConfiguration:")
    print(f"  Config file: {CONFIG_FILE}")
    if CONFIG_FILE.exists():
        print(f"  ✓ Config file exists")
    else:
        print(f"  ✗ Config file not found (using defaults)")
        print(f"  Run with --create-config to create one")
    
    print(f"\nConfigured Terminals: {', '.join(TERMINAL_APPS)}")
    available = get_available_terminals()
    
    if available:
        print(f"✓ Available Terminals: {', '.join(available)}")
    else:
        print("✗ No configured terminals found!")
        print(f"  Please install one of: {', '.join(TERMINAL_APPS)}")
    
    print(f"\nConfigured Editor: {EDITOR_APP if EDITOR_APP else '(none)'}")
    if EDITOR_APP:
        if app_exists(EDITOR_APP):
            print(f"✓ Editor {EDITOR_APP} is installed")
        else:
            print(f"✗ Editor {EDITOR_APP} not found")
            print(f"  (Editor is optional - will be skipped)")
    else:
        print(f"  Editor disabled (auto_open_editor: {AUTO_OPEN_EDITOR})")
    
    # Logging info
    print(f"\nLogging Configuration:")
    print(f"  Log file: {LOG_FILE}")
    print(f"  Logging enabled: {LOGGING_ENABLED}")
    print(f"  Log level: {LOG_LEVEL}")
    print(f"  Max log size: {LOG_MAX_BYTES / 1024:.0f} KB")
    print(f"  Backup count: {LOG_BACKUP_COUNT}")
    if LOG_FILE.exists():
        size = LOG_FILE.stat().st_size
        print(f"  Current log size: {size / 1024:.2f} KB")
    else:
        print(f"  Log file does not exist yet")
    
    # Behavior settings
    print(f"\nBehavior:")
    print(f"  Auto-open editor: {AUTO_OPEN_EDITOR}")
    print(f"  Remember choices: {REMEMBER_CHOICES} (Phase 2.4 feature)")
    
    # Test path sanitization
    if verbose:
        print("\n" + "=" * 60)
        print("Path Sanitization Tests:")
        print("=" * 60)
        
        test_paths = [
            ".",
            "~",
            "/tmp",
            "../../../etc",  # Potentially malicious
            "test dir with spaces",
        ]
        
        for test_path in test_paths:
            print(f"\nTesting: {test_path}")
            result = sanitize_path(test_path, verbose=True)
            if result:
                print(f"  Result: {result}")
    
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
    parser.add_argument(
        '--no-log',
        action='store_true',
        help='Disable file logging'
    )
    parser.add_argument(
        '--config',
        type=str,
        help='Path to custom config file'
    )
    parser.add_argument(
        '--create-config',
        action='store_true',
        help='Create example config file at default location'
    )
    
    args = parser.parse_args()
    
    # Handle config creation
    if args.create_config:
        if create_example_config(verbose=True):
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Load custom config if specified
    if args.config:
        config = load_config(args.config, args.verbose)
        # Re-extract configuration values
        TERMINAL_APPS = config["terminals"]
        EDITOR_APP = config["editor"]
        LOGGING_ENABLED = config["logging"]["enabled"]
        LOG_LEVEL = config["logging"]["level"]
    
    # Setup logging with appropriate settings
    logger = setup_logging(
        enabled=LOGGING_ENABLED and not args.no_log,
        verbose=args.verbose,
        level=LOG_LEVEL
    )
    
    logger.info("=" * 50)
    logger.info("macOS Dev Launcher started")
    logger.info(f"Arguments: {sys.argv[1:]}")
    logger.info(f"Verbose: {args.verbose}, Test mode: {args.test}, Logging: {not args.no_log}")
    logger.info(f"Config file: {args.config if args.config else 'default'}")
    
    try:
        # Test mode
        if args.test:
            test_mode(args.verbose)
            sys.exit(0)
        
        # Handle paths
        if args.paths:
            # Paths provided as arguments
            for path in args.paths:
                open_project(path, args.verbose)
        else:
            # No arguments - show usage
            print("No paths provided.")
            print("\nUsage examples:")
            print("  python3 open_dev_env.py ~/projects/my-app")
            print("  python3 open_dev_env.py --test")
            print("  python3 open_dev_env.py --verbose ~/projects/my-app")
            print("  python3 open_dev_env.py --no-log ~/projects/my-app")
            print("  python3 open_dev_env.py --config ~/my-config.json ~/projects/my-app")
            print("  python3 open_dev_env.py --create-config")
            print("\nOr use via Automator Quick Action (right-click a folder in Finder)")
            logger.info("No paths provided, showing usage")
            sys.exit(1)
    
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise
    
    finally:
        logger.info("macOS Dev Launcher finished")
        logger.info("=" * 50)
