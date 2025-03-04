@echo off
echo Creating bundled installer for SCRM Champion with Windows SDK...
python "%~dp0create_bundled_installer.py" %*
if %ERRORLEVEL% EQU 0 (
    echo Bundled installer created successfully!
) else (
    echo Failed to create bundled installer.
)
pause
