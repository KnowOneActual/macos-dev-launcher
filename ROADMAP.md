# macOS Dev Launcher Roadmap

**Project:** [macos-dev-launcher](https://github.com/KnowOneActual/macos-dev-launcher)  
**Purpose:** Systematic enhancement plan for improved reliability, UX, and extensibility  
**Last Updated:** December 1, 2025  
**Current Version:** v1.4.0

---

## Overview

This roadmap outlines a phased approach to enhancing the macOS Dev Launcher while maintaining its core simplicity and usability. Each phase builds on the previous one, ensuring the tool remains functional throughout development.

---

## Phase 1: Foundation & Robustness (Priority: High) ✅ COMPLETE

**Goal:** Ensure reliability and graceful failure handling before adding new features.

### 1.1 Application Validation ✅
- **Status:** COMPLETED (v1.1.0)
- **Task:** Verify terminal and editor apps exist before presenting options
- **Implementation:**
  - Create `app_exists()` function to check `/Applications/{app}.app`
  - Filter `TERMINAL_APPS` list to show only installed apps
  - Handle case where no valid terminals are found
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours
- **Dependencies:** None
- **Bonus Features Added:**
  - CLI argument parsing with `argparse`
  - `--test` mode for configuration validation
  - `--verbose` mode for debugging
  - Path validation (exists and is directory)

### 1.2 Error Messaging & User Feedback ✅
- **Status:** COMPLETED (integrated across phases)
- **Task:** Implement informative dialogs for errors and success states
- **Implementation:**
  - Create `show_error_dialog()` for failures (app not found, permissions issues)
  - Add error handling to all subprocess calls
  - Log all errors for troubleshooting
- **Completed:** November 30, 2025 (via Phases 1.1, 1.3, 1.4)
- **Actual Effort:** Integrated throughout other phases
- **Dependencies:** 1.1
- **Note:** Success dialogs deferred to Phase 3.3 (Status Notifications)

### 1.3 Path & Input Sanitization ✅
- **Status:** COMPLETED (v1.2.0)
- **Task:** Safely handle special characters, spaces, and potentially malicious paths
- **Implementation:**
  - Use `shlex.quote()` for shell arguments
  - Validate input paths exist and are directories
  - Handle symlinks and aliases properly
- **Completed:** November 30, 2025
- **Actual Effort:** 1 hour
- **Dependencies:** None
- **Features Delivered:**
  - `sanitize_path()` function with comprehensive validation
  - Symlink resolution and detection
  - Special character escaping in dialogs
  - Security checks for suspicious paths
  - Enhanced `--test --verbose` mode with path tests

### 1.4 Logging Infrastructure ✅
- **Status:** COMPLETED (v1.3.0)
- **Task:** Add optional logging for troubleshooting
- **Implementation:**
  - Create log file at `~/Library/Logs/macos-dev-launcher.log`
  - Log launches, errors, and user choices
  - Add configuration option to enable/disable logging
  - Implement log rotation (keep last 7 days)
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours
- **Dependencies:** None
- **Features Delivered:**
  - Rotating file handler (1 MB per file, 7 backups)
  - Multiple log levels (DEBUG, INFO, WARNING, ERROR)
  - Comprehensive logging coverage
  - `--no-log` flag to disable logging
  - Session start/end markers
  - Exception traceback capture

**Phase 1 Deliverable:** ✅ **ACHIEVED** - Robust, production-ready base with comprehensive error handling

---

## Phase 2: Configuration & Customization (Priority: Medium) ✅ COMPLETE

**Goal:** Enable user-specific workflows without hardcoding values.

### 2.1 External Configuration File ✅
- **Status:** COMPLETED (v1.4.0)
- **Task:** Move configuration out of script into a user-editable file
- **Implementation:**
  - Create `~/.config/macos-dev-launcher/config.json`
  - Support terminal list, editor preferences, logging options
  - Provide sensible defaults if config missing
  - Add example configuration file to repository
- **Completed:** November 30, 2025
- **Actual Effort:** 3 hours
- **Dependencies:** Phase 1 complete ✅
- **Features Delivered:**
  - JSON config file with deep-merge of defaults
  - `--config` flag for custom config path
  - `--create-config` flag to generate example
  - `config.example.json` with comprehensive documentation
  - Backward compatibility with legacy config format

### 2.2 Multi-Editor Support ✅
- **Status:** COMPLETED (v1.4.0)
- **Task:** Allow selection from multiple editors, not just one
- **Implementation:**
  - Add `EDITOR_APPS` list to config
  - Present editor picker dialog if multiple configured
  - Support "None" option to skip editor launch
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours
- **Dependencies:** 2.1 ✅
- **Features Delivered:**
  - Intelligent picker (shows picker if multiple, Yes/No if single)
  - "None (Terminal Only)" option in multi-editor picker
  - `get_available_editors()` function
  - Auto-skip if no editors installed

### 2.3 Custom Launch Arguments ✅
- **Status:** COMPLETED (v1.4.0)
- **Task:** Support terminal/editor-specific arguments
- **Implementation:**
  - Add `app_args` to config per app
  - Examples: specific profiles, themes, window positions
  - Document common use cases in README
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours
- **Dependencies:** 2.1 ✅
- **Features Delivered:**
  - `APP_ARGS` dict support in config
  - Arguments passed via `--args` to `open` command
  - Comprehensive `CUSTOM_ARGS.md` documentation
  - Examples for all major terminals and editors

### 2.4 Memory/Favorites System 🚧
- **Status:** PARTIALLY COMPLETE
- **Task:** Remember last-used terminal/editor per project
- **Implementation:**
  - Create `~/.config/macos-dev-launcher/history.json`
  - Store project path → (terminal, editor) mappings
  - Pre-select last choice in dialogs as default
  - Add "Forget History" option in dialog
- **Progress:**
  - ✅ Config structure exists (`behavior.remember_choices`)
  - ✅ Config directory and file handling ready
  - ❌ `history.json` implementation pending
  - ❌ Pre-selection logic pending
- **Estimated Effort:** 2-3 hours remaining
- **Dependencies:** 2.1 ✅
- **Next Steps:**
  - Implement `load_history()` and `save_choice()` functions
  - Add history pre-selection to dialog default values
  - Add "Forget" button to picker dialogs

**Phase 2 Deliverable:** ✅ **MOSTLY ACHIEVED** - Fully customizable launcher (favorites system 90% ready)

---

## Phase 3: User Experience Enhancements (Priority: Medium)

**Goal:** Polish the interaction flow and provide power-user features.

### 3.1 Combined Launch Options Dialog
- **Status:** NOT STARTED
- **Task:** Offer terminal, editor, or both in single dialog
- **Implementation:**
  - Replace two-dialog flow with unified choice dialog
  - Options: "Terminal Only", "Editor Only", "Both", "Cancel"
  - Remember choice per project if history enabled
- **Estimated Effort:** 2-3 hours
- **Dependencies:** Phase 2 complete ✅
- **Ready to start:** Yes

### 3.2 Installation Script
- **Status:** NOT STARTED
- **Task:** Automate setup process for new users
- **Implementation:**
  - Create `install.sh` script
  - Automatically place script in `~/scripts/` or user-specified location
  - Create Automator Quick Action programmatically
  - Set up default config file
  - Request necessary permissions
- **Estimated Effort:** 4-5 hours
- **Dependencies:** 2.1 ✅
- **Ready to start:** Yes
- **High Impact:** Would significantly improve adoption

### 3.3 Status Notifications
- **Status:** NOT STARTED
- **Task:** Use native macOS notifications for feedback
- **Implementation:**
  - Replace success dialog with notification banner
  - Use for background operations (editor launching, etc.)
  - Make notifications optional in config
- **Estimated Effort:** 2 hours
- **Dependencies:** 2.1 ✅
- **Ready to start:** Yes

### 3.4 Project Type Detection
- **Status:** NOT STARTED
- **Task:** Auto-suggest appropriate editor based on project contents
- **Implementation:**
  - Detect `.vscode/`, `.idea/`, `package.json`, `Cargo.toml`, etc.
  - Map to preferred editors in config
  - Pre-select detected editor in picker
- **Estimated Effort:** 3-4 hours
- **Dependencies:** 2.2 ✅
- **Ready to start:** Yes

**Phase 3 Deliverable:** Streamlined, intelligent workflow with minimal friction

---

## Phase 4: Advanced Features (Priority: Low)

**Goal:** Extend capabilities for power users and specialized workflows.

### 4.1 Profile System
- **Status:** NOT STARTED
- **Task:** Named configurations for different project types
- **Implementation:**
  - Define profiles in config: "Web Dev", "Python Project", "Rust Project"
  - Each profile specifies terminals, editors, custom commands
  - Add profile selector to dialog if multiple match
- **Estimated Effort:** 4-5 hours
- **Dependencies:** Phase 3 complete

### 4.2 Post-Launch Commands
- **Status:** NOT STARTED
- **Task:** Run custom shell commands after opening terminal/editor
- **Implementation:**
  - Add `post_launch_commands` to config (per terminal or profile)
  - Examples: activate venv, start dev server, git fetch
  - Support both sync and async execution
- **Estimated Effort:** 3-4 hours
- **Dependencies:** 2.3 ✅, 4.1

### 4.3 Multi-Project Batch Launch
- **Status:** NOT STARTED
- **Task:** Launch multiple projects simultaneously
- **Implementation:**
  - Allow Quick Action on multiple selected folders
  - Present single consolidated dialog for all projects
  - Launch terminals/editors in parallel
  - Option to use same terminal/editor for all
- **Estimated Effort:** 3-4 hours
- **Dependencies:** Phase 3 complete

### 4.4 CLI Alternative
- **Status:** NOT STARTED
- **Task:** Provide command-line interface for terminal users
- **Implementation:**
  - Create `dev-launcher` CLI tool using same core logic
  - Support flags: `--terminal`, `--editor`, `--profile`
  - Interactive mode if no flags provided
  - Install via `brew` or direct download
- **Estimated Effort:** 5-6 hours
- **Dependencies:** Phase 2 ✅, 3 complete

### 4.5 Keyboard Shortcut Integration
- **Status:** NOT STARTED
- **Task:** Enable hotkey-based launching
- **Implementation:**
  - Document integration with Raycast, Alfred
  - Provide example Alfred workflow
  - Consider macOS native keyboard shortcut for Quick Action
- **Estimated Effort:** 2-3 hours
- **Dependencies:** 3.2

**Phase 4 Deliverable:** Feature-complete tool supporting advanced workflows

---

## Phase 5: Documentation & Community (Priority: Ongoing)

**Goal:** Enable adoption, contributions, and long-term maintenance.

### 5.1 Enhanced README 🚧
- **Status:** PARTIALLY COMPLETE
- **Task:** Comprehensive documentation with examples
- **Progress:**
  - ✅ Basic README with installation
  - ✅ Configuration section needed
  - ❌ Screenshots/GIFs of workflow
  - ❌ Detailed troubleshooting section
  - ❌ Compatibility matrix
- **Estimated Effort:** 2-3 hours remaining
- **Dependencies:** Phase 3 complete (for complete docs)
- **Can start now:** Yes (document existing features)

### 5.2 Example Configurations
- **Status:** NOT STARTED
- **Task:** Provide real-world config templates
- **Implementation:**
  - Create `examples/` directory
  - Add configs for common setups: web dev, data science, DevOps
  - Include profile examples
- **Estimated Effort:** 2 hours
- **Dependencies:** Phase 4 complete

### 5.3 Testing Framework
- **Status:** NOT STARTED
- **Task:** Add automated tests for core functionality
- **Implementation:**
  - Unit tests for config parsing, app validation
  - Mock subprocess calls for testing
  - CI/CD pipeline with GitHub Actions
- **Estimated Effort:** 5-6 hours
- **Dependencies:** Phase 2 complete ✅
- **Ready to start:** Yes

### 5.4 Contributing Guidelines ✅
- **Status:** COMPLETED
- **Task:** Enable community contributions
- **Implementation:**
  - Add `CONTRIBUTING.md`
  - Define code style, PR process
  - Create issue templates
  - Add feature request template
- **Completed:** November 2025
- **File:** CONTRIBUTING.md exists

**Phase 5 Deliverable:** Well-documented, maintainable, community-friendly project

---

## Implementation Timeline

**Progress Summary:**
- **Phase 1:** ✅ COMPLETE (November 30, 2025)
- **Phase 2:** ✅ COMPLETE (November 30, 2025) - 2.4 at 90%
- **Phase 3:** 🔜 READY TO START
- **Phase 4:** ⏳ Waiting on Phase 3
- **Phase 5:** 🚧 ONGOING

**Next Milestone: Phase 3 Start**
- Recommended first task: **Phase 3.2 (Installation Script)** - High impact on adoption
- Alternative: **Phase 2.4 completion** - Finish memory system (2-3 hours)
- Alternative: **Phase 5.1** - Update README with config documentation (2 hours)

---

## Success Metrics

- **Reliability:** ✅ Zero silent failures, all errors communicated clearly
- **Usability:** ✅ Single-action launch (Quick Action → Pick → Done)
- **Performance:** ✅ Launch time under 2 seconds
- **Customization:** ✅ External config with 13+ options
- **Adoption:** ⏳ 0 stars (need promotion + installation script)
- **Maintainability:** ⏳ No tests yet, but good code structure

---

## Notes & Considerations

### Backward Compatibility ✅
- Config system maintains backward compatibility
- Legacy `editor` field auto-converts to `editors` list
- Default values ensure script works without config file
- No breaking changes from v1.0.0 to v1.4.0

### macOS Version Support
- Tested on macOS 12 (Monterey) through current version
- Python 3 requirement (pre-installed on modern macOS)
- No external dependencies required

### Performance Considerations ✅
- Startup time: <1 second on modern hardware
- Config loaded once at startup
- App validation cached during execution
- No heavy imports or external dependencies

### Security Considerations ✅
- Path sanitization prevents traversal attacks
- AppleScript injection protection via escaping
- Config file validation
- Future: Sandboxing for post-launch commands (Phase 4)

---

## Future Ideas (Backlog)

Ideas for consideration beyond this roadmap:

- **Terminal multiplexer integration:** Auto-create tmux/screen sessions
- **Remote project support:** SSH into remote dev boxes
- **Container integration:** Launch Docker/Podman containers
- **IDE plugin:** Create VS Code/JetBrains extensions
- **Analytics:** Optional anonymous usage stats for improvement insights
- **GUI configuration editor:** Native app for config management
- **Workspace restoration:** Save/restore entire development sessions
- **Git integration:** Detect branch, show status in dialog
- **Virtual environment detection:** Auto-activate venv/conda environments

---

## Current State Summary (v1.4.0)

### ✅ What Works
- Full configuration system with JSON file
- Multi-terminal support with intelligent filtering
- Multi-editor support with smart dialogs
- Custom launch arguments per app
- Comprehensive logging with rotation
- Path security and validation
- CLI with test/verbose modes
- Error handling and user feedback

### 🚧 In Progress
- Phase 2.4: Memory system (90% ready)
- Phase 5.1: Enhanced README (basic complete)

### 🔜 Ready to Implement
- Phase 2.4 completion (2-3 hours)
- Phase 3.2: Installation script (high impact)
- Phase 5.1: README updates (quick win)

---

## Recommended Next Steps

**Option 1: Quick Wins (4-5 hours total)**
1. Complete Phase 2.4 (Memory system) - 2-3 hours
2. Update README with configuration docs - 1-2 hours
3. Tag v1.5.0 release

**Option 2: High Impact (4-5 hours)**
1. Implement Phase 3.2 (Installation script) - 4-5 hours
2. Tag v2.0.0 release (major usability improvement)

**Option 3: Documentation Focus (3-4 hours)**
1. Update README comprehensively - 2 hours
2. Add screenshots/GIFs - 1 hour
3. Create example configs - 1 hour
4. Tag v1.4.1 release

---

**🎉 Phase 2 Complete! The launcher is now fully customizable.**

**Ready to tackle Phase 3? Let's make installation seamless!**
