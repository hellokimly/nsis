@echo off
echo Testing Python silent installer...
python "%~dp0test_installer.py"
if %ERRORLEVEL% EQU 0 (
    echo All tests passed!
) else (
    echo Tests failed with error code %ERRORLEVEL%
)
pause
