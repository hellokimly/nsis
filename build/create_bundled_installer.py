#!/usr/bin/env python3
"""
Automated Bundling Script for SCRM Champion and Windows SDK Installers

This script automates the process of bundling SCRM Champion and Windows SDK installers.
It creates a new installer that will silently execute both installers in sequence.

Usage:
    python create_bundled_installer.py [--scrm-installer PATH] [--sdk-installer PATH] [--output PATH]

Example:
    python create_bundled_installer.py --scrm-installer "SCRM Champion-v4.85.1-win32-x64.exe" --sdk-installer "winsdksetup.exe" --output "SCRM Champion-with-SDK.exe"
"""

import os
import sys
import shutil
import tempfile
import argparse
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"bundler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Bundle SCRM Champion and Windows SDK installers')
    parser.add_argument('--scrm-installer', type=str, default=None,
                        help='Path to SCRM Champion installer')
    parser.add_argument('--sdk-installer', type=str, default=None,
                        help='Path to Windows SDK installer')
    parser.add_argument('--output', type=str, default=None,
                        help='Output path for bundled installer')
    parser.add_argument('--nsis', action='store_true',
                        help='Use NSIS to create the bundled installer (requires makensis)')
    parser.add_argument('--python', action='store_true', default=True,
                        help='Use Python to create the bundled installer')
    
    return parser.parse_args()

def find_installers(scrm_path=None, sdk_path=None):
    """Find installer files if not specified."""
    script_dir = Path(__file__).parent.resolve()
    parent_dir = script_dir.parent
    
    # Find SCRM Champion installer
    if scrm_path is None:
        # Look for SCRM Champion installer in current, script, and parent directories
        for directory in [Path.cwd(), script_dir, parent_dir]:
            for file in directory.glob("*SCRM*Champion*.exe"):
                scrm_path = file
                logger.info(f"Found SCRM Champion installer: {scrm_path}")
                break
            if scrm_path:
                break
    else:
        scrm_path = Path(scrm_path)
    
    # Find Windows SDK installer
    if sdk_path is None:
        # Look for Windows SDK installer in current, script, and parent directories
        for directory in [Path.cwd(), script_dir, parent_dir]:
            for file in directory.glob("*winsdksetup*.exe"):
                sdk_path = file
                logger.info(f"Found Windows SDK installer: {sdk_path}")
                break
            if sdk_path:
                break
    else:
        sdk_path = Path(sdk_path)
    
    return scrm_path, sdk_path

def create_output_path(scrm_path, output_path=None):
    """Create output path for bundled installer if not specified."""
    if output_path is None:
        # Extract version from SCRM Champion installer filename
        filename = scrm_path.name
        version_match = filename.split("SCRM Champion-")[1].split("-win")[0] if "SCRM Champion-" in filename else "latest"
        
        # Create output filename
        output_path = scrm_path.parent / f"SCRM Champion-{version_match}-with-SDK-win32-x64.exe"
        logger.info(f"Generated output path: {output_path}")
    else:
        output_path = Path(output_path)
    
    return output_path

