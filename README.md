# macOS Dev Environment Launcher

![Language](https://img.shields.io/badge/Language-Python_3-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-macOS-000000?logo=apple&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0.0-blue)

# I'm currently working on refactoring, and I'll be updating it frequently over the next several weeks. Thanks for your patience!

A macOS Quick Action that streamlines your workflow startup. 
Instead of manually opening a terminal, navigating to a project, and then launching your editor, this script lets you right-click any project folder and ask: **"Which terminal should we use today?"**

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
  - [Quick Start](#quick-start)
  - [Configuration Options](#configuration-options)
  - [Custom Launch Arguments](#custom-launch-arguments)
  - [Examples](#configuration-examples)
- [CLI Usage](#cli-usage)
- [Documentation](#documentation)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features

* **Interactive Picker:** Uses native macOS dialogs to choose your terminal on the fly
* **Multi-Editor Support:** Configure multiple editors and pick the right one for each project
* **Custom Launch Arguments:** Pass specific flags to your terminals and editors
* **External Configuration:** JSON config file for easy customization without editing code
* **Memory System:** Remembers your terminal/editor choices per project
* **Context Aware:** Opens the terminal directly to the selected folder
* **Comprehensive Logging:** Optional rotating logs for troubleshooting
* **Lightweight & Fast:** Zero dependencies, launches in under 2 seconds
* **Highly Customizable:** 13+ configuration options to match your workflow

### Phase 3.1 - Combined Dialog (NEW!)
- **Two-dialog workflow**: Pick terminal → pick editor → both launch
- Optional combined mode via `combined_dialog: true` in config
- Faster workflow when both apps needed
- Maintains full backward compatibility

## Quick Start

**Add to `~/.zshrc`:**

```bash
dev() {
    python3 "$HOME/github_repo/macos-dev-launcher/open_dev_env.py" "${1:-.}"
}
```

**Reload:**
```bash
source ~/.zshrc
```

**Use:**
```bash
dev .                    # Current directory
dev my-project           # Searches common paths
dev ~/full/path/project  # Full path
```

---

## What It Does

When you run `dev`, it:
1. Opens your terminal in the project directory
2. Asks which terminal you want (Ghostty, Kitty, Warp, etc.)
3. Asks which editor you want (VSCodium, etc.)
4. Remembers your choices for next time

## Installation

### Repo Setup
```bash
git clone https://github.com/KnowOneActual/macos-dev-launcher.git ~/github_repo/macos-dev-launcher
cd ~/github_repo/macos-dev-launcher
python3 open_dev_env.py --create-config
```

### Shell Integration
Add this to `~/.zshrc` or `~/.bash_profile`:

```bash
dev() {
    python3 "$HOME/github_repo/macos-dev-launcher/open_dev_env.py" "${1:-.}"
}
```

Then reload:
```bash
source ~/.zshrc
```

---

## Usage

### Open current directory
```bash
dev .
```

### Open by project name (searches common paths)
```bash
dev my-project
```
Searches in: `~/github_repo`, `~/projects`, `~/work`, `~/dev`, `~/src`

### Open with full path
```bash
dev ~/any/path/to/project
```

### Test installation
```bash
python3 open_dev_env.py --test
```

---

## Configuration

Edit `~/.config/macos-dev-launcher/config.json`:

```json
{
  "terminals": ["Ghostty", "Kitty", "Warp", "Wave"],
  "editors": ["VSCodium"],
  "behavior": {
    "auto_open_editor": true,
    "remember_choices": true,
    "combined_dialog": true
  },
  "logging": {
    "enabled": true,
    "level": "INFO",
    "file": "~/Library/Logs/macos-dev-launcher.log"
  }
}
```

### Options

| Setting | Default | What it does |
|---------|---------|--------------|
| `terminals` | List of apps | Terminal apps to choose from |
| `editors` | ["VSCodium"] | Editor apps to choose from |
| `auto_open_editor` | true | Open editor after terminal |
| `remember_choices` | false | Save your terminal/editor choice per project |
| `combined_dialog` | true | Single dialog for both selections |
| `logging.enabled` | true | Log to file |

---

## Features

✅ **Smart app detection** - Only shows installed apps
✅ **Project memory** - Remembers your last choices
✅ **Combined dialog** - One screen for terminal + editor
✅ **Validation** - Checks paths and apps before launching
✅ **Logging** - Tracks what happens
✅ **Config file** - Customize everything
✅ **Error handling** - Clear messages if something goes wrong

---

## Examples

### Setup for GitHub projects
Assuming projects are in `~/github_repo/`:

```bash
dev my-web-app       # Opens ~/github_repo/my-web-app
dev .                # Opens current directory
```

### With custom search paths
Edit your shell config to add more search directories:

```bash
dev() {
    # Add your custom paths here by editing the Python script
    python3 "$HOME/github_repo/macos-dev-launcher/open_dev_env.py" "${1:-.}"
}
```

Or create a custom config at `~/.config/macos-dev-launcher/config.json`.

### Remember choices per project
Enable in config:

```json
{
  "behavior": {
    "remember_choices": true
  }
}
```

Now when you open a project, next time it remembers if you chose Ghostty + VSCodium.

---

## How It Works

1. **You run:** `dev my-project`
2. **Script finds:** `~/github_repo/my-project`
3. **Dialog appears:** Pick terminal (Ghostty, Kitty, Warp?)
4. **Dialog appears:** Pick editor (VSCodium, none, other?)
5. **Terminal opens:** At project directory
6. **Editor opens:** (if you chose one)
7. **Saved:** Your choices for next time (if enabled)

---

## Troubleshooting

### `dev: command not found`
Make sure you added the function to `~/.zshrc` and ran `source ~/.zshrc`.

### `python3: can't open file`
Check that the repo is at `~/github_repo/macos-dev-launcher` and the file exists there.

### Project not found
Make sure project is in one of these directories:
- `~/github_repo/`
- `~/projects/`
- `~/work/`
- `~/dev/`
- `~/src/`

Or use the full path: `dev ~/any/path/to/project`

### No terminals showing
Install one of these:
- [Ghostty](https://ghostty.org)
- [Kitty](https://sw.kovidgoyal.net/kitty/)
- [Warp](https://www.warp.dev)
- [Wave](https://www.waveterm.dev)

---

## Phases

**Phase 1:** Path validation, app checking, error handling
**Phase 2:** Config files, project memory, logging
**Phase 3.1:** Combined dialog for terminal + editor
**Phase 4:** Simple shell command `dev`

---

## Requirements

- macOS 10.14+
- Python 3.7+
- At least one terminal app installed
- (Optional) An editor app

---

## License

MIT

---

## Contributing

Found a bug? Have an idea? Open an issue on GitHub.

---

**That's it. Simple, clean, ready to use.** ⚡
