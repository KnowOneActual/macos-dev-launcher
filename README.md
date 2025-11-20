![Language](https://img.shields.io/badge/Language-Python_3-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-macOS-000000?logo=apple&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

# macOS Dev Environment Launcher

A macOS Quick Action that streamlines your workflow startup. 
Instead of manually opening a terminal, navigating to a project, and then launching your editor, this script lets you right-click any project folder and ask: **"Which terminal should we use today?"**

## Features

* **Interactive Picker:** Uses a native macOS dialog to let you choose your terminal on the fly (e.g., Ghostty, Kitty, Warp, Wave).
* **Editor Integration:** Optionally launches your code editor (VS Codium, VS Code, etc.) alongside the terminal.
* **Context Aware:** Opens the terminal directly to the selected folder.

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
````

-----

## Installation

### 1\. Place the Script

Save `open_dev_env.py` to a permanent location (e.g., `~/scripts/`).

### 2\. Create the Quick Action

1.  Open **Automator** \> **New Quick Action**.
2.  Set **Workflow receives current** to `files or folders` in `Finder`.
3.  Add a **Run Shell Script** action.
4.  **Important:** Set "Pass input" to **as arguments**.
5.  Paste the command:
    ```bash
    /usr/bin/python3 "$HOME/scripts/open_dev_env.py" "$@"
    ```
6.  Save as "Open Dev Environment".

-----

## Usage

1.  Right-click a project folder in Finder.
2.  Select **Quick Actions \> Open Dev Environment**.
3.  Pick your terminal from the list.
4.  Click "Yes" to open your editor.

## License

MIT License.
