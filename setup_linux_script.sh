#!/bin/bash

# 1. Check if Python is installed, else install Python
if command -v python3 &> /dev/null; then
    echo "Python found."
else
    echo "Python not found. Installing...."
    # Install Python (You may need to modify this based on your system package manager)
    sudo apt-get install python3
fi

# 2. Check if Java is installed, else install Java
if command -v java &> /dev/null; then
    echo "Java found."
else
    echo "Java not found. Installing..."
    # Install Java (You may need to modify this based on your system package manager)
    sudo apt-get install default-jre
fi

# 3. Check if a virtual environment exists, else create a virtual environment
if [ -d "venv" ]; then
    echo "Virtual environment found."
else
    echo "Virtual environment not found. Creating...."
    python3 -m venv venv
fi

# 4. Activate the virtual environment
source venv/bin/activate

# 5. Check if all modules from requirements.txt are installed, else install them
while read module; do
    if python -c "import $module" &> /dev/null; then
        echo "$module found."
    else
        echo "$module not found. Installing..."
        pip install $module
    fi
done < requirements.txt

# 6. Check if NetLogo is installed, else install NetLogo
if command -v NetLogo &> /dev/null; then
    echo "NetLogo found."
else
    echo "NetLogo not found. Installing..."
    # Install NetLogo using curl
    curl -LJO https://ccl.northwestern.edu/netlogo/6.2.0/NetLogo-6.2.0-64.tgz
    tar -xzvf NetLogo-6.2.0-64.tgz
fi

# 7. Set the FLASK_APP environment variable
export FLASK_APP=main.py

# 8. Run the Flask application
echo "Running Flask application..."
flask run

echo "Setup completed successfully. Go to http://localhost:5000/ to view the application."
