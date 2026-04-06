# Step-by-Step on How to Run Project

Assumptions:
- User knows basic command line
- User is using Windows
- User has at least python version 3.14 installed
- User has git installed

### Step 1: Download Project Source
1. Open a command prompt
2. Move to the directory where you want to clone the git repo
3. Run `git clone https://github.com/cpgeersen/Book-Tracker.git` in target folder

Outcome: Project source is now downloaded

### Step 2: Create and Activate Virtual Environment
1. In command prompt run (while point to project folder) `python -m venv .venv`
2. Now run `.venv\Scripts\activate`

Outcome: User now has a python virtual environment active

### Step 3: Download Requirements using pip
1. While virtual environment is active, run `py -m pip install -r requirements.txt` 
or `pip install -r requirements.txt` (sometimes one works while the other does not)

Outcome: All requirements are downloaded per requirements.txt to .venv and are tied to the virtual environment

### Step 4: Normal Virtual Environment Usage
For day-to-day usage, a user only needs to run `.venv\Scripts\activate` before coding or running any project commands
in the command line.

Note: If requirements.txt changes `py -m pip install -r requirements.txt` needs to rerun the virtual environment.