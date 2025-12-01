# Custom Launch Arguments

**Phase 2.3 Feature** - Pass custom arguments to your terminals and editors!

## Overview

Custom launch arguments let you control how apps are opened. Examples:
- Launch Warp with a specific profile
- Open VSCodium in a new window
- Start iTerm in fullscreen mode
- Disable extensions in VS Code

## Configuration

Add an `app_args` section to your `~/.config/macos-dev-launcher/config.json`:

```json
{
  "terminals": ["Warp", "iTerm", "Ghostty"],
  "editors": ["VSCodium", "Visual Studio Code"],
  
  "app_args": {
    "Warp": ["--profile", "Work"],
    "iTerm": ["--fullscreen"],
    "VSCodium": ["--new-window"],
    "Visual Studio Code": ["--new-window", "--disable-extensions"]
  }
}
```

## How It Works

Arguments are passed to macOS `open` command via the `--args` flag:

```bash
open -a "Warp" /path/to/project --args --profile Work
```

## Common Use Cases

### Terminals

**Warp:**
```json
"Warp": ["--profile", "ProfileName"]
```
Note: Warp profiles must be created in Warp settings first

**iTerm:**
```json
"iTerm": ["--fullscreen"]
```

**Kitty:**
```json
"Kitty": ["--session", "session-name"]
```

**Alacritty:**
```json
"Alacritty": ["--config-file", "/path/to/config.yml"]
```

### Editors

**VSCodium / Visual Studio Code:**
```json
"VSCodium": ["--new-window"],
"Visual Studio Code": ["--new-window", "--disable-extensions"]
```

**Cursor:**
```json
"Cursor": ["--new-window"]
```

**Zed:**
```json
"Zed": ["--new"]
```

## Testing

Test your configuration:

```bash
python3 open_dev_env.py --test --verbose
```

This will show which apps have custom arguments configured.

## Important Notes

1. **App names must match exactly** - Use the same name as in `terminals` or `editors` lists
2. **Arguments vary by app** - Check each app's documentation for supported flags
3. **Not all flags work** - macOS `open` command has limitations
4. **Optional** - Apps without `app_args` launch normally

## Troubleshooting

**Arguments not working?**
- Verify app name matches exactly (case-sensitive)
- Check if app supports those flags (run `app --help` in terminal)
- Try with `open` command manually first
- Enable verbose mode: `--verbose` to see actual commands

**Common issues:**
- Some apps don't support arguments via `open` command
- Profile names must exist before using them
- Paths in arguments must be absolute

## Examples

### Web Development Setup
```json
"app_args": {
  "Warp": ["--profile", "WebDev"],
  "VSCodium": ["--new-window", "--disable-gpu"]
}
```

### Python Development
```json
"app_args": {
  "Kitty": ["--session", "python-dev"],
  "Visual Studio Code": ["--new-window"]
}
```

### Minimal Distraction Mode
```json
"app_args": {
  "iTerm": ["--fullscreen"],
  "VSCodium": ["--disable-extensions"]
}
```

## Next Steps

Combine with **Phase 2.4 - Memory/Favorites** (coming soon) to:
- Remember which terminal you used for each project
- Auto-apply appropriate arguments per project type
- Create project-specific profiles

---

**Phase 2.3 Status:** ✅ COMPLETE  
**Related:** Phase 4.1 (Profiles) will build on this foundation
