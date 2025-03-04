import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path

def create_temp_dir():
    """Create a unique temporary directory for the installation."""
    return tempfile.mkdtemp(prefix='scrm_champion_installer_')

def run_installer(installer_path, silent=False):
    """Run an installer and wait for completion."""
    try:
        cmd = [str(installer_path)]
        if silent:
            cmd.append('/quiet')
            cmd.append('/norestart')
        
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running installer: {e}")
        return False

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.resolve()
    
    # Create temporary directory
    temp_dir = Path(create_temp_dir())
    
    try:
        # Copy installers to temp directory
        scrm_installer = script_dir / "SCRM Champion-v4.85.1-win32-x64.exe"
        sdk_installer = script_dir / "winsdksetup.exe"
        
        temp_scrm = temp_dir / scrm_installer.name
        temp_sdk = temp_dir / sdk_installer.name
        
        shutil.copy2(scrm_installer, temp_scrm)
        shutil.copy2(sdk_installer, temp_sdk)
        
        # Run SCRM Champion installer with UI
        if run_installer(temp_scrm):
            # If SCRM Champion installed successfully, run SDK installer silently
            run_installer(temp_sdk, silent=True)
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            print(f"Error cleaning up temporary directory: {e}")

if __name__ == "__main__":
    main()
