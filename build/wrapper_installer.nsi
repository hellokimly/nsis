; SCRM Champion Installer with Windows SDK
; This script creates a wrapper installer that bundles the original SCRM Champion installer
; and the Windows SDK installer, executing the SDK installer silently after the main installation.

; Include necessary headers
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"

; General configuration
Name "SCRM Champion v4.85.1"
OutFile "SCRM Champion-v4.85.1-with-SDK-win32-x64.exe"
InstallDir "$TEMP\SCRM_Champion_Installer"
RequestExecutionLevel user ; Match the original installer's execution level (asInvoker)

; Interface settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico" ; Default icon, will be replaced

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Variables
Var OriginalInstallerExitCode
Var SDKInstallerExitCode

; Installer sections
Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    SetOverwrite on
    
    ; Extract the original installer and Windows SDK installer
    File "../SCRM Champion-v4.85.1-win32-x64.exe"
    File "../winsdksetup.exe"
    
    ; Execute the original installer with UI
    DetailPrint "Running SCRM Champion installer..."
    ExecWait '"$INSTDIR\SCRM Champion-v4.85.1-win32-x64.exe"' $OriginalInstallerExitCode
    DetailPrint "SCRM Champion installer completed with exit code: $OriginalInstallerExitCode"
    
    ; Only proceed with SDK installation if the original installer was successful
    ${If} $OriginalInstallerExitCode == 0
        ; Execute Windows SDK installer silently
        DetailPrint "Installing Windows SDK silently..."
        ExecWait '"$INSTDIR\winsdksetup.exe" /quiet /norestart' $SDKInstallerExitCode
        DetailPrint "Windows SDK installer completed with exit code: $SDKInstallerExitCode"
    ${Else}
        DetailPrint "SCRM Champion installation failed or was cancelled. Skipping Windows SDK installation."
    ${EndIf}
    
    ; Clean up temporary files
    DetailPrint "Cleaning up temporary files..."
    Delete "$INSTDIR\SCRM Champion-v4.85.1-win32-x64.exe"
    Delete "$INSTDIR\winsdksetup.exe"
    RMDir "$INSTDIR"
SectionEnd

; Installer functions
Function .onInit
    ; Create a unique temporary directory
    ${GetTime} "" "L" $0 $1 $2 $3 $4 $5 $6
    StrCpy $INSTDIR "$TEMP\SCRM_Champion_Installer_$2$1$0$4$5$6"
    CreateDirectory $INSTDIR
FunctionEnd
