# Kira-Bot AI Development Instructions

## Project Overview
This is a Discord chatbot with local LLM capabilities, featuring a modular GUI architecture, GPU optimization, and SQLite-based memory system. The bot integrates Discord commands, web search, and real-time system monitoring.

## Communication Guidelines
**IMPORTANT**: Always communicate in French when interacting with the project owner. The project is French-focused and all documentation, comments, and interactions should be in French.

**Instructions Updates**: Feel free to update these instructions with new discoveries, improvements, or replacements as the project evolves. Keep them current and relevant.

## Architecture Components

### Core Bot Structure
- **`bot.py`**: Main Discord bot entry point with command loading
- **`start_kira.py`**: Primary startup script
- **`model.py`**: LLM management with GPU optimization profiles
- **`config.py`**: Centralized configuration with advanced logging setup
- **`memory.py`**: SQLite-based conversational memory with fact storage

### GUI Architecture (Modular)
The GUI uses a modular architecture centered in `gui/`:
- **`gui/core/qt_imports.py`**: Centralized PySide6 imports, COLOR_PALETTE, FONTS, and shared utilities
- **`gui/modules/`**: Specialized components (notifications, monitoring, chat)
- **`gui/launch_gui.py`**: Unified launcher with fallback mechanisms
- **`gui/kira_gui.py`**: Legacy interface for compatibility

### Commands System
Located in `commands/`, each module exports a `setup(bot)` function:
- Commands use role-based authorization with optional 2FA TOTP
- GPU optimization commands in `optimize.py` with real-time profiling
- Memory commands support fact storage and conversation history

### Testing & Integration
- **`launchers/test_integration.py`**: Comprehensive architecture validation
- **`launchers/launch_optimized.py`**: Production launcher with dependency checks
- Tests validate: core imports, modules, GPU utils, widget creation, notifications

## Key Development Patterns

### Import Strategy
Always import from `gui.core` for Qt components to maintain consistency:
```python
from gui.core.qt_imports import QApplication, QWidget, COLOR_PALETTE, FONTS
from gui.modules import show_success, NotificationManager
```

### GPU Optimization Integration
GPU features are optional with graceful fallbacks:
```python
try:
    import pynvml
    NVIDIA_AVAILABLE = True
except ImportError:
    NVIDIA_AVAILABLE = False
```

Use `gpu_utils.gpu_manager` for GPU operations and `tools.gpu_optimizer` for performance profiling.

### Command Development
Create commands in `commands/` following this pattern:
```python
from auth_decorators import require_authorized_role, require_totp_if_enabled

async def your_command(ctx, *args):
    # Command logic here
    pass

def setup(bot):
    bot.add_command(commands.Command("your_command", your_command))
```

### GUI Module Development
When creating new GUI modules:
1. Use `gui/core/qt_imports.py` for all Qt imports
2. Follow the pattern in `gui/modules/` for specialized components
3. Export main classes/functions in `gui/modules/__init__.py`
4. Add tests to `launchers/test_integration.py`

### Environment & Virtual Environment
**CRITICAL**: Always activate the virtual environment before any command execution!

- Project uses `llama-venv/` virtual environment
- **MUST activate before ANY command**: `llama-venv\Scripts\activate` (Windows)
- Full Python path when needed: `C:/Dev/IA-chatbot/llama-venv/Scripts/python.exe`
- Key dependencies: PySide6, psutil, pynvml, llama-cpp-python

## Critical Workflows

### Running the Bot
**ALWAYS activate virtual environment first:**
```bash
# Windows - REQUIRED before any command
llama-venv\Scripts\activate

# Then run commands:
python start_kira.py                    # Discord bot

# GUI interfaces
python gui/launch_gui.py --legacy       # Legacy interface
python gui/launch_gui.py --modern       # Modern interface

# Optimized launcher with tests
python launchers/launch_optimized.py --mode test
```

### Testing Architecture
**Environment activation required:**
```bash
# Activate virtual environment FIRST
llama-venv\Scripts\activate

# Then run tests
python launchers/test_integration.py

# Expected output: 6/6 tests passing
# Tests: core imports, modules, GPU utils, architecture integrity, widgets, notifications
```

### GPU Optimization
The bot includes adaptive GPU profiling:
- 6+ optimization profiles (Performance, Balanced, Emergency, etc.)
- Real-time VRAM monitoring with temperature tracking
- Automatic fallback for non-NVIDIA systems

## Configuration Files

### JSON Configuration
- **`JSON/log_config.json`**: Advanced logging configuration
- **`JSON/context.json`**: Conversational context parameters
- **`JSON/character_limits.json`**: Response length limits
- **`JSON/autoreply.json`**: Auto-reply channel configuration

### Database Schema
- **`data/kira.db`**: SQLite with optimized indexes for conversations/facts
- **`data/logs.db`**: Advanced logging database with structured queries

## Debugging & Troubleshooting

### Common Issues
1. **Import errors**: Check virtual environment activation and `sys.path` setup
   - **CRITICAL**: Always run `llama-venv\Scripts\activate` before any Python command
   - Use full path if needed: `C:/Dev/IA-chatbot/llama-venv/Scripts/python.exe`
2. **GPU not detected**: Verify pynvml installation and NVIDIA drivers
3. **GUI launch failures**: Use `launch_gui.py` fallback mechanisms
4. **Command authorization**: Check Discord roles and TOTP configuration

### Logging System
Dual logging approach:
- Standard logging to `logs/kira_bot.log`
- Advanced structured logging to `data/logs.db` (if available)

Access via `config.logger` and `config.advanced_log_manager`.