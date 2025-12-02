# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Phase 2.4: Memory/Favorites system (history.json implementation)
- Phase 3.1: Combined launch options dialog
- Phase 3.2: Installation script

## [1.4.0] - 2025-11-30

### Added
- **Phase 2.1:** External configuration file support (`~/.config/macos-dev-launcher/config.json`)
- **Phase 2.2:** Multi-editor support with intelligent picker dialog
- **Phase 2.3:** Custom launch arguments per app via `app_args` config
- `--create-config` flag to generate example configuration file
- `--config` flag to specify custom config file location
- Backward compatibility for legacy single `editor` config (auto-converts to `editors` list)
- Comprehensive config validation in test mode

### Changed
- Converted from single `EDITOR_APP` to `EDITOR_APPS` list for multi-editor support
- Editor prompt now shows picker if multiple editors configured
- Editor prompt shows simple Yes/No dialog if only one editor configured
- Config values now deep-merge with defaults for better flexibility

### Documentation
- Added `config.example.json` with comprehensive examples and comments
- Added `CUSTOM_ARGS.md` guide for Phase 2.3 feature
- Updated ROADMAP to reflect Phase 2 completion

## [1.3.0] - 2025-11-30

### Added
- **Phase 1.4:** Comprehensive logging infrastructure
- Rotating log file handler (1MB per file, keeps 7 backups)
- Multiple log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- `--no-log` flag to disable file logging
- `--verbose` flag enables console logging at DEBUG level
- Session start/end markers in logs
- Exception traceback capture for debugging

### Changed
- Logger now configured via `setup_logging()` function
- Log directory created automatically at `~/Library/Logs/`
- Log configuration exposed in config file

## [1.2.0] - 2025-11-30

### Added
- **Phase 1.3:** Path sanitization and security validation
- `sanitize_path()` function with comprehensive checks
- Symlink detection and resolution
- Security warnings for paths outside user directory
- Special character escaping in AppleScript dialogs

### Enhanced
- `--test --verbose` mode now includes path sanitization tests
- Improved error messages with sanitized path information

### Security
- Added path validation (exists, is directory, security checks)
- Protection against malicious path traversal attempts

## [1.1.0] - 2025-11-30

### Added
- **Phase 1.1:** Application validation before showing in pickers
- `app_exists()` function to check `/Applications/{app}.app`
- `get_available_terminals()` and `get_available_editors()` filter functions
- CLI argument parsing with `argparse`
- `--test` mode for configuration validation without launching apps
- `--verbose` mode for debugging and detailed output
- Error dialogs for missing applications
- Path validation (exists and is directory)

### Changed
- Terminal picker now only shows installed applications
- Editor prompt skipped if no editors are installed
- Improved user feedback with native error dialogs

### Fixed
- Script no longer fails silently if configured apps are missing
- Better error handling for invalid paths

## [1.0.0] - 2025-11-20

### Added
- Initial release of the Dev Environment Launcher
- Core `open_dev_env.py` script with native macOS UI
- Interactive picker for terminal selection (Ghostty, Kitty, Warp, Wave)
- Optional editor integration (VS Codium)
- Automator Quick Action workflow
- Basic documentation (README, LICENSE, CONTRIBUTING)
- MIT License

### Features
- Right-click any folder in Finder to launch
- Native macOS dialogs (no external dependencies)
- Terminal opens directly to selected folder
- Editor launches with same folder context
- Zero configuration required for basic usage

---

## Version History Summary

- **v1.4.0** - Phase 2 complete (External config + multi-editor + custom args)
- **v1.3.0** - Phase 1.4 (Logging infrastructure)
- **v1.2.0** - Phase 1.3 (Path sanitization)
- **v1.1.0** - Phase 1.1 (App validation + CLI)
- **v1.0.0** - Initial release

## Migration Notes

### Upgrading from v1.0.0 to v1.4.0

Your script will continue to work with hardcoded values, but you can now:

1. **Create a config file** for customization:
   ```bash
   python3 ~/scripts/open_dev_env.py --create-config
   ```

2. **Edit config** at `~/.config/macos-dev-launcher/config.json`

3. **Test your setup**:
   ```bash
   python3 ~/scripts/open_dev_env.py --test --verbose
   ```

No breaking changes - all new features are opt-in via configuration file.
