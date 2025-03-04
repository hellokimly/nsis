# Modified NSIS Installer for SCRM Champion with Windows SDK

This repository contains a modified NSIS installer for SCRM Champion that bundles and silently executes the Windows SDK installer after the main installation completes.

## Implementation Details

The implementation uses a wrapper NSIS script that:

1. Bundles both the original SCRM Champion installer and the Windows SDK installer
2. Extracts them to a temporary directory during installation
3. Executes the original installer with UI
4. Waits for the original installer to complete
5. Silently executes the Windows SDK installer
6. Cleans up temporary files

## Files

- `build/wrapper_installer.nsi`: The NSIS script that creates the wrapper installer
- `SCRM Champion-v4.85.1-win32-x64.exe`: The original SCRM Champion installer
- `winsdksetup.exe`: The Windows SDK installer

## Building the Installer

To build the modified installer, run:

```bash
makensis build/wrapper_installer.nsi
```

This will create a new installer file named `SCRM Champion-v4.85.1-with-SDK-win32-x64.exe` in the current directory.

## Testing

To verify that the modified installer works correctly:

1. Run the modified installer
2. Verify that the SCRM Champion installer runs with UI as expected
3. Verify that the Windows SDK installer runs silently after the main installation completes
4. Verify that both applications work correctly after installation
5. Verify that temporary files are cleaned up properly

## Notes

- The modified installer preserves the original installer's execution level (asInvoker)
- The Windows SDK installer is executed with the `/quiet /norestart` options to ensure silent installation
- A unique temporary directory is created for each installation to avoid conflicts
