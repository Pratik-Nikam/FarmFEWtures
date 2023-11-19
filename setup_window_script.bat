:: Task 0: Check if curl is installed, if not, install it
where curl >nul 2>&1 || (
    echo Installing curl...
    curl -O https://curl.se/windows/dl-7.80.0/curl-7.80.0-win64-mingw.zip
    tar -xf curl-7.80.0-win64-mingw.zip -C C:\
    del curl-7.80.0-win64-mingw.zip
)

:: Task 1: Check if Python is installed, if not, install it
where python >nul 2>&1 || (
    echo Installing Python...
    curl -O https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe
    python-3.9.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    del python-3.9.0-amd64.exe
)

:: Task 2: Check if Java is installed, if not, install it
java -version >nul 2>&1 || (
    echo Installing Java...
    choco install openjdk -y
)

:: Task 3: Check if a virtual environment exists, if not, create it
if not exist .\venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

:: Task 4: Activate the virtual environment
call .\venv\Scripts\activate

:: Task 5: Install modules from requirements.txt
if exist requirements.txt (
    echo Installing Python modules...
    pip install -r requirements.txt
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
