# macOS Dev Environment Launcher

![Language](https://img.shields.io/badge/Language-Python_3-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-macOS-000000?logo=apple&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-2.0.0-blue)

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

---

## Installation

### One-Command Script Install (Recommended)

```bash
# Install script and config only
curl -fsSL https://raw.githubusercontent.com/KnowOneActual/macos-dev-launcher/main/install.sh | bash
```

Or clone and install:
```bash
git clone https://github.com/KnowOneActual/macos-dev-launcher.git
cd macos-dev-launcher
./install.sh
```

This installs:
- ✅ Script: `~/scripts/open_dev_env.py`
- ✅ Config: `~/.config/macos-dev-launcher/config.json`
- ✅ Ready to use with manual Quick Action setup below

**After install:**
```bash
killall Finder  # Refresh Finder menu
python3 ~/scripts/open_dev_env.py --test  # Verify installation
```

### Manual Quick Action Setup

1. Open **Automator** (Spotlight: `Cmd+Space` → "Automator")

2. **New Document** → **Quick Action** → **Choose**

3. Set top options:
   ```
   Workflow receives current: folders
   in: Finder
   ```

4. Add **Run Shell Script** action:
   - Shell: `/bin/bash`
   - Pass input: `as arguments`

5. Paste this exact script:
   ```bash
   /usr/bin/python3 "$HOME/scripts/open_dev_env.py" "$@"
   ```

6. **File** → **Save** → Name: `Open Dev Environment`

7. **Done!** Right-click folders → **Quick Actions** → **Open Dev Environment**

### Uninstall

```bash
curl -fsSL https://raw.githubusercontent.com/KnowOneActual/macos-dev-launcher/main/install.sh | bash -s -- --uninstall
```

---

## Usage

### Via Finder (Quick Action)

1. Right-click a project folder in Finder
2. Select **Quick Actions > Open Dev Environment**
3. Pick your terminal from the list (remembers your last choice!)
4. Choose your editor (or skip)

**That's it!** Your terminal and editor will launch in the selected directory.

### Via Command Line

You can also launch directly from the terminal:

```bash
# Launch with picker dialogs
python3 ~/scripts/open_dev_env.py ~/projects/my-app

# Test configuration
python3 ~/scripts/open_dev_env.py --test

# Verbose mode for debugging
python3 ~/scripts/open_dev_env.py --verbose ~/projects/my-app

# Use custom config file
python3 ~/scripts/open_dev_env.py --config ~/my-config.json ~/projects/my-app
```

---

## Configuration

### Quick Start

Create your configuration file:

```bash
python3 ~/scripts/open_dev_env.py --create-config
```

This creates `~/.config/macos-dev-launcher/config.json` with sensible defaults.

**Edit your config:**
```bash
open ~/.config/macos-dev-launcher/config.json
```

### Configuration Options

The config file supports the following options:

#### Terminals and Editors

```json
{
  "terminals": [
    "Ghostty",
    "Kitty",
    "Warp",
    "Wave",
    "iTerm",
    "Alacritty",
    "Terminal"
  ],
  "editors": [
    "VSCodium",
    "Visual Studio Code",
    "Cursor",
    "Zed"
  ]
}
```

#### Custom Launch Arguments

```json
{
  "app_args": {
    "Warp": ["--profile", "Work"],
    "iTerm": ["--fullscreen"],
    "VSCodium": ["--new-window"],
    "Visual Studio Code": ["--new-window", "--disable-extensions"]
  }
}
```

#### Memory & Behavior

```json
{
  "remember_choices": true,
  "auto_open_editor": true
}
```

#### Logging Configuration

```json
{
  "logging": {
    "enabled": true,
    "level": "INFO",
    "file": "~/Library/Logs/macos-dev-launcher.log",
    "max_bytes": 1048576,
    "backup_count": 7
  }
}
```

**Full example configs in `config.example.json`**

---

## CLI Usage

```bash
# Launch with dialogs
python3 open_dev_env.py ~/projects/my-app

# Test configuration (no apps launched)
python3 open_dev_env.py --test

# Verbose output for debugging
python3 open_dev_env.py --test --verbose

# Disable logging for this run
python3 open_dev_env.py --no-log ~/projects/my-app

# Create example config file
python3 open_dev_env.py --create-config
```

---

## Documentation

- 📋 [ROADMAP.md](ROADMAP.md) - Development roadmap
- 🎨 [CUSTOM_ARGS.md](CUSTOM_ARGS.md) - Custom launch arguments
- 📜 [CHANGELOG.md](CHANGELOG.md) - Version history
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines

**Current:** v2.0.0 (Phase 1+2+Memory System Complete)

---

## Troubleshooting

**Quick Action doesn't appear:**
```bash
killall Finder
```

**App not launching:**
```bash
python3 ~/scripts/open_dev_env.py --test --verbose
```

**Config issues:**
```bash
python3 -m json.tool ~/.config/macos-dev-launcher/config.json
```

---

## Supported Applications

**Terminals:** Ghostty, Kitty, Warp, Wave, iTerm2, Alacritty, Terminal
**Editors:** VS Code, VSCodium, Cursor, Zed, JetBrains IDEs

**Any app in `/Applications` works!**

---

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](LICENSE).

---

**⭐ Star this repo if useful!**