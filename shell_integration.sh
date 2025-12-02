#!/bin/bash
# macOS Dev Launcher - Shell Integration
# Phase 4: Smart project launching with shell wrapper
# Source this in your .zshrc or .bashrc

# Get the directory where this script is located
LAUNCHER_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER_SCRIPT="$LAUNCHER_DIR/open_dev_env.py"
CONFIG_DIR="$HOME/.config/macos-dev-launcher"
HISTORY_FILE="$CONFIG_DIR/history.json"

# Configuration - customize these paths for your setup
PROJECT_SEARCH_PATHS=(
    "$HOME/github_repo"
    "$HOME/projects"
    "$HOME/work"
    "$HOME/dev"
    "$HOME/src"
)

# --- HELPER FUNCTIONS ---

# Extract project name from full path
_get_project_name() {
    basename "$1"
}

# Find a project directory by name
_find_project() {
    local project_name="$1"
    
    # If it's a full path, return it
    if [[ "$project_name" == /* ]] || [[ "$project_name" == ~* ]]; then
        echo "$project_name"
        return 0
    fi
    
    # Special case: current directory
    if [[ "$project_name" == "." || "$project_name" == "" ]]; then
        echo "$(pwd)"
        return 0
    fi
    
    # Search in configured paths
    for search_path in "${PROJECT_SEARCH_PATHS[@]}"; do
        if [[ -d "$search_path/$project_name" ]]; then
            echo "$search_path/$project_name"
            return 0
        fi
    done
    
    # Try exact path (might be relative)
    if [[ -d "$project_name" ]]; then
        echo "$(cd "$project_name" && pwd)"
        return 0
    fi
    
    return 1
}

# Extract recent projects from history.json
_get_recent_projects() {
    if [[ ! -f "$HISTORY_FILE" ]]; then
        return 1
    fi
    
    # Parse JSON and get paths sorted by last_used (newest first)
    python3 -c "
import json
from datetime import datetime

try:
    with open('$HISTORY_FILE', 'r') as f:
        history = json.load(f)
    
    # Sort by last_used timestamp (most recent first)
    sorted_projects = sorted(
        history.items(),
        key=lambda x: x[1].get('last_used', ''),
        reverse=True
    )
    
    # Print top 5 with nice formatting
    for i, (path, data) in enumerate(sorted_projects[:5], 1):
        name = path.split('/')[-1]
        print(f'{i}. {name} ({path})')
except:
    pass
" 2>/dev/null
}

# Show help
_dev_help() {
    cat << EOF
📱 macOS Dev Launcher - Shell Integration (Phase 4)

USAGE:
  dev [project]           Open project (searches in common paths)
  dev .                   Open current directory
  dev /full/path          Open with full path
  dev --recent            Pick from 5 most recent projects
  dev --list              Show all projects in history
  dev --help              Show this help

EXAMPLES:
  dev my-project          → ~/github_repo/my-project
  dev .                   → Current directory
  dev ~/projects/myapp    → Full path
  dev --recent            → Interactive picker

SEARCH PATHS:
$(for path in "${PROJECT_SEARCH_PATHS[@]}"; do echo "  • $path"; done)

EDIT SEARCH PATHS:
  Edit PROJECT_SEARCH_PATHS in ~/.config/macos-dev-launcher/shell_integration.sh

EOF
}

# Show all projects in history
_dev_list() {
    if [[ ! -f "$HISTORY_FILE" ]]; then
        echo "No history yet. Open a project first!"
        return 1
    fi
    
    echo "📚 All projects in history:"
    python3 -c "
import json
from datetime import datetime

try:
    with open('$HISTORY_FILE', 'r') as f:
        history = json.load(f)
    
    # Sort by last_used
    sorted_projects = sorted(
        history.items(),
        key=lambda x: x[1].get('last_used', ''),
        reverse=True
    )
    
    for path, data in sorted_projects:
        name = path.split('/')[-1]
        last_used = data.get('last_used', 'unknown')
        term = data.get('terminal', 'unknown')
        editor = data.get('editor', 'none')
        
        # Parse ISO timestamp
        try:
            dt = datetime.fromisoformat(last_used)
            last_used = dt.strftime('%Y-%m-%d %H:%M')
        except:
            pass
        
        print(f'  • {name:20} ({term} + {editor:10}) - {last_used}')
        print(f'    {path}')
except:
    print('  (error reading history)')
" 2>/dev/null
}

# Show recent projects picker
_dev_recent() {
    if [[ ! -f "$HISTORY_FILE" ]]; then
        echo "No history yet. Open a project first!"
        return 1
    fi
    
    echo "📋 Recent projects (pick one):"
    _get_recent_projects
    
    read -p "Enter number (1-5): " choice
    
    if ! [[ "$choice" =~ ^[1-5]$ ]]; then
        echo "Invalid choice"
        return 1
    fi
    
    # Extract path from the selected project
    local project_path=$(python3 -c "
import json

try:
    with open('$HISTORY_FILE', 'r') as f:
        history = json.load(f)
    
    sorted_projects = sorted(
        history.items(),
        key=lambda x: x[1].get('last_used', ''),
        reverse=True
    )
    
    if $choice <= len(sorted_projects):
        print(sorted_projects[$choice - 1][0])
except:
    pass
" 2>/dev/null)
    
    if [[ -z "$project_path" ]]; then
        echo "Could not find project"
        return 1
    fi
    
    echo "Opening: $project_path"
    python3 "$LAUNCHER_SCRIPT" "$project_path"
}

# Tab completion for zsh
_dev_completion() {
    local cur="${COMP_WORDS[COMP_CWORD]}"
    local projects=()
    
    # Get project directories from search paths
    for search_path in "${PROJECT_SEARCH_PATHS[@]}"; do
        if [[ -d "$search_path" ]]; then
            while IFS= read -r -d '' dir; do
                local project_name=$(basename "$dir")
                projects+=("$project_name")
            done < <(find "$search_path" -maxdepth 1 -type d -not -name '.*' -print0 2>/dev/null)
        fi
    done
    
    # Add special options
    projects+=("--recent" "--list" "--help")
    
    # Filter completions
    COMPREPLY=($(compgen -W "${projects[*]}" -- "$cur"))
}

# --- MAIN FUNCTION ---

dev() {
    local arg="${1:-.}"
    
    # Show help
    if [[ "$arg" == "-h" ]] || [[ "$arg" == "--help" ]]; then
        _dev_help
        return 0
    fi
    
    # Show recent projects
    if [[ "$arg" == "--recent" ]]; then
        _dev_recent
        return $?
    fi
    
    # Show all projects
    if [[ "$arg" == "--list" ]]; then
        _dev_list
        return $?
    fi
    
    # Find and open project
    local project_path
    project_path=$(_find_project "$arg") || {
        echo "❌ Project not found: $arg"
        echo ""
        echo "Searched in:"
        for path in "${PROJECT_SEARCH_PATHS[@]}"; do
            echo "  • $path"
        done
        echo ""
        echo "Use 'dev --help' for more options"
        return 1
    }
    
    if [[ ! -d "$project_path" ]]; then
        echo "❌ Not a directory: $project_path"
        return 1
    fi
    
    # Launch with Python script
    python3 "$LAUNCHER_SCRIPT" "$project_path"
}

# Register tab completion for zsh
if [[ -n "${ZSH_VERSION:-}" ]]; then
    compctl -K _dev_completion dev
fi

# Register tab completion for bash
if [[ -n "${BASH_VERSION:-}" ]]; then
    complete -o bashdefault -o default -o nospace -F _dev_completion dev
fi

# Export the function
export -f dev