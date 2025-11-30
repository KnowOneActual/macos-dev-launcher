# macOS Dev Launcher Roadmap

**Project:** [macos-dev-launcher](https://github.com/KnowOneActual/macos-dev-launcher)  
**Purpose:** Systematic enhancement plan for improved reliability, UX, and extensibility  
**Last Updated:** November 30, 2025

---

## Overview

This roadmap outlines a phased approach to enhancing the macOS Dev Launcher while maintaining its core simplicity and usability. Each phase builds on the previous one, ensuring the tool remains functional throughout development.

---

## Phase 1: Foundation & Robustness (Priority: High)

**Goal:** Ensure reliability and graceful failure handling before adding new features.

### 1.1 Application Validation
- **Task:** Verify terminal and editor apps exist before presenting options
- **Implementation:**
  - Create `app_exists()` function to check `/Applications/{app}.app`
  - Filter `TERMINAL_APPS` list to show only installed apps
  - Handle case where no valid terminals are found
- **Estimated Effort:** 2-3 hours
- **Dependencies:** None

### 1.2 Error Messaging & User Feedback
- **Task:** Implement informative dialogs for errors and success states
- **Implementation:**
  - Create `show_error_dialog()` for failures (app not found, permissions issues)
  - Create `show_success_dialog()` for successful launches
  - Add error handling to all subprocess calls
- **Estimated Effort:** 2-3 hours
- **Dependencies:** 1.1

### 1.3 Path & Input Sanitization
- **Task:** Safely handle special characters, spaces, and potentially malicious paths
- **Implementation:**
  - Use `shlex.quote()` for shell arguments
  - Validate input paths exist and are directories
  - Handle symlinks and aliases properly
- **Estimated Effort:** 1-2 hours
- **Dependencies:** None

### 1.4 Logging Infrastructure
- **Task:** Add optional logging for troubleshooting
- **Implementation:**
  - Create log file at `~/Library/Logs/macos-dev-launcher.log`
  - Log launches, errors, and user choices
  - Add configuration option to enable/disable logging
  - Implement log rotation (keep last 7 days)
- **Estimated Effort:** 2-3 hours
- **Dependencies:** None

**Phase 1 Deliverable:** Robust, production-ready base with comprehensive error handling

---

## Phase 2: Configuration & Customization (Priority: Medium)

**Goal:** Enable user-specific workflows without hardcoding values.

### 2.1 External Configuration File
- **Task:** Move configuration out of script into a user-editable file
- **Implementation:**
  - Create `~/.config/macos-dev-launcher/config.json`
  - Support terminal list, editor preferences, logging options
  - Provide sensible defaults if config missing
  - Add example configuration file to repository
- **Estimated Effort:** 3-4 hours
- **Dependencies:** Phase 1 complete

### 2.2 Multi-Editor Support
- **Task:** Allow selection from multiple editors, not just one
- **Implementation:**
  - Add `EDITOR_APPS` list to config
  - Present editor picker dialog if multiple configured
  - Support "None" option to skip editor launch
- **Estimated Effort:** 2-3 hours
- **Dependencies:** 2.1

### 2.3 Custom Launch Arguments
- **Task:** Support terminal/editor-specific arguments
- **Implementation:**
  - Add `terminal_args` and `editor_args` to config per app
  - Examples: specific profiles, themes, window positions
  - Document common use cases in README
- **Estimated Effort:** 2-3 hours
- **Dependencies:** 2.1

### 2.4 Memory/Favorites System
- **Task:** Remember last-used terminal/editor per project
- **Implementation:**
  - Create `~/.config/macos-dev-launcher/history.json`
  - Store project path → (terminal, editor) mappings
  - Pre-select last choice in dialogs as default
  - Add "Forget History" option in dialog
- **Estimated Effort:** 3-4 hours
- **Dependencies:** 2.1

**Phase 2 Deliverable:** Fully customizable launcher with persistent preferences

---

## Phase 3: User Experience Enhancements (Priority: Medium)

**Goal:** Polish the interaction flow and provide power-user features.

### 3.1 Combined Launch Options Dialog
- **Task:** Offer terminal, editor, or both in single dialog
- **Implementation:**
  - Replace two-dialog flow with unified choice dialog
  - Options: "Terminal Only", "Editor Only", "Both", "Cancel"
  - Remember choice per project if history enabled
- **Estimated Effort:** 2-3 hours
- **Dependencies:** Phase 2 complete

### 3.2 Installation Script
- **Task:** Automate setup process for new users
- **Implementation:**
  - Create `install.sh` script
  - Automatically place script in `~/scripts/` or user-specified location
  - Create Automator Quick Action programmatically
  - Set up default config file
  - Request necessary permissions
- **Estimated Effort:** 4-5 hours
- **Dependencies:** 2.1

### 3.3 Status Notifications
- **Task:** Use native macOS notifications for feedback
- **Implementation:**
  - Replace success dialog with notification banner
  - Use for background operations (editor launching, etc.)
  - Make notifications optional in config
- **Estimated Effort:** 2 hours
- **Dependencies:** 2.1

### 3.4 Project Type Detection
- **Task:** Auto-suggest appropriate editor based on project contents
- **Implementation:**
  - Detect `.vscode/`, `.idea/`, `package.json`, `Cargo.toml`, etc.
  - Map to preferred editors in config
  - Pre-select detected editor in picker
- **Estimated Effort:** 3-4 hours
- **Dependencies:** 2.2

**Phase 3 Deliverable:** Streamlined, intelligent workflow with minimal friction

---

## Phase 4: Advanced Features (Priority: Low)

**Goal:** Extend capabilities for power users and specialized workflows.

### 4.1 Profile System
- **Task:** Named configurations for different project types
- **Implementation:**
  - Define profiles in config: "Web Dev", "Python Project", "Rust Project"
  - Each profile specifies terminals, editors, custom commands
  - Add profile selector to dialog if multiple match
- **Estimated Effort:** 4-5 hours
- **Dependencies:** Phase 3 complete

### 4.2 Post-Launch Commands
- **Task:** Run custom shell commands after opening terminal/editor
- **Implementation:**
  - Add `post_launch_commands` to config (per terminal or profile)
  - Examples: activate venv, start dev server, git fetch
  - Support both sync and async execution
- **Estimated Effort:** 3-4 hours
- **Dependencies:** 2.3, 4.1

### 4.3 Multi-Project Batch Launch
- **Task:** Launch multiple projects simultaneously
- **Implementation:**
  - Allow Quick Action on multiple selected folders
  - Present single consolidated dialog for all projects
  - Launch terminals/editors in parallel
  - Option to use same terminal/editor for all
- **Estimated Effort:** 3-4 hours
- **Dependencies:** Phase 3 complete

### 4.4 CLI Alternative
- **Task:** Provide command-line interface for terminal users
- **Implementation:**
  - Create `dev-launcher` CLI tool using same core logic
  - Support flags: `--terminal`, `--editor`, `--profile`
  - Interactive mode if no flags provided
  - Install via `brew` or direct download
- **Estimated Effort:** 5-6 hours
- **Dependencies:** Phase 2, 3 complete

### 4.5 Keyboard Shortcut Integration
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

### 5.1 Enhanced README
- **Task:** Comprehensive documentation with examples
- **Implementation:**
  - Add screenshots/GIFs of workflow in action
  - Create detailed troubleshooting section
  - Document all configuration options
  - Provide compatibility matrix (macOS versions, Python versions)
  - Add permissions guide
- **Estimated Effort:** 3-4 hours
- **Dependencies:** Phase 3 complete

### 5.2 Example Configurations
- **Task:** Provide real-world config templates
- **Implementation:**
  - Create `examples/` directory
  - Add configs for common setups: web dev, data science, DevOps
  - Include profile examples
- **Estimated Effort:** 2 hours
- **Dependencies:** Phase 4 complete

### 5.3 Testing Framework
- **Task:** Add automated tests for core functionality
- **Implementation:**
  - Unit tests for config parsing, app validation
  - Mock subprocess calls for testing
  - CI/CD pipeline with GitHub Actions
- **Estimated Effort:** 5-6 hours
- **Dependencies:** Phase 2 complete

### 5.4 Contributing Guidelines
- **Task:** Enable community contributions
- **Implementation:**
  - Add `CONTRIBUTING.md`
  - Define code style, PR process
  - Create issue templates
  - Add feature request template
- **Estimated Effort:** 2 hours
- **Dependencies:** None

**Phase 5 Deliverable:** Well-documented, maintainable, community-friendly project

---

## Implementation Timeline

**Conservative Estimate (Part-time development):**
- **Phase 1:** 1-2 weeks
- **Phase 2:** 2-3 weeks
- **Phase 3:** 2-3 weeks
- **Phase 4:** 3-4 weeks
- **Phase 5:** Ongoing

**Aggressive Timeline (Focused development):**
- **Phase 1:** 2-3 days
- **Phase 2:** 4-5 days
- **Phase 3:** 3-4 days
- **Phase 4:** 5-7 days
- **Phase 5:** Ongoing

---

## Success Metrics

- **Reliability:** Zero silent failures, all errors communicated clearly
- **Usability:** Single-action launch (Quick Action → Pick → Done)
- **Performance:** Launch time under 2 seconds on average
- **Adoption:** 10+ GitHub stars, 3+ contributors
- **Maintainability:** 80%+ code coverage, comprehensive documentation

---

## Notes & Considerations

### Backward Compatibility
- Maintain support for simple config format even as features expand
- Provide migration tools/scripts when config format changes
- Version the config schema for future-proofing

### macOS Version Support
- Test on macOS 12 (Monterey) through current version
- Document any version-specific features or limitations
- Consider using macOS-native Python 3 vs. Homebrew Python

### Performance Considerations
- Keep startup time minimal (avoid heavy imports)
- Launch apps asynchronously to prevent blocking
- Cache app existence checks for repeated use

### Security Considerations
- Never execute arbitrary commands from config without validation
- Sanitize all file paths and app names
- Consider sandboxing for post-launch commands (Phase 4)

---

## Future Ideas (Backlog)

Ideas for consideration beyond this roadmap:

- **Terminal multiplexer integration:** Auto-create tmux/screen sessions
- **Remote project support:** SSH into remote dev boxes
- **Container integration:** Launch Docker/Podman containers
- **IDE plugin:** Create VS Code/JetBrains extensions
- **Analytics:** Optional anonymous usage stats for improvement insights
- **GUI configuration editor:** Electron or native app for config management
- **Workspace restoration:** Save/restore entire development sessions

---

## Getting Started with Implementation

**Recommended Approach:**

1. **Create a development branch:** `git checkout -b feature/roadmap-implementation`
2. **Start with Phase 1.1:** It's foundational and self-contained
3. **Test thoroughly at each step:** Don't rush to next phase
4. **Update this roadmap:** Check off completed items, adjust estimates
5. **Release incrementally:** Tag versions at each phase completion

**Questions to Consider:**
- Which phases are most valuable to your daily workflow?
- Are there any phases you want to skip or reprioritize?
- Should we create separate branches/PRs for each phase?

---

**Ready to start? Let me know which phase you'd like to tackle first, and I can help implement it!**
