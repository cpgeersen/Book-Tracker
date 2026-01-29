# CSC289 Programming Capstone Project Plan


### Project Name: Book Tracker

### Team Number: 2

### Team Project Manager / Scrum Master: Collin Geersen
***

### Team Member Details
| Name      | Email                                       | Role                     |
| --------- | ------------------------------------------- |--------------------------|
| Collin Geersen         | cpgeersen@my.waketech.edu      | Project Manager          | 
| Brandon Prevatte       | bcprevatte@my.waketech.edu     |                          |
| Christopher O'Brien    | cmobrien3@my.waketech.edu      |                          |
| Holly Green            | hmgreen@my.waketech.edu        |                          |
| Joseph Candleana       | jrcandleana@my.waketech.edu    |                          |
| Mireliz Gimenez        | mgimenez@my.waketech.edu       |                          |
| Nicholas Grudier       | njgrudier@my.waketech.edu      |                          |

***

### Project Goal: Improve a User's Ability to Track and Maintain a List of Books
The project goal is to provide a user maintainable book database that allows one to track owned books and have enhanced
functionality by pulling book data from OpenLibrary's API.


### Project Objectives
1. Objective 1: Develop a local book database in 3NF with CRUD functionality within the project deadline.
2. Objective 2: Develop a user-friendly Graphical User Interface, following ADA color and contrast standards 
within project deadline.
3. Objective 3: Ensure Windows and Linux compatibility within project deadline.
4. Objective 4: Ensure proper usage of the OpenLibrary API following OpenLibrary's documentation 
within project deadline. 

### Project Scope
In-Scope:
- User Book Database:
  - Create-Read-Update-Delete (CRUD) Book Data
  - Premade Labels: owned, favorite, read, currently reading, and whether personal or academic reading
  - Track chapters completed per book
  - Allow the addition of notes per book
  - Store cover images for added books
- Querying Book Database:
  - Return all books in database
  - Return all books from an author, year, genre, and off of labels
- Querying OpenLibrary API:
  - Prevent request for books already in database
  - Return data for an ISBN, title, or author search
  - Return only 10 results at a time for title search
- User Metrics:
  - Display stats like: completed books, number of books in database, and favorite genre
  - Display current books
  - How many books completed over a period of time
- User Settings:
  - Theme for UI
  - Username (only for when referring to the user)
  - Export/import database as CSV for backups
- GUI:
  - Include all functions available in-scope to be done through the GUI

Out-of-Scope:
- No passwords or authentication
- No full database pulling from OpenLibrary
- No online features other than pulling data from API (i.e. cloud support or retailer integration)
- No additional information about authors or publishers will be included
- No timeing functionality
- No user reviews
- No cli
- Recommendations from uncompleted books in database
- Average page reading time (to calculate estimated completion time)

### Project Assumptions
Team Assumptions:
- Assumes that all teams members throughout the project will be available for communication and completion of tasks.
- Assumes all project deliverables will be submitted by Project Manager.
- Assumes all team members have an account with the tools being used for the project.
- Assumes all team members will use GitHub following an agreed on workflow.

OpenLibrary Assumptions:
- Assumes OpenLibrary's API is available at all times to pull information from.
- Assumes OpenLibrary does not change API endpoints.
- Assumes a book is in the OpenLibrary database.

User Assumptions:
- Assumes the user read books.
- Assumes the user has a supported platform.
- Assumes the user knows how to use a GUI.
- Assumes the user knows how to install Python.
- Assumes the user knows how to read a basic end-user readme.

Tech Stack Assumptions:
- Assumes all Python and Python libraries work together with the database.


### Project Constraints
Time Constraint: Project must be completed by the deadline of 4/17/26 to fulfill the team's Programming Capstone Project.

Team Constraint: Project is limited to the assigned members and cannot be increased if needed.

Communication Constraint: Project members can only meet digitally because of the distributed nature of the team.

### Project Resources Required
Physical Tools:
- Computer for every team member with the project environment

Programming Tools:
- IDE (i.e. VSCode or PyCharm)
- Python
- Database Management Tool

Personnel:
- Seven team members assigned to project
- Professor and/or mentor to consult

### Team Collaboration and Communication
Collaboration Tools: The two main collaboration tools utilized in this project will be GitHub and Trello.

GitHub will be used for version control of the source code of the project. GitHub allows the team to coordinate
and work asynchronously on different parts of the project. Team members will follow basic GitHub workflows utilizing
branches, pull requests, and issues. Additionally, GitHub will allow for CI/CD with GitHub actions to maintain project
quality and assurance.

Trello will be used to track and assign tasks that correlate will story epics and user stories. Trello is mainly
used for the facilitation of Agile methodology.

Communication Tools:
The main collaboration tool used for communication over the course of the project is Microsoft Teams. MS Teams will
be the platform that we will have our virtual meetings. Additionally, MS Teams allows for team members to chat in
text channels for quick communication.

### Project Documentation
The two documentation tools that will be used are GitHub and Microsoft Teams. The main one being GitHub. Documentation
for the project and code will be housed in the /docs folder in the repository. This allows for documentation to be
version tracked and also be in the same place as the source code. This is possible since the main file used for
documentation is markdown. Existing files like the SRS or ones given in non-markdown will be housed in the files section
of the MS Teams channel. These documents will be organized into folders by sprint.

### Project Management Plan and Methodologies
The project methodology that will be utilized is Scrum, with Kanban features. The project manager will also act as
Scrum Master. Scrum, being an Agile methodology, is perfect for the given project. Scrum allows our team to iterate 
through sprints that will add new in-scope features and ship them at the end of each sprint. Even though at the end
of each sprint all features may not be added, a usable version will be available. Since we are using Scrum, Trello
is a perfect facilitator. Trello allows for the creation of Story Epics and User Stories. Using these two, tasks can
be generated and assigned to team members with a Kanban board.