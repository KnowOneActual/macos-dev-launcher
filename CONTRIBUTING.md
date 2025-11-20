# Contributing to Dev Environment Launcher

Thanks for checking out this project! 🚀

This tool is designed to be a simple, hackable way to manage dev environments on macOS. Whether you want to add support for more terminals or improve the Python logic, your help is welcome.

## How to Contribute

### 1. Reporting Bugs
If the script fails to open your terminal or crashes:
* **Check your config:** Ensure the app names in `TERMINAL_APPS` match exactly what is in your `/Applications` folder.
* **Open an Issue:** Tell us which OS version you are on and which terminal you were trying to launch.

### 2. Suggesting Features
Want to add a "Open in Browser" option? Or maybe support for iTerm profiles?
* Open a **Feature Request** issue.
* Explain how you would use it in your daily workflow.

### 3. Submitting Pull Requests
1.  **Fork** the repository.
2.  **Clone** your fork locally.
3.  **Create a branch** (e.g., `feat-add-alacritty` or `fix-path-spaces`).
4.  **Test your changes** (see below).
5.  **Push** to your fork and open a **Pull Request**.

---

## Development & Testing

### macOS Requirement
This script relies heavily on `osascript` to display native dialogs. **It will only run on macOS.**

### Testing the Script
You don't need to create a Quick Action every time you change code. You can run it directly from your terminal:

1.  Open your current terminal.
2.  Run the script against a dummy folder:
    ```bash
    # Replace with your actual path
    python3 open_dev_env.py "/Users/you/code/my-test-project"
    ```
3.  **Verify:**
    * Did the popup appear?
    * Did the selected terminal open?
    * Did it `cd` into the correct folder?

---

## Style Guidelines

* **Python:** We follow standard PEP 8 style.
* **Config:** If you add new default apps, please keep them sorted alphabetically in the `TERMINAL_APPS` list.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.