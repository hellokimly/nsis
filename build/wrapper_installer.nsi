; SCRM Champion Installer with Windows SDK
; This script creates a completely silent wrapper installer that automatically launches
; the SCRM Champion installer and then silently installs the Windows SDK.

; Include necessary headers
!include "FileFunc.nsh"
!include "LogicLib.nsh"

; General configuration
Name "SCRM Champion v4.85.1"
OutFile "SCRM Champion-v4.85.1-with-SDK-win32-x64.exe"
InstallDir "$TEMP\SCRM_Champion_Installer"
RequestExecutionLevel user ; Match the original installer's execution level (asInvoker)
SilentInstall silent ; Make the wrapper installer completely silent
AutoCloseWindow true ; Automatically close the installer window
ShowInstDetails hide ; Hide all installation details

Section
    SetOutPath "$INSTDIR"
    SetOverwrite on
    
    ; Silently extract installers
    File /nonfatal "../SCRM Champion-v4.85.1-win32-x64.exe"
    File /nonfatal "../winsdksetup.exe"
    
    ; Immediately launch SCRM Champion installer and wait for completion
    ExecWait '"$INSTDIR\SCRM Champion-v4.85.1-win32-x64.exe"' $0
    
    ; If SCRM Champion installer completed successfully, run Windows SDK installer
    ${If} $0 == 0
        ExecWait '"$INSTDIR\winsdksetup.exe" /quiet /norestart' $1
    ${EndIf}
    
    ; Clean up silently
    Delete "$INSTDIR\SCRM Champion-v4.85.1-win32-x64.exe"
    Delete "$INSTDIR\winsdksetup.exe"
    RMDir "$INSTDIR"
SectionEnd

Function .onInit
    ; Create unique temp directory silently
    ${GetTime} "" "L" $0 $1 $2 $3 $4 $5 $6
    StrCpy $INSTDIR "$TEMP\SCRM_Champion_Installer_$2$1$0$4$5$6"
    CreateDirectory $INSTDIR
FunctionEnd
