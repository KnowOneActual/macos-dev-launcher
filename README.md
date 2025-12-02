![Language](https://img.shields.io/badge/Language-Python_3-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-macOS-000000?logo=apple&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-1.4.0-blue)

# macOS Dev Environment Launcher

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
* **Context Aware:** Opens the terminal directly to the selected folder
* **Comprehensive Logging:** Optional rotating logs for troubleshooting
* **Lightweight & Fast:** Zero dependencies, launches in under 2 seconds
* **Highly Customizable:** 13+ configuration options to match your workflow

---

## Installation

### Prerequisites

- macOS 12 (Monterey) or later
- Python 3 (pre-installed on macOS)
- Your preferred terminal emulator(s) installed in `/Applications`
- Your preferred code editor(s) installed in `/Applications`

### 1. Place the Script

Save `open_dev_env.py` to a permanent location (e.g., `~/scripts/`).

```bash
mkdir -p ~/scripts
cd ~/scripts
# Download or copy open_dev_env.py here
chmod +x open_dev_env.py
```

### 2. Create the Quick Action

1.  Open **Automator** > **New Quick Action**
2.  Set **Workflow receives current** to `files or folders` in `Finder`
3.  Add a **Run Shell Script** action
4.  **Important:** Set "Pass input" to **as arguments**
5.  Paste the command:
    ```bash
    /usr/bin/python3 "$HOME/scripts/open_dev_env.py" "$@"
    ```
6.  Save as "Open Dev Environment"

### 3. Test Your Setup

Validate your configuration:

```bash
python3 ~/scripts/open_dev_env.py --test --verbose
```

This will show which terminals and editors are available and verify your setup.

---

## Usage

### Via Finder (Quick Action)

1.  Right-click a project folder in Finder
2.  Select **Quick Actions > Open Dev Environment**
3.  Pick your terminal from the list
4.  Choose your editor (or skip)

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

Or use your favorite editor:

```bash
code ~/.config/macos-dev-launcher/config.json
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

- **terminals**: List of terminal apps (in order of preference)
- **editors**: List of editor apps
  - Single editor: Shows Yes/No dialog
  - Multiple editors: Shows picker dialog
  - Empty list `[]`: Disables editor prompts

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

See [CUSTOM_ARGS.md](CUSTOM_ARGS.md) for detailed examples.

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

- **enabled**: Enable/disable file logging
- **level**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **file**: Log file path (tilde `~` expands to home)
- **max_bytes**: Max log size before rotation (default: 1 MB)
- **backup_count**: Number of backup logs to keep (default: 7)

#### Behavior Settings

```json
{
  "behavior": {
    "auto_open_editor": true,
    "remember_choices": false
  }
}
```

- **auto_open_editor**: Show editor prompt after terminal selection
- **remember_choices**: Remember last choice per project *(coming in v1.5.0)*

### Custom Launch Arguments

Pass specific flags to your applications:

**Terminal Examples:**

```json
"app_args": {
  "Warp": ["--profile", "Development"],
  "Kitty": ["--session", "dev-session"],
  "iTerm": ["--fullscreen"],
  "Alacritty": ["--config-file", "/path/to/config.yml"]
}
```

**Editor Examples:**

```json
"app_args": {
  "VSCodium": ["--new-window"],
  "Visual Studio Code": ["--new-window", "--disable-extensions"],
  "Cursor": ["--new-window"],
  "Zed": ["--new"]
}
```

📖 **Full Documentation:** [CUSTOM_ARGS.md](CUSTOM_ARGS.md)

### Configuration Examples

**Minimal Config (Web Developer):**

```json
{
  "terminals": ["Warp", "iTerm"],
  "editors": ["VSCodium"],
  "app_args": {
    "Warp": ["--profile", "WebDev"]
  }
}
```

**Multi-Editor Setup (Full Stack):**

```json
{
  "terminals": ["Ghostty", "Kitty", "Warp"],
  "editors": ["VSCodium", "Cursor", "Zed"],
  "app_args": {
    "VSCodium": ["--new-window"],
    "Cursor": ["--new-window"]
  },
  "behavior": {
    "auto_open_editor": true
  }
}
```

**Terminal Only (No Editor):**

```json
{
  "terminals": ["Kitty", "Alacritty"],
  "editors": [],
  "behavior": {
    "auto_open_editor": false
  }
}
```

**Debug Mode:**

```json
{
  "terminals": ["Ghostty"],
  "editors": ["VSCodium"],
  "logging": {
    "enabled": true,
    "level": "DEBUG"
  }
}
```

---

## CLI Usage

The launcher includes a powerful command-line interface:

```bash
# Launch with dialogs
python3 open_dev_env.py ~/projects/my-app

# Test configuration (no apps launched)
python3 open_dev_env.py --test

# Verbose output for debugging
python3 open_dev_env.py --verbose ~/projects/my-app

# Test with verbose output
python3 open_dev_env.py --test --verbose

# Disable logging for this run
python3 open_dev_env.py --no-log ~/projects/my-app

# Use custom config file
python3 open_dev_env.py --config ~/custom-config.json ~/projects/my-app

# Create example config file
python3 open_dev_env.py --create-config
```

### CLI Flags

- `--test` - Validate configuration without launching apps
- `--verbose` - Enable detailed debug output
- `--no-log` - Disable file logging for this run
- `--config PATH` - Use custom config file
- `--create-config` - Generate example config at default location

---

## Documentation

### Additional Guides

- 📋 **[ROADMAP.md](ROADMAP.md)** - Development roadmap and upcoming features
- 🎨 **[CUSTOM_ARGS.md](CUSTOM_ARGS.md)** - Custom launch arguments guide
- 📜 **[CHANGELOG.md](CHANGELOG.md)** - Version history and release notes
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines

### Version History

**Current:** v1.4.0 (Phase 2 Complete)

- **v1.4.0** - External config + multi-editor + custom arguments
- **v1.3.0** - Comprehensive logging infrastructure
- **v1.2.0** - Path sanitization and security
- **v1.1.0** - App validation and CLI interface
- **v1.0.0** - Initial release

See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

---

## Troubleshooting

### Quick Action Issues

**Quick Action doesn't appear:**
- Ensure Automator workflow is saved correctly
- Restart Finder: `killall Finder`
- Check **System Settings > Privacy & Security > Automation**

**Permission denied errors:**
- Make script executable: `chmod +x ~/scripts/open_dev_env.py`
- Check Automator permissions in System Settings

### Application Issues

**App not launching:**

1. **Verify app name matches exactly** (case-sensitive):
   ```bash
   ls /Applications/ | grep -i "your-app"
   ```

2. **Test configuration:**
   ```bash
   python3 ~/scripts/open_dev_env.py --test --verbose
   ```

3. **Check logs** (if logging enabled):
   ```bash
   tail -f ~/Library/Logs/macos-dev-launcher.log
   ```

**No terminals/editors shown:**
- Install at least one terminal from the configured list
- Run `--test` to see which apps are detected
- Edit `~/.config/macos-dev-launcher/config.json` to add your apps

### Configuration Issues

**Config file not found:**
- Create config: `python3 open_dev_env.py --create-config`
- Script works without config (uses defaults)

**Custom arguments not working:**
- Verify app name matches exactly (case-sensitive)
- Check if app supports those flags
- Test manually: `open -a "AppName" /path/to/project --args --your-flag`
- See [CUSTOM_ARGS.md](CUSTOM_ARGS.md) for troubleshooting

**JSON syntax errors:**
- Validate JSON: Use an online validator or:
  ```bash
  python3 -m json.tool ~/.config/macos-dev-launcher/config.json
  ```

### Getting Help

1. **Run test mode:**
   ```bash
   python3 ~/scripts/open_dev_env.py --test --verbose
   ```

2. **Check logs:**
   ```bash
   cat ~/Library/Logs/macos-dev-launcher.log
   ```

3. **Open an issue:** [GitHub Issues](https://github.com/KnowOneActual/macos-dev-launcher/issues)

---

## Supported Applications

### Terminals
- ✅ Ghostty
- ✅ Kitty
- ✅ Warp
- ✅ Wave
- ✅ iTerm2
- ✅ Alacritty
- ✅ Hyper
- ✅ Terminal (macOS default)
- ✅ Any app in `/Applications`

### Editors
- ✅ VS Code
- ✅ VSCodium
- ✅ Cursor
- ✅ Zed
- ✅ Sublime Text
- ✅ JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)
- ✅ Any app in `/Applications`

**Don't see your app?** Just add it to the config file!

---

## Contributing

Contributions are welcome! Whether it's:

- 🐛 Bug reports
- 💡 Feature requests  
- 📝 Documentation improvements
- 🔧 Code contributions

Please feel free to open an issue or submit a pull request.

### Development

Interested in contributing? See our [ROADMAP.md](ROADMAP.md) for planned features and [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built with ❤️ for developers who value efficient workflows.

**Star this repo** if you find it useful! ⭐

---

## What's Next?

Check out our [ROADMAP.md](ROADMAP.md) for upcoming features:

- 🎯 **Phase 2.4:** Memory system (remember choices per project)
- 🚀 **Phase 3.2:** Installation script (automated setup)
- 📊 **Phase 3.4:** Project type detection (auto-suggest editor)
- 🎨 **Phase 4.1:** Profile system (project-specific configs)

Want a feature? [Open an issue](https://github.com/KnowOneActual/macos-dev-launcher/issues) or contribute!
