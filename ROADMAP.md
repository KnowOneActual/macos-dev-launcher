# macOS Dev Launcher Roadmap

**Project:** [macos-dev-launcher](https://github.com/KnowOneActual/macos-dev-launcher)  
**Purpose:** Systematic enhancement plan for improved reliability, UX, and extensibility  
**Last Updated:** December 1, 2025  
**Current Version:** v1.5.0

---

## Overview

This roadmap outlines a phased approach to enhancing the macOS Dev Launcher while maintaining its core simplicity and usability. Each phase builds on the previous one, ensuring the tool remains functional throughout development.

---

## Phase 1: Foundation & Robustness (Priority: High) ✅ COMPLETE

**Goal:** Ensure reliability and graceful failure handling before adding new features.

### 1.1 Application Validation ✅
- **Status:** COMPLETED (v1.1.0)
- **Task:** Verify terminal and editor apps exist before presenting options
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours

### 1.2 Error Messaging & User Feedback ✅
- **Status:** COMPLETED (integrated across phases)
- **Task:** Implement informative dialogs for errors and success states
- **Completed:** November 30, 2025

### 1.3 Path & Input Sanitization ✅
- **Status:** COMPLETED (v1.2.0)
- **Task:** Safely handle special characters, spaces, and potentially malicious paths
- **Completed:** November 30, 2025
- **Actual Effort:** 1 hour

### 1.4 Logging Infrastructure ✅
- **Status:** COMPLETED (v1.3.0)
- **Task:** Add optional logging for troubleshooting
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours

**Phase 1 Deliverable:** ✅ **ACHIEVED** - Robust, production-ready base with comprehensive error handling

---

## Phase 2: Configuration & Customization (Priority: Medium) ✅ COMPLETE

**Goal:** Enable user-specific workflows without hardcoding values.

### 2.1 External Configuration File ✅
- **Status:** COMPLETED (v1.4.0)
- **Task:** Move configuration out of script into a user-editable file
- **Completed:** November 30, 2025
- **Actual Effort:** 3 hours

### 2.2 Multi-Editor Support ✅
- **Status:** COMPLETED (v1.4.0)
- **Task:** Allow selection from multiple editors, not just one
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours

### 2.3 Custom Launch Arguments ✅
- **Status:** COMPLETED (v1.4.0)
- **Task:** Support terminal/editor-specific arguments
- **Completed:** November 30, 2025
- **Actual Effort:** 2 hours

### 2.4 Memory/Favorites System ✅
- **Status:** COMPLETED (v1.5.0)
- **Task:** Remember last-used terminal/editor per project
- **Implementation:**
  - Create `~/.config/macos-dev-launcher/history.json`
  - Store project path → (terminal, editor) mappings
  - Pre-select last choice in dialogs as default
- **Completed:** December 1, 2025
- **Actual Effort:** 2.5 hours
- **Dependencies:** 2.1 ✅
- **Features Delivered:**
  - ✅ `history.json` file storage
  - ✅ `load_history()`, `save_choice()`, `get_last_choice()` functions
  - ✅ Pre-selection logic in terminal and editor dialogs
  - ✅ Timestamp tracking per project
  - ✅ Auto-creation of history file
  - ✅ Enhanced `--test` mode with history display
  - ✅ Comprehensive logging of all history operations

**Phase 2 Deliverable:** ✅ **FULLY ACHIEVED** - Complete customizable launcher with persistent preferences

---

## Phase 3: User Experience Enhancements (Priority: Medium)

**Goal:** Polish the interaction flow and provide power-user features.

### 3.1 Combined Launch Options Dialog
- **Status:** NOT STARTED
- **Estimated Effort:** 2-3 hours
- **Dependencies:** Phase 2 complete ✅
- **Ready to start:** Yes

### 3.2 Installation Script
- **Status:** NOT STARTED
- **Estimated Effort:** 4-5 hours
- **Dependencies:** 2.1 ✅
- **Ready to start:** Yes
- **High Impact:** Would significantly improve adoption

### 3.3 Status Notifications
- **Status:** NOT STARTED
- **Estimated Effort:** 2 hours
- **Dependencies:** 2.1 ✅
- **Ready to start:** Yes

### 3.4 Project Type Detection
- **Status:** NOT STARTED
- **Estimated Effort:** 3-4 hours
- **Dependencies:** 2.2 ✅
- **Ready to start:** Yes

**Phase 3 Deliverable:** Streamlined, intelligent workflow with minimal friction

---

## Phase 4: Advanced Features (Priority: Low)

**Goal:** Extend capabilities for power users and specialized workflows.

### 4.1 Profile System
- **Status:** NOT STARTED
- **Estimated Effort:** 4-5 hours
- **Dependencies:** Phase 3 complete

### 4.2 Post-Launch Commands
- **Status:** NOT STARTED
- **Estimated Effort:** 3-4 hours
- **Dependencies:** 2.3 ✅, 4.1

### 4.3 Multi-Project Batch Launch
- **Status:** NOT STARTED
- **Estimated Effort:** 3-4 hours
- **Dependencies:** Phase 3 complete

### 4.4 CLI Alternative
- **Status:** NOT STARTED
- **Estimated Effort:** 5-6 hours
- **Dependencies:** Phase 2 ✅, 3 complete

### 4.5 Keyboard Shortcut Integration
- **Status:** NOT STARTED
- **Estimated Effort:** 2-3 hours
- **Dependencies:** 3.2

**Phase 4 Deliverable:** Feature-complete tool supporting advanced workflows

---

## Phase 5: Documentation & Community (Priority: Ongoing)

**Goal:** Enable adoption, contributions, and long-term maintenance.

### 5.1 Enhanced README ✅
- **Status:** COMPLETED (December 1, 2025)
- **Progress:**
  - ✅ Comprehensive configuration documentation
  - ✅ CLI usage guide
  - ✅ Troubleshooting section
  - ❌ Screenshots/GIFs (future enhancement)

### 5.2 Example Configurations
- **Status:** NOT STARTED
- **Estimated Effort:** 2 hours
- **Dependencies:** Phase 4 complete

### 5.3 Testing Framework
- **Status:** NOT STARTED
- **Estimated Effort:** 5-6 hours
- **Dependencies:** Phase 2 complete ✅
- **Ready to start:** Yes

### 5.4 Contributing Guidelines ✅
- **Status:** COMPLETED
- **File:** CONTRIBUTING.md exists

**Phase 5 Deliverable:** Well-documented, maintainable, community-friendly project

---

## Implementation Timeline

**Progress Summary:**
- **Phase 1:** ✅ COMPLETE (November 30, 2025)
- **Phase 2:** ✅ COMPLETE (December 1, 2025) 🎉
- **Phase 3:** 🔜 READY TO START
- **Phase 4:** ⏳ Waiting on Phase 3
- **Phase 5:** 🚧 ONGOING (README complete, tests pending)

**Next Milestone: Phase 3 Start**
- **Recommended:** Phase 3.2 (Installation Script) - High impact on adoption
- **Alternative:** Phase 3.1 (Combined dialog) - UX improvement
- **Alternative:** Phase 5.3 (Testing framework) - Code quality

---

## Success Metrics

- **Reliability:** ✅ Zero silent failures, all errors communicated clearly
- **Usability:** ✅ Single-action launch (Quick Action → Pick → Done)
- **Performance:** ✅ Launch time under 2 seconds
- **Customization:** ✅ External config with 14+ options
- **Memory:** ✅ Remembers preferences per project
- **Adoption:** ⏳ 0 stars (need promotion + installation script)
- **Maintainability:** ⏳ No tests yet, but excellent code structure

---

## Current State Summary (v1.5.0)

### ✅ What Works
- Full configuration system with JSON file
- Multi-terminal support with intelligent filtering
- Multi-editor support with smart dialogs
- Custom launch arguments per app
- **Memory system - remembers choices per project** 🎆
- Comprehensive logging with rotation
- Path security and validation
- CLI with test/verbose modes
- Complete error handling and user feedback

### 🎯 Phase 2 Fully Complete!

**All features delivered:**
- External configuration
- Multi-editor support
- Custom arguments
- Memory/favorites system

**Ready for Phase 3!**

### 🔜 Ready to Implement
- Phase 3.2: Installation script (highest impact)
- Phase 3.1: Combined launch dialog
- Phase 5.3: Testing framework

---

## Recommended Next Steps

**Option 1: High Impact - Installation Script (4-5 hours)**
Create automated setup that:
- Downloads and installs script
- Creates Automator Quick Action automatically
- Sets up config file
- One-command installation for new users
- **Result:** v2.0.0 release, major adoption boost

**Option 2: Quick UX Win - Combined Dialog (2-3 hours)**
- Single dialog for terminal + editor selection
- Faster workflow
- Better UX
- **Result:** v1.6.0 release

**Option 3: Code Quality - Testing Framework (5-6 hours)**
- Unit tests for all core functions
- CI/CD pipeline
- Better maintainability
- **Result:** v1.5.1 release, professional quality

---

**🎉 Phase 2 Fully Complete! The launcher now remembers your preferences perfectly.**

**Recommended: Tackle Phase 3.2 (Installation Script) next for maximum user impact!**
