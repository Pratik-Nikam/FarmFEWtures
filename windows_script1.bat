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


REM 1. Check if Python is installed, else install Python
where python >nul 2>nul
if %errorlevel% == 0 (
    echo Python found.
) else (
    echo Python not found. Installing....
    REM Install Python (You may need to modify this based on your Python installer)
    choco install python
    setx PATH "%PATH%;C:\ProgramData\chocolatey\lib\python\tools" /M
)


REM 2. Check if pip is installed, else install pip
where pip >nul 2>nul
if %errorlevel% == 0 (
    echo pip found.
) else (
    echo pip not found. Installing...
    choco install pip
)

REM 3. Check if Java is installed, else install Java
if exist "C:\Program Files\OpenJDK\jdk-21.0.1\bin\server\jvm.dll" (
    echo Java found.
) else (
    echo Java not found. Installing...
    REM Install Java (You may need to modify this based on your Java installer)
    choco install openjdk

    REM Add Java to the system PATH
    setx PATH "%PATH%;C:\Program Files\Java\jdk-20.0.2\bin" /M
    setx PATH "%PATH%;C:\Program Files\OpenJDK\jdk-21.0.1" /M
)

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


:: Task 7: Set the FLASK_APP environment variable
set FLASK_APP=main.py

:: Task 8: Run the Flask application
echo Running Flask application...
start cmd /k python main.py
