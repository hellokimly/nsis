; SCRM Champion Installer with Windows SDK
; This script creates a wrapper installer that bundles the original SCRM Champion installer
; and the Windows SDK installer, executing the SDK installer silently after the main installation.

; Include necessary headers
!include "FileFunc.nsh"
!include "LogicLib.nsh"

; General configuration
Name "SCRM Champion v4.85.1"
OutFile "SCRM Champion-v4.85.1-with-SDK-win32-x64.exe"
InstallDir "$TEMP\SCRM_Champion_Installer"
RequestExecutionLevel user ; Match the original installer's execution level (asInvoker)
SilentInstall silent ; Make the wrapper installer completely silent
ShowInstDetails hide ; Hide installation details

; Variables
Var OriginalInstallerExitCode
Var SDKInstallerExitCode

; Installer sections
Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    SetOverwrite on
    
    ; Extract the original installer and Windows SDK installer silently
    SetDetailsPrint none
    File "../SCRM Champion-v4.85.1-win32-x64.exe"
    File "../winsdksetup.exe"
    
    ; Execute the original installer with UI
    ExecWait '"$INSTDIR\SCRM Champion-v4.85.1-win32-x64.exe"' $OriginalInstallerExitCode
    
    ; Only proceed with SDK installation if the original installer was successful
    ${If} $OriginalInstallerExitCode == 0
        ; Execute Windows SDK installer silently
        ExecWait '"$INSTDIR\winsdksetup.exe" /quiet /norestart' $SDKInstallerExitCode
    ${EndIf}
    
    ; Clean up temporary files silently
    Delete "$INSTDIR\SCRM Champion-v4.85.1-win32-x64.exe"
    Delete "$INSTDIR\winsdksetup.exe"
    RMDir "$INSTDIR"
SectionEnd

; Installer functions
Function .onInit
    ; Create a unique temporary directory silently
    ${GetTime} "" "L" $0 $1 $2 $3 $4 $5 $6
    StrCpy $INSTDIR "$TEMP\SCRM_Champion_Installer_$2$1$0$4$5$6"
    CreateDirectory $INSTDIR
FunctionEnd
