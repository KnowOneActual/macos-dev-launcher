![Language](https://img.shields.io/badge/Language-Python_3-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-macOS-000000?logo=apple&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

# macOS Dev Environment Launcher

A macOS Quick Action that streamlines your workflow startup. 
Instead of manually opening a terminal, navigating to a project, and then launching your editor, this script lets you right-click any project folder and ask: **"Which terminal should we use today?"**

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)

## Features

* **Interactive Picker:** Uses a native macOS dialog to let you choose your terminal on the fly (e.g., Ghostty, Kitty, Warp, Wave).
* **Editor Integration:** Optionally launches your code editor (VS Codium, VS Code, etc.) alongside the terminal.
* **Context Aware:** Opens the terminal directly to the selected folder.
* **Lightweight & Fast:** Minimal dependencies, launches in under 2 seconds.
* **Highly Customizable:** Easy to configure for your specific development environment.

---

## Installation

### Prerequisites

- macOS 12 (Monterey) or later
- Python 3 (pre-installed on macOS)
- Your preferred terminal emulator(s) installed in `/Applications`
- Your preferred code editor installed in `/Applications`

### 1. Place the Script

Save `open_dev_env.py` to a permanent location (e.g., `~/scripts/`).

```bash
mkdir -p ~/scripts
cd ~/scripts
# Download or copy open_dev_env.py here
```

### 2. Create the Quick Action

1.  Open **Automator** > **New Quick Action**.
2.  Set **Workflow receives current** to `files or folders` in `Finder`.
3.  Add a **Run Shell Script** action.
4.  **Important:** Set "Pass input" to **as arguments**.
5.  Paste the command:
    ```bash
    /usr/bin/python3 "$HOME/scripts/open_dev_env.py" "$@"
    ```
6.  Save as "Open Dev Environment".

### 3. Enable the Quick Action

The Quick Action should now appear in Finder's context menu under **Quick Actions** when you right-click a folder.

---

## Usage

1.  Right-click a project folder in Finder.
2.  Select **Quick Actions > Open Dev Environment**.
3.  Pick your terminal from the list.
4.  Click "Yes" to open your editor (or "No" to skip).

**That's it!** Your terminal and editor will launch in the selected directory.

---

## Configuration

The script is designed to be easily customized for your specific tools. 

1.  Open `open_dev_env.py`.
2.  Edit the `TERMINAL_APPS` list to match the exact names of the apps in your `/Applications` folder.
3.  Update `EDITOR_APP` to your preferred editor.

```python
# --- CONFIGURATION ---
TERMINAL_APPS = ["Ghostty", "Kitty", "Warp", "Wave"] 
EDITOR_APP = "VSCodium"
```

**Supported Terminal Emulators:**
- Ghostty
- Kitty
- Warp
- Wave
- iTerm2
- Alacritty
- Hyper
- Terminal (macOS default)
- Any app in `/Applications`

**Supported Editors:**
- VS Code
- VSCodium
- Sublime Text
- JetBrains IDEs (IntelliJ, PyCharm, WebStorm, etc.)
- Any app in `/Applications`

---

## Documentation

### Project Roadmap

Interested in upcoming features and improvements? Check out our detailed implementation plan:

📋 **[ROADMAP.md](ROADMAP.md)** - Multi-phase enhancement plan including:
- Advanced error handling and logging
- External configuration files
- Multi-editor support
- Project type detection
- Profile system for different workflows
- And much more!

### Troubleshooting

**Quick Action doesn't appear:**
- Ensure the Automator workflow is saved correctly
- Try restarting Finder: `killall Finder`
- Check System Settings > Privacy & Security > Automation

**Permission denied errors:**
- Verify the script has executable permissions: `chmod +x ~/scripts/open_dev_env.py`
- Check that Automator has necessary permissions in System Settings

**App not launching:**
- Verify the app name in `TERMINAL_APPS` or `EDITOR_APP` matches exactly with the name in `/Applications`
- App names are case-sensitive (e.g., "VSCodium" not "vscodium")

---

## Contributing

Contributions are welcome! Whether it's:

- 🐛 Bug reports
- 💡 Feature requests  
- 📝 Documentation improvements
- 🔧 Code contributions

Please feel free to open an issue or submit a pull request.

### Development

Interested in contributing? See our [ROADMAP.md](ROADMAP.md) for planned features and implementation priorities.

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built with ❤️ for developers who value efficient workflows.

**Star this repo** if you find it useful! ⭐
