# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0]

### Added
- **start-project.sh**: Added support for command-line arguments (e.g., `./start-project.sh my-app`) to skip the initial prompt.
- **start-project.sh**: Added safety checks to prevent overwriting existing directories and using invalid characters in project names.
- **start-project.sh**: Added a `download_file` helper function to streamline external file fetching.
- **start-work.sh**: Added an "auto-stash" feature to safely save uncommitted changes instead of exiting.
- **start-work.sh**: Added a branch type selection menu (Feature, Bugfix, Hotfix) for standardized naming.
- **.prettierrc**: Added `endOfLine: lf` to strictly enforce Linux line endings.

### Changed
- **start-project.sh**: Improved `git init` logic to support older Git versions that don't recognize the `-b` flag.
- **README.md**: Removed the "instructions currently in development" warning.

### Fixed
- **start-project.sh**: Fixed a syntax error in the `.prettierignore` download command.
- **.prettierrc**: Resolved merge conflicts and restored valid JSON formatting.
