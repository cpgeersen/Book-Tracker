# Git Workflow

> [!IMPORTANT]  
> All commits must be done in a separate working branch that will be merged via a pull request.
***
### Steps of pushing a feature branch:
1. Set up local environment if not already done:
    1. Clone the repo
       ```bash
       # Using git cli
       git clone https://github.com/cpgeersen/Book-Tracker.git
       ```
       or
       ```bash
       # Using gh cli
       gh repo clone cpgeersen/Book-Tracker
       ```
       or
       
       Use GitHub Desktop
       
    3. Set up Python virtual environment
       ```bash
       # Make sure the terminal is currently pointing to the project folder
       python -m venv .venv
       ```
    5. Activate Python virutal environment
       ```bash
       # Make sure the terminal is currently pointing to the project folder
       # Windows
       .venv\Scripts\activate
       # Linux
       .venv\bin\activate
       ```
    7. Install requirements in Python virtual environment
       ```bash
       # Make sure the terminal is currently pointing to the project folder
       pip -r requirements.txt
       ```
2. Pull from main to make sure up-to-date
3. Create working branch for feature
4. Make logical commits
5. Push branch to repo
6. Submit a pull request from branch to merge to main
> [!IMPORTANT]  
> Only submit a pull request for functional code.
7. Code will be reviewed by Project Manager
8. Cleared code will be merged to main
***
### Simple edits (i.e. docs):
Can edit directly to main branch, but will still need to be merged through a pull request.
