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


REM 1. Check if Chocolatey is installed, else install Chocolatey
where choco >nul 2>nul
if %errorlevel% == 0 (
    echo Chocolatey found.
) else (
    echo Chocolatey not found. Installing...
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
)

if not exist C:\Python39 (
    mkdir C:\Python39

    curl -o python-installer.exe https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe
    python-installer.exe /quiet TargetDir=C:\Python39
)


REM 3. Add Python to the system PATH
setx PATH "%PATH%;C:\Python39" /M

REM 4. Install pip
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
C:\Python39\python.exe get-pip.py

REM Clean up the downloaded script
del get-pip.py
del python-installer.exe

REM 5. Check Python version
C:\Python39\python.exe --version

::REM 6. Install required Python modules
::C:\Python39\Scripts\pip.exe install -r requirements.txt || (
::    echo Error installing Python modules
::    pause
::    exit /b 1
::)


REM Check if Java is now in the system PATH
where java >nul 2>nul
if %errorlevel% == 0 (
    echo Java installation and PATH updated successfully.
) else (
    echo Error updating Java installation and PATH.
)

REM 4. Check if a virtual environment exists, else create a virtual environment
if exist venv (
    echo Virtual environment found.
) else (
    echo Virtual environment not found. Creating....
    python -m venv venv
)

REM 5. Activate the virtual environment
call venv\Scripts\activate

:: Task 6: Install modules from requirements.txt
if exist requirements.txt (
    echo Installing Python modules...
    pip install -r requirements.txt || (
        echo Error installing Python modules
        pause
        exit /b 1
    )
)

:: Task 6: Check if NetLogo is installed, if not, download and install it
if not exist "C:\Program Files\NetLogo 6.4.0" (
    echo Downloading and installing NetLogo...
    curl -O https://ccl.northwestern.edu/netlogo/6.4.0/NetLogo-6.4.0-64.msi
    msiexec /i NetLogo-6.4.0-64.msi /quiet
    :: del NetLogo-6.4.0-64.msi
)

:: Task 7: Set the FLASK_APP environment variable
set FLASK_APP=main.py

:: Task 8: Run the Flask application
echo Running Flask application...
start cmd /k python main.py
