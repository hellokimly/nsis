# Python-based Silent Installer for SCRM Champion with Windows SDK

This repository contains a Python-based silent installer for SCRM Champion that bundles and silently executes the Windows SDK installer after the main installation completes.

## Implementation Details

The implementation uses a Python script that:

1. Creates a unique temporary directory
2. Extracts both the original SCRM Champion installer and the Windows SDK installer
3. Runs the SCRM Champion installer with UI
4. Waits for the original installer to complete
5. Silently executes the Windows SDK installer
6. Cleans up temporary files

## Files

- `build/silent_installer.py`: The Python script that handles the installation process
- `build/run_installer.bat`: A batch file to easily run the Python script on Windows
- `SCRM Champion-v4.85.1-win32-x64.exe`: The original SCRM Champion installer
- `winsdksetup.exe`: The Windows SDK installer

## Running the Installer

To run the installer, simply execute the batch file:

```
run_installer.bat
```

Or run the Python script directly:

```
python build/silent_installer.py
```

## Testing

To verify that the installer works correctly:

1. Run the batch file or Python script
2. Verify that the SCRM Champion installer runs with UI as expected
3. Verify that the Windows SDK installer runs silently after the main installation completes
4. Verify that both applications work correctly after installation
5. Verify that temporary files are cleaned up properly

## Notes

- The Python script creates a log file in the system's temporary directory
- The Windows SDK installer is executed with the `/quiet /norestart` options to ensure silent installation
- A unique temporary directory is created for each installation to avoid conflicts
