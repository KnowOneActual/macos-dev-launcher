# Contributing to Project Starter Script

First off, thanks for taking the time to contribute! 🚀

We want to make this tool the best way to kickstart new projects, and your help is welcome—whether it's fixing a bug in the Bash logic or improving the boilerplate templates.

## How to Contribute

### Reporting Bugs
If the script crashes, misbehaves, or creates a weird directory structure, please [open an issue](https://github.com/KnowOneActual/Project_Starter_Script/issues/new?template=bug_report.md).
* Check if the issue already exists.
* Use the **Bug Report** template to provide details (OS, Bash version, etc.).

### Requesting Features
Have an idea for a new language template or a workflow improvement?
* Open a **Feature Request** ticket.
* Describe *why* this feature would be useful to the broader community.

### Submitting Changes (Pull Requests)

1.  **Fork the Repo**: Click the "Fork" button in the top right corner of this page.
2.  **Clone your Fork**:
    ```bash
    git clone [https://github.com/YOUR-USERNAME/Project_Starter_Script.git](https://github.com/YOUR-USERNAME/Project_Starter_Script.git)
    cd Project_Starter_Script
    ```
3.  **Create a Branch**:
    ```bash
    # Use a descriptive name
    git checkout -b fix-git-init-logic
    ```
4.  **Make your Changes**: Edit the script or the boilerplate files.
5.  **Test Your Changes**: (See the "Testing" section below).
6.  **Push and PR**: Push your branch to your fork and open a Pull Request against our `main` branch. Please fill out the [PR Template](.github/PULL_REQUEST_TEMPLATE.md) completely.

---

## Development & Testing

### Testing the Script Logic
If you are modifying `start-project.sh`, you should test it by running it against a dummy folder.

```bash
# Make sure it's executable
chmod +x start-project.sh

# Run it with a test name
./start-project.sh test-project-01
````

### Testing Boilerplate Downloads (Important\!)

The script uses `curl` to fetch boilerplate files (like `.editorconfig` or `LICENSE`) directly from the **main** branch of this repository.

**If you modify a boilerplate file**, the script *will not* see your changes locally because it is still fetching the old version from the live URL.

To test changes to downloaded files:

1.  Edit `start-project.sh`.
2.  Temporarily change the `BASE_URL` variable or the specific `download_file` line to point to your local file path or your fork's raw URL.
3.  **Do not commit this change.** Please revert the URL change before submitting your PR.

## Style Guidelines

### Bash Scripting

We aim for clean, safe, and portable Bash code.

  * **ShellCheck**: We recommend running your code through [ShellCheck](https://www.shellcheck.net/) to catch common errors.
  * **Indentation**: Use 4 spaces for indentation.
  * **Comments**: Comment complex logic, especially regex or API calls.

### Markdown & Text

  * This project uses **Prettier** for formatting.
  * Refer to `.prettierrc` for the specific configuration (Space indentation, `lf` line endings).

## License

By contributing to Project Starter Script, you agree that your contributions will be licensed under its MIT License.

```
```
