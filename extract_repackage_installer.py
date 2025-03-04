#!/usr/bin/env python3
"""
SCRM Champion and Windows SDK Installer Extraction and Repackaging Script

This script automates the extraction and repackaging of SCRM Champion and Windows SDK installers.
It extracts the contents of the SCRM Champion installer and creates a new installer that
directly includes both the SCRM Champion app and the Windows SDK.

Usage:
from extract_repackage_installer import RepackageTool

# Create repackage tool instance
repackager = RepackageTool()

# Method 1: Explicitly specify paths
repackager.extract_and_repackage(
    scrm_installer="SCRM Champion-v4.85.1-win32-x64.exe",
    sdk_installer="winsdksetup.exe",
    output_path="SCRM Champion-with-SDK.exe",
    silent_sdk=True # Set to False for interactive SDK installation
)

# Method 2: Auto-detect installers
repackager.extract_and_repackage(silent_sdk=False) # Interactive SDK installation
"""

import os
import sys
import shutil
import tempfile
import subprocess
import logging
from pathlib import Path
from datetime import datetime


class RepackageTool:
    def __init__(self):
        """Initialize the repackaging tool and configure logging."""
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"repackager_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def find_installers(self, scrm_path=None, sdk_path=None):
        """If installers are not specified, find them."""
        script_dir = Path(__file__).parent.resolve()
        parent_dir = script_dir.parent

        # Find SCRM Champion installer
        if scrm_path is None:
            # Look for SCRM Champion installer in current, script, and parent directories
            for directory in [Path.cwd(), script_dir, parent_dir]:
                for file in directory.glob("*SCRM*Champion*.exe"):
                    scrm_path = file
                    self.logger.info(f"Found SCRM Champion installer: {scrm_path}")
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
                    self.logger.info(f"Found Windows SDK installer: {sdk_path}")
                    break
                if sdk_path:
                    break
        else:
            sdk_path = Path(sdk_path)

        return scrm_path, sdk_path

    def create_output_path(self, scrm_path, output_path=None):
        """If output path is not specified, create one for the repackaged installer."""
        if output_path is None:
            # Extract version from SCRM Champion installer filename
            filename = scrm_path.name
            version_match = filename.split("SCRM Champion-")[1].split("-win")[
                0] if "SCRM Champion-" in filename else "latest"

            # Create output filename
            output_path = scrm_path.parent / f"SCRM Champion-{version_match}-with-SDK-win32-x64.exe"
            self.logger.info(f"Generated output path: {output_path}")
        else:
            output_path = Path(output_path)

        return output_path

    def extract_scrm_installer(self, scrm_path):
        """Extract the contents of the SCRM Champion installer."""
        self.logger.info(f"Extracting SCRM Champion installer: {scrm_path}")
        
        # Create temporary directory for extraction
        extract_dir = Path(tempfile.mkdtemp(prefix='scrm_extract_'))
        self.logger.info(f"Created temporary directory for extraction: {extract_dir}")
        
        try:
            # Extract SCRM Champion installer using 7zip
            self.logger.info("Extracting with 7zip...")
            result = subprocess.run(
                ["7z", "x", "-o" + str(extract_dir), str(scrm_path), "-y"],
                check=True,
                capture_output=True,
                text=True
            )
            self.logger.info("Extraction completed successfully")
            
            # Check if app-64.7z exists and extract it
            app_7z = extract_dir / "$PLUGINSDIR" / "app-64.7z"
            if app_7z.exists():
                self.logger.info(f"Found app-64.7z, extracting...")
                app_extract_dir = extract_dir / "app"
                app_extract_dir.mkdir(exist_ok=True)
                
                result = subprocess.run(
                    ["7z", "x", "-o" + str(app_extract_dir), str(app_7z), "-y"],
                    check=True,
                    capture_output=True,
                    text=True
                )
                self.logger.info("App extraction completed successfully")
            else:
                self.logger.warning("app-64.7z not found in extracted files")
            
            return extract_dir
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error extracting SCRM Champion installer: {e}")
            self.logger.error(f"stdout: {e.stdout}")
            self.logger.error(f"stderr: {e.stderr}")
            shutil.rmtree(extract_dir)
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error during extraction: {e}")
            shutil.rmtree(extract_dir)
            return None

    def create_direct_nsis_installer(self, extract_dir, sdk_path, output_path, silent_sdk=True):
        """Create a direct NSIS installer that includes both SCRM Champion and Windows SDK."""
        self.logger.info("Creating direct NSIS installer")
        self.logger.info(f"Windows SDK silent install mode: {'enabled' if silent_sdk else 'disabled'}")
        
        # Create temporary directory for NSIS script
        temp_dir = Path(tempfile.mkdtemp(prefix='nsis_direct_'))
        self.logger.info(f"Created temporary directory: {temp_dir}")
        
        try:
            # Create NSIS script
            nsis_script = temp_dir / "direct_installer.nsi"
            
            # Determine SDK install command based on silent_sdk parameter
            sdk_install_command = f'ExecWait \'"$INSTDIR\\winsdksetup.exe" /quiet /norestart\' $1' if silent_sdk else f'ExecWait \'"$INSTDIR\\winsdksetup.exe"\' $1'
            
            # Check if app directory exists
            app_dir = extract_dir / "app"
            app_files_dir = app_dir if app_dir.exists() else extract_dir
            
            with open(nsis_script, 'w') as f:
                f.write(f"""
                ; SCRM Champion with Windows SDK Direct Installer
                ; This script creates a direct installer that includes
                ; both SCRM Champion and Windows SDK.
                
                ; Include necessary header files
                !include "FileFunc.nsh"
                !include "LogicLib.nsh"
                !include "MUI2.nsh"
                
                ; General configuration
                Name "SCRM Champion with Windows SDK"
                OutFile "{output_path}"
                InstallDir "$PROGRAMFILES64\\SCRM Champion"
                RequestExecutionLevel admin
                
                ; Interface settings
                !define MUI_ABORTWARNING
                
                ; Pages
                !insertmacro MUI_PAGE_WELCOME
                !insertmacro MUI_PAGE_DIRECTORY
                !insertmacro MUI_PAGE_INSTFILES
                !insertmacro MUI_PAGE_FINISH
                
                ; Languages
                !insertmacro MUI_LANGUAGE "English"
                
                Section "SCRM Champion" SecSCRM
                    SetOutPath "$INSTDIR"
                    SetOverwrite on
                    
                    ; Copy all SCRM Champion files
                    File /r "{app_files_dir}\\*.*"
                    
                    ; Copy Windows SDK installer
                    File "{sdk_path}"
                    
                    ; Create shortcuts
                    CreateDirectory "$SMPROGRAMS\\SCRM Champion"
                    CreateShortcut "$SMPROGRAMS\\SCRM Champion\\SCRM Champion.lnk" "$INSTDIR\\SCRM Champion.exe"
                    CreateShortcut "$DESKTOP\\SCRM Champion.lnk" "$INSTDIR\\SCRM Champion.exe"
                    
                    ; Install Windows SDK
                    {sdk_install_command}
                    
                    ; Write uninstaller
                    WriteUninstaller "$INSTDIR\\Uninstall SCRM Champion.exe"
                SectionEnd
                
                Section "Uninstall"
                    ; Remove shortcuts
                    Delete "$SMPROGRAMS\\SCRM Champion\\SCRM Champion.lnk"
                    Delete "$DESKTOP\\SCRM Champion.lnk"
                    RMDir "$SMPROGRAMS\\SCRM Champion"
                    
                    ; Remove files
                    Delete "$INSTDIR\\winsdksetup.exe"
                    Delete "$INSTDIR\\Uninstall SCRM Champion.exe"
                    RMDir /r "$INSTDIR"
                SectionEnd
                """)
            
            # Run makensis to create installer
            try:
                subprocess.run(["makensis", str(nsis_script)], check=True)
                self.logger.info(f"Created direct NSIS installer: {output_path}")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Error creating NSIS installer: {e}")
                return None
            except FileNotFoundError:
                self.logger.error("makensis not found. Please install NSIS to create the installer.")
                return None
            
            return output_path
            
        finally:
            # Clean up temporary directory
            try:
                shutil.rmtree(temp_dir)
                self.logger.info(f"Cleaned up temporary directory: {temp_dir}")
            except Exception as e:
                self.logger.error(f"Error cleaning up temporary directory: {e}")

    def extract_and_repackage(self, scrm_installer=None, sdk_installer=None, output_path=None, silent_sdk=True):
        """
        Main method to extract and repackage the installers.
        
        Args:
            scrm_installer (str, optional): Path to SCRM Champion installer
            sdk_installer (str, optional): Path to Windows SDK installer
            output_path (str, optional): Path for output installer
            silent_sdk (bool, optional): Whether to install Windows SDK silently, default is True
            
        Returns:
            int: 0 on success, 1 on failure
        """
        self.logger.info("Starting extraction and repackaging")
        self.logger.info(f"Windows SDK silent install mode: {'enabled' if silent_sdk else 'disabled'}")
        
        # Find installers
        scrm_path, sdk_path = self.find_installers(scrm_installer, sdk_installer)
        
        # Check if installers were found
        if scrm_path is None:
            self.logger.error("SCRM Champion installer not found. Please specify path explicitly.")
            return 1
            
        if sdk_path is None:
            self.logger.error("Windows SDK installer not found. Please specify path explicitly.")
            return 1
            
        self.logger.info(f"Using SCRM Champion installer: {scrm_path}")
        self.logger.info(f"Using Windows SDK installer: {sdk_path}")
        
        # Create output path
        output_path = self.create_output_path(scrm_path, output_path)
        self.logger.info(f"Output path: {output_path}")
        
        # Extract SCRM Champion installer
        extract_dir = self.extract_scrm_installer(scrm_path)
        if extract_dir is None:
            self.logger.error("Extraction failed")
            return 1
            
        try:
            # Create direct NSIS installer
            result = self.create_direct_nsis_installer(extract_dir, sdk_path, output_path, silent_sdk)
            
            if result:
                self.logger.info(f"Successfully created direct installer: {output_path}")
                return 0
            else:
                self.logger.error("Failed to create direct installer")
                return 1
        finally:
            # Clean up extraction directory
            try:
                shutil.rmtree(extract_dir)
                self.logger.info(f"Cleaned up extraction directory: {extract_dir}")
            except Exception as e:
                self.logger.error(f"Error cleaning up extraction directory: {e}")


# Usage example
if __name__ == "__main__":
    # Create repackage tool instance
    repackager = RepackageTool()
    
    # Extract and repackage with interactive SDK installation
    repackager.extract_and_repackage(silent_sdk=False)
