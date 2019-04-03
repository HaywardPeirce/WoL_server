# WoL_server

### Setup
The following steps outline how to setup a linux system to run this script (based on the information outlined in [this](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) guide)

1. Install Python 3.6+. For debian-based systems: `sudo apt-get install python3.6`
2. Install virtualenv to create an isolated python environment to run this script in `pip install virtualenv`
3. From the top level of the project folder, create a new virtual environment `virtualenv -p /usr/bin/python3.6 venv`. This example assumes the version of python you install was 3.6, so please plug in the version of python you used in step 1.
4. Activate your new virutal environment: `source venv/bin/activate`
5. Install the python packages you will need to run this script `pip install -r requirements.txt`

### Usage
Once the python virtual environment is activated, run the application using the following command from the top level of this repo: `python index.py`