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
- `build/test_installer.py`: A test script to verify installer functionality
- `build/test_installer.bat`: A batch file to run the test script on Windows
- `SCRM Champion-v4.85.1-win32-x64.exe`: The original SCRM Champion installer
- `winsdksetup.exe`: The Windows SDK installer

## Requirements

- Python 3.6 or higher (Python 3.12 recommended)
- Windows operating system
- Administrator privileges (if required by the installers)

## Installation

1. Ensure Python is installed on your system
2. Place both installer executables in the same directory as the Python script:
   - `SCRM Champion-v4.85.1-win32-x64.exe`
   - `winsdksetup.exe`

## Running the Installer

To run the installer, simply execute the batch file:

```
build\run_installer.bat
```

Or run the Python script directly:

```
python build\silent_installer.py
```

The installer will:
1. Run completely silently in the background
2. Automatically launch the SCRM Champion installer with UI
3. Wait for the SCRM Champion installation to complete
4. Silently install the Windows SDK
5. Clean up all temporary files

## Testing

To test the installer without actually running the installers:

```
build\test_installer.bat
```

Or run the test script directly:

```
python build\test_installer.py
```

To verify that the actual installer works correctly:

1. Run the batch file or Python script
2. Verify that the SCRM Champion installer runs with UI as expected
3. Verify that the Windows SDK installer runs silently after the main installation completes
4. Verify that both applications work correctly after installation
5. Verify that temporary files are cleaned up properly

## Logging

The installer creates a log file in the system's temporary directory (`%TEMP%\scrm_installer.log`) that contains detailed information about the installation process. This can be useful for troubleshooting if any issues occur.

## Notes

- The Python script runs completely silently with no UI
- The SCRM Champion installer runs with its normal UI
- The Windows SDK installer is executed with the `/quiet /norestart` options to ensure silent installation
- A unique temporary directory is created for each installation to avoid conflicts
- All temporary files are automatically cleaned up after installation
