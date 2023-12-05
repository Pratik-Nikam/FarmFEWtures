@echo off
set "INSTALL_PATH=C:\Program Files\netlogo"
set "MSI_FILE=NetLogo-6.4.0-64.msi"
set "LOG_FILE=out.log"

:: Check if C:\netlogo exists
if exist "%INSTALL_PATH%" (
    echo NetLogo is already installed in "%INSTALL_PATH%". Skipping installation.
) else (
    :: Create installation directory
    mkdir "%INSTALL_PATH%"

    :: Download NetLogo using curl
    curl -LJO --fail https://ccl.northwestern.edu/netlogo/6.4.0/%MSI_FILE%
    if not exist "%MSI_FILE%" (
        echo Failed to download NetLogo MSI file.
    ) else (
        :: Install NetLogo
        msiexec /i "%MSI_FILE%" INSTALLDIR="%INSTALL_PATH%" /passive /qn /l*vx "%LOG_FILE%"
        echo NetLogo installation completed.

        :: Add NetLogo to PATH
        :: setx PATH "%PATH%;%INSTALL_PATH%" /M
        echo NetLogo added to PATH.
    )
)
