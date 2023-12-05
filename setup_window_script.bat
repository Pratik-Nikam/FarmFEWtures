@echo off

:: Task 0: Check if curl is installed, if not, install it 
where curl >nul 2>&1 || (
    echo Installing curl...
    curl -O https://curl.se/windows/dl-7.80.0/curl-7.80.0-win64-mingw.zip || (
        echo Error installing curl
        pause
        exit /b 1
    )
    tar -xf curl-7.80.0-win64-mingw.zip -C C:\ || (
        echo Error extracting curl archive
        pause
        exit /b 1
    )
    del curl-7.80.0-win64-mingw.zip || (
        echo Error deleting curl archive
        pause
        exit /b 1
    )
)

set JDK_VERSION=12.0.2
::set INSTALL_DIR=C:\java\jdk-%JDK_VERSION%

set INSTALL_DIR=C:\java

:: Create installation directory
if exist "%INSTALL_DIR%" (
    echo ++++++++++++++++ Found JDK %JDK_VERSION% at %INSTALL_DIR%
) else (
    mkdir %INSTALL_DIR%
    echo Downloading OpenJDK %JDK_VERSION%...
    curl -L "https://download.java.net/java/GA/jdk%JDK_VERSION%/e482c34c86bd4bf8b56c0b35558996b9/10/GPL/openjdk-%JDK_VERSION%_windows-x64_bin.zip" -o "openjdk-%JDK_VERSION%_windows-x64_bin.zip"

    echo Extracting OpenJDK %JDK_VERSION%...
    powershell -Command "Expand-Archive -Path '%CD%\openjdk-%JDK_VERSION%_windows-x64_bin.zip' -DestinationPath '%INSTALL_DIR%'"
)

:: Add Java binary directory to PATH
setx PATH "%PATH%;%INSTALL_DIR%\bin" /M

echo OpenJDK %JDK_VERSION% installation completed.


set PYTHON_VERSION=3.9.7
set INSTALL_DIR=C:\Python\Python%PYTHON_VERSION%

:: Check if Python 3.9 is already installed
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Python 3.9 is already installed. Adding to PATH...
    setx PATH "%PATH%;%INSTALL_DIR%;%INSTALL_DIR%\Scripts" /M
    echo Python added to PATH.
) else (
    :: Step 1: Download Python Installer
    echo Downloading Python Installer...
    curl -o python_installer.exe https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-amd64.exe

    :: Step 2: Create Installation Directory
    echo Creating installation directory...
    mkdir %INSTALL_DIR%

    :: Step 3: Install Python with pip and add to PATH
    echo Installing Python and adding to PATH...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1 TargetDir="%INSTALL_DIR%" DefaultPip=1

    echo Python installation completed.
)


:: Task 3: Check if a virtual environment exists, if not, create it
if not exist .\venv (
    echo Creating Python virtual environment...
    python -m venv venv || (
        echo Error creating Python virtual environment
        pause
        exit /b 1
    )
)

:: Task 4: Activate the virtual environment
call .\venv\Scripts\activate || (
    echo Error activating Python virtual environment
    pause
    exit /b 1
)

:: Task 5: Install modules from requirements.txt
if exist requirements.txt (
    echo Installing Python modules...
    pip install -r requirements.txt || (
        echo Error installing Python modules
        pause
        exit /b 1
    )
)


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


REM 8. Run the Flask application
echo Running Flask application...
python main.py

echo Setup completed successfully. Go to http://localhost:5000/ to view the application.
 