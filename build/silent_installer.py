#!/usr/bin/env python3
"""
Silent Installer for SCRM Champion with Windows SDK

This script creates a silent installer that:
1. Extracts both the SCRM Champion installer and Windows SDK installer
2. Runs the SCRM Champion installer with UI
3. Silently runs the Windows SDK installer after SCRM Champion completes
4. Cleans up temporary files
"""

import os
import sys
import shutil
import tempfile
import subprocess
import time
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(tempfile.gettempdir(), "scrm_installer.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_temp_dir():
    """Create a unique temporary directory for the installation."""
    temp_dir = tempfile.mkdtemp(prefix='scrm_champion_installer_')
    logger.info(f"Created temporary directory: {temp_dir}")
    return temp_dir

def run_installer(installer_path, silent=False):
    """Run an installer and wait for completion.
    
    Args:
        installer_path: Path to the installer executable
        silent: Whether to run the installer silently
        
    Returns:
        True if installation was successful, False otherwise
    """
    try:
        cmd = [str(installer_path)]
        if silent:
            cmd.append('/quiet')
            cmd.append('/norestart')
        
        logger.info(f"Running installer: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True)
        logger.info(f"Installer completed with return code: {result.returncode}")
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error(f"Error running installer: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error running installer: {e}")
        return False

def main():
    """Main function to run the silent installer."""
    logger.info("Starting SCRM Champion with Windows SDK silent installer")
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.resolve()
    logger.info(f"Script directory: {script_dir}")
    
    # Create temporary directory
    temp_dir = Path(create_temp_dir())
    
    try:
        # Define installer paths
        scrm_installer = script_dir / "SCRM Champion-v4.85.1-win32-x64.exe"
        sdk_installer = script_dir / "winsdksetup.exe"
        
        # Check if installers exist
        if not scrm_installer.exists():
            logger.error(f"SCRM Champion installer not found at: {scrm_installer}")
            return 1
        
        if not sdk_installer.exists():
            logger.error(f"Windows SDK installer not found at: {sdk_installer}")
            return 1
        
        logger.info("Copying installers to temporary directory")
        temp_scrm = temp_dir / scrm_installer.name
        temp_sdk = temp_dir / sdk_installer.name
        
        # Copy installers to temp directory
        shutil.copy2(scrm_installer, temp_scrm)
        shutil.copy2(sdk_installer, temp_sdk)
        
        # Run SCRM Champion installer with UI
        logger.info("Running SCRM Champion installer with UI")
        if run_installer(temp_scrm):
            # If SCRM Champion installed successfully, run SDK installer silently
            logger.info("SCRM Champion installation successful, running Windows SDK installer silently")
            run_installer(temp_sdk, silent=True)
        else:
            logger.error("SCRM Champion installation failed, skipping Windows SDK installation")
            return 1
        
        logger.info("Installation completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error during installation: {e}")
        return 1
    finally:
        # Clean up temporary directory
        try:
            logger.info(f"Cleaning up temporary directory: {temp_dir}")
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temporary directory: {e}")

if __name__ == "__main__":
    sys.exit(main())
