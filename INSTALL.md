# Installation Guide

## Method 1: pipx (Recommended)

**Best for:** End users who want a global CLI tool

```bash
# Install pipx (if needed)
brew install pipx  # macOS
# or: apt install pipx  # Ubuntu/Debian
# or: python3 -m pip install --user pipx

# Ensure pipx is in PATH
pipx ensurepath

# Install aigit
pipx install git+https://github.com/hardiksondagar/aigit.git

# Verify installation
aigit --help
```

### Benefits
- ✅ Available globally (`aigit` works from any directory)
- ✅ Isolated dependencies (won't conflict with other Python packages)
- ✅ Easy to upgrade: `pipx upgrade aigit`
- ✅ Easy to uninstall: `pipx uninstall aigit`

## Method 2: pip (Global)

**Best for:** Users who prefer traditional pip installation

```bash
# Clone the repo
git clone https://github.com/hardiksondagar/aigit.git
cd aigit

# Install globally
pip install .

# Verify installation
aigit --help
```

**Note:** You may need to add `~/.local/bin` to your PATH:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

## Method 3: Development Install

**Best for:** Contributors and developers

```bash
# Clone the repo
git clone https://github.com/hardiksondagar/aigit.git
cd aigit

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Verify installation
aigit --help
```

### For Global Access in Dev Mode with pipx:

```bash
# From the aigit directory
pipx install -e .
```

This installs aigit globally but changes you make to the source code are reflected immediately.

## Troubleshooting

### "command not found: aigit"

1. **Check if it's installed:**
   ```bash
   which aigit
   pip list | grep aigit
   # or: pipx list
   ```

2. **Add to PATH:**
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export PATH="$HOME/.local/bin:$PATH"
   source ~/.bashrc  # or source ~/.zshrc
   ```

### Python version issues

aigit requires Python 3.10+:
```bash
python --version  # Should be 3.10 or higher
```

If you have multiple Python versions:
```bash
python3.10 -m pipx install git+https://github.com/hardiksondagar/aigit.git
```

### Permission errors

Don't use `sudo` with pip/pipx. Instead:
- Use `pipx` (recommended)
- Use `pip install --user`
- Use a virtual environment

## Upgrading

### With pipx:
```bash
pipx upgrade aigit
```

### With pip:
```bash
pip install --upgrade git+https://github.com/hardiksondagar/aigit.git
```

### Development install:
```bash
cd aigit
git pull
# No reinstall needed if using pip install -e .
```

## Uninstalling

### With pipx:
```bash
pipx uninstall aigit
```

### With pip:
```bash
pip uninstall aigit
```

