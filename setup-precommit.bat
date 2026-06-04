@echo off
REM Setup pre-commit hooks for Windows

setlocal enabledelayedexpansion

echo.
echo ===================================================================
echo 0x4 Setting up pre-commit hooks
echo ===================================================================
echo.

REM Check if pre-commit is installed
where pre-commit >nul 2>nul
if %errorlevel% neq 0 (
    echo 0x50 Installing pre-commit...
    pip install pre-commit
) else (
    echo 0x52 pre-commit is already installed
)

REM Install git hooks
echo.
echo 0x51 Installing git hooks...
pre-commit install

REM Run on all files initially
echo.
echo 0x52 Running pre-commit on all files...
echo    (This may take a moment...)
pre-commit run --all-files

echo.
echo ===================================================================
echo 0x52 Pre-commit setup complete!
echo.
echo 0x50 Next time you commit, pre-commit will automatically:
echo    * Format code with Black
echo    * Sort imports with isort
echo    * Lint with Ruff
echo    * Check types with mypy
echo    * Validate YAML files
echo    * Check for common issues
echo.
echo 0x54 Tips:
echo    * Run manually: pre-commit run --all-files
echo    * Skip hooks: git commit --no-verify
echo    * Update hooks: pre-commit autoupdate
echo ===================================================================
echo.
