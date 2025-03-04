# Python-based Installer Solutions for SCRM Champion with Windows SDK

This repository contains two Python-based solutions for bundling and installing SCRM Champion with Windows SDK:

1. **Silent Installer**: A ready-to-use installer that bundles both applications
2. **Bundler Script**: A tool to create custom bundled installers

## Silent Installer

The silent installer automatically executes SCRM Champion with UI and then silently installs Windows SDK.

### Implementation Details

The implementation uses a Python script that:

1. Creates a unique temporary directory
2. Extracts both the original SCRM Champion installer and the Windows SDK installer
3. Runs the SCRM Champion installer with UI
4. Waits for the original installer to complete
5. Silently executes the Windows SDK installer
6. Cleans up temporary files

### Files

- `build/silent_installer.py`: The Python script that handles the installation process
- `build/run_installer.bat`: A batch file to easily run the Python script on Windows
- `build/test_installer.py`: A test script to verify installer functionality
- `build/test_installer.bat`: A batch file to run the test script on Windows
- `SCRM Champion-v4.85.1-win32-x64.exe`: The original SCRM Champion installer
- `winsdksetup.exe`: The Windows SDK installer

### Requirements

- Python 3.6 or higher (Python 3.12 recommended)
- Windows operating system
- Administrator privileges (if required by the installers)

### Installation

1. Ensure Python is installed on your system
2. Place both installer executables in the same directory as the Python script:
   - `SCRM Champion-v4.85.1-win32-x64.exe`
   - `winsdksetup.exe`

### Running the Installer

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

## Automated Bundling Script

The bundling script allows you to create custom bundled installers whenever needed.

### Files

- `build/create_bundled_installer.py`: The Python script that creates bundled installers
- `build/create_bundled_installer.bat`: A batch file to easily run the bundler script on Windows

### Requirements

- Python 3.6 or higher (Python 3.12 recommended)
- Windows operating system
- NSIS (optional, for NSIS-based bundling)
- 7-Zip (optional, for self-extracting archives on Windows)

### Usage

To create a bundled installer, run the bundler script:

```
python build\create_bundled_installer.py --scrm-installer "path\to\SCRM Champion.exe" --sdk-installer "path\to\winsdksetup.exe" --output "path\to\output.exe"
```

Or use the batch file:

```
build\create_bundled_installer.bat --scrm-installer "path\to\SCRM Champion.exe" --sdk-installer "path\to\winsdksetup.exe"
```

#### Command-line Arguments

- `--scrm-installer`: Path to the SCRM Champion installer (optional, auto-detected if not specified)
- `--sdk-installer`: Path to the Windows SDK installer (optional, auto-detected if not specified)
- `--output`: Path for the output bundled installer (optional, auto-generated if not specified)
- `--nsis`: Use NSIS to create the bundled installer (requires makensis)
- `--python`: Use Python to create the bundled installer (default)

#### Examples

Basic usage (auto-detect installers):
```
python build\create_bundled_installer.py
```

Specify installer paths:
```
python build\create_bundled_installer.py --scrm-installer "SCRM Champion-v4.85.1-win32-x64.exe" --sdk-installer "winsdksetup.exe"
```

Create NSIS-based installer:
```
python build\create_bundled_installer.py --nsis
```

### How It Works

The bundler script:
1. Finds the SCRM Champion and Windows SDK installers
2. Creates a temporary directory for bundling
3. Generates a bundled installer using either Python or NSIS
4. Outputs the bundled installer to the specified location

The bundled installer will:
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

Both the installer and bundler script create log files that contain detailed information about the process. These can be useful for troubleshooting if any issues occur.

## Notes

- The Python scripts run completely silently with no UI
- The SCRM Champion installer runs with its normal UI
- The Windows SDK installer is executed with the `/quiet /norestart` options to ensure silent installation
- Unique temporary directories are created to avoid conflicts
- All temporary files are automatically cleaned up after installation