def create_python_bundler(scrm_path, sdk_path, output_path):
    """Create a Python-based bundled installer."""
    logger.info("Creating Python-based bundled installer")
    
    # Create temporary directory for bundler files
    temp_dir = Path(tempfile.mkdtemp(prefix='bundler_'))
    logger.info(f"Created temporary directory: {temp_dir}")
    
    try:
        # Create silent_installer.py in temp directory
        installer_script = temp_dir / "silent_installer.py"
        with open(installer_script, 'w') as f:
            f.write('''#!/usr/bin/env python3
import os
import sys
import shutil
import tempfile
import subprocess
import logging
from pathlib import Path

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
    """Run an installer and wait for completion."""
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
        scrm_installer = script_dir / "SCRM_Champion.exe"
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
''')
        
        # Create batch file
        batch_file = temp_dir / "run_installer.bat"
        with open(batch_file, 'w') as f:
            f.write('@echo off\npython "%~dp0silent_installer.py"\n')
        
        # Copy installers to temp directory
        scrm_temp = temp_dir / "SCRM_Champion.exe"
        sdk_temp = temp_dir / "winsdksetup.exe"
        shutil.copy2(scrm_path, scrm_temp)
        shutil.copy2(sdk_path, sdk_temp)
        
        # Create self-extracting archive using 7-Zip
        try:
            # Check if 7-Zip is installed
            subprocess.run(["7z", "--help"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            
            # Create 7z archive
            archive_path = temp_dir / "installer.7z"
            subprocess.run(["7z", "a", str(archive_path), f"{temp_dir}/*"], check=True)
            
            # Create self-extracting config
            sfx_config = temp_dir / "config.txt"
            with open(sfx_config, 'w') as f:
                f.write('''
;!@Install@!UTF-8!
Title="SCRM Champion with Windows SDK Installer"
BeginPrompt="Do you want to install SCRM Champion with Windows SDK?"
RunProgram="run_installer.bat"
;!@InstallEnd@!
''')
            
            # Create self-extracting executable
            subprocess.run(["copy", "/b", "7zS.sfx", "+", str(sfx_config), "+", str(archive_path), str(output_path)], check=True)
            logger.info(f"Created self-extracting installer: {output_path}")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.warning("7-Zip not found, creating simple bundled installer")
            
            # Create simple bundled installer
            with open(output_path, 'wb') as outfile:
                # Write a simple header
                outfile.write(b"#!/usr/bin/env python3\n")
                outfile.write(b"# SCRM Champion with Windows SDK Bundled Installer\n")
                outfile.write(b"# This is a self-extracting Python script\n\n")
                
                # Write the Python script
                with open(installer_script, 'rb') as f:
                    outfile.write(f.read())
                
                # Write the installers as base64-encoded data
                outfile.write(b"\n\n# Bundled installers\n")
                outfile.write(b"import base64\n")
                
                # Write SCRM Champion installer
                outfile.write(b"SCRM_CHAMPION_INSTALLER = base64.b64decode('''\n")
                with open(scrm_path, 'rb') as f:
                    outfile.write(base64.b64encode(f.read()))
                outfile.write(b"''')\n\n")
                
                # Write Windows SDK installer
                outfile.write(b"WINDOWS_SDK_INSTALLER = base64.b64decode('''\n")
                with open(sdk_path, 'rb') as f:
                    outfile.write(base64.b64encode(f.read()))
                outfile.write(b"''')\n\n")
                
                # Write extraction code
                outfile.write(b"""
# Extract installers
def extract_installers():
    script_dir = Path(__file__).parent.resolve()
    
    # Extract SCRM Champion installer
    scrm_path = script_dir / "SCRM_Champion.exe"
    with open(scrm_path, 'wb') as f:
        f.write(SCRM_CHAMPION_INSTALLER)
    
    # Extract Windows SDK installer
    sdk_path = script_dir / "winsdksetup.exe"
    with open(sdk_path, 'wb') as f:
        f.write(WINDOWS_SDK_INSTALLER)
    
    return scrm_path, sdk_path

if __name__ == "__main__":
    # Extract installers
    extract_installers()
    
    # Run main installer
    sys.exit(main())
""")
            
            # Make the file executable
            os.chmod(output_path, 0o755)
            logger.info(f"Created bundled installer: {output_path}")
    
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temporary directory: {e}")
    
    return output_path

def create_nsis_bundler(scrm_path, sdk_path, output_path):
    """Create an NSIS-based bundled installer."""
    logger.info("Creating NSIS-based bundled installer")
    
    # Create temporary directory for NSIS script
    temp_dir = Path(tempfile.mkdtemp(prefix='nsis_bundler_'))
    logger.info(f"Created temporary directory: {temp_dir}")
    
    try:
        # Create NSIS script
        nsis_script = temp_dir / "wrapper_installer.nsi"
        with open(nsis_script, 'w') as f:
            f.write(f"""
; SCRM Champion Installer with Windows SDK
; This script creates a completely silent wrapper installer that automatically launches
; the SCRM Champion installer and then silently installs the Windows SDK.

; Include necessary headers
!include "FileFunc.nsh"
!include "LogicLib.nsh"

; General configuration
Name "SCRM Champion with Windows SDK"
OutFile "{output_path}"
InstallDir "$TEMP\\SCRM_Champion_Installer"
RequestExecutionLevel user ; Match the original installer's execution level (asInvoker)
SilentInstall silent ; Make the wrapper installer completely silent
AutoCloseWindow true ; Automatically close the installer window
ShowInstDetails hide ; Hide all installation details

Section
    SetOutPath "$INSTDIR"
    SetOverwrite on
    
    ; Silently extract installers
    File /nonfatal "{scrm_path}"
    File /nonfatal "{sdk_path}"
    
    ; Immediately launch SCRM Champion installer and wait for completion
    ExecWait '"$INSTDIR\\{scrm_path.name}"' $0
    
    ; If SCRM Champion installer completed successfully, run Windows SDK installer
    ${{If}} $0 == 0
        ExecWait '"$INSTDIR\\{sdk_path.name}" /quiet /norestart' $1
    ${{EndIf}}
    
    ; Clean up silently
    Delete "$INSTDIR\\{scrm_path.name}"
    Delete "$INSTDIR\\{sdk_path.name}"
    RMDir "$INSTDIR"
SectionEnd

Function .onInit
    ; Create unique temp directory silently
    ${{GetTime}} "" "L" $0 $1 $2 $3 $4 $5 $6
    StrCpy $INSTDIR "$TEMP\\SCRM_Champion_Installer_$2$1$0$4$5$6"
    CreateDirectory $INSTDIR
FunctionEnd
""")
        
        # Run makensis to create the installer
        try:
            subprocess.run(["makensis", str(nsis_script)], check=True)
            logger.info(f"Created NSIS bundled installer: {output_path}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error creating NSIS installer: {e}")
            return None
        except FileNotFoundError:
            logger.error("makensis not found. Please install NSIS or use --python option.")
            return None
    
    finally:
        # Clean up temporary directory
        try:
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            logger.error(f"Error cleaning up temporary directory: {e}")
    
    return output_path

def main():
    """Main function to create bundled installer."""
    logger.info("Starting bundled installer creation")
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Find installers
    scrm_path, sdk_path = find_installers(args.scrm_installer, args.sdk_installer)
    
    # Check if installers were found
    if scrm_path is None:
        logger.error("SCRM Champion installer not found. Please specify with --scrm-installer.")
        return 1
    
    if sdk_path is None:
        logger.error("Windows SDK installer not found. Please specify with --sdk-installer.")
        return 1
    
    logger.info(f"Using SCRM Champion installer: {scrm_path}")
    logger.info(f"Using Windows SDK installer: {sdk_path}")
    
    # Create output path
    output_path = create_output_path(scrm_path, args.output)
    logger.info(f"Output path: {output_path}")
    
    # Create bundled installer
    if args.nsis:
        # Create NSIS-based bundled installer
        result = create_nsis_bundler(scrm_path, sdk_path, output_path)
    else:
        # Create Python-based bundled installer
        result = create_python_bundler(scrm_path, sdk_path, output_path)
    
    if result:
        logger.info(f"Successfully created bundled installer: {output_path}")
        return 0
    else:
        logger.error("Failed to create bundled installer")
        return 1

if __name__ == "__main__":
    sys.exit(main())
