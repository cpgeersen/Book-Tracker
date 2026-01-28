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
{ Provide a broad, high-level statement that articulates the desired outcome of the project. 
For example: “provide excellent customer service”}

The project goal is to provide a user maintainable book database that allows one to track owned books and have enhanced
functionality by pulling book data from OpenLibrary's API.


### Project Objectives
{List at least 3 specific, measurable, achievable, relevant, and time-bound (SMART) target that a project aims to 
achieve. It outlines the tangible outcomes or results that the project intends to deliver. 
For example: “reduce customer wait time to one minute” }
1. Objective 1: Develop a normalized local book database with CRUD functionality.
2. Objective 2: Develop a user-friendly Graphical User Interface, following ADA color and contrast standards.
3. Objective 3: Ensure Windows, macOS, and Linux compatibility.
4. Objective 4: Ensure proper usage of the OpenLibrary API following OpenLibrary's documentation. 

### Project Scope
{Specify the boundaries and extent of the project, outlining what is included and what is excluded. Provides a clear 
understanding of the project's focus.}

In-Scope:
- User Book Database:
  - Create-Read-Update-Delete (CRUD) Book Data
  - Premade Labels: owned, favorite, read, currently reading, and whether personal or academic reading
  - Track chapters completed per book (two options user provided chapters or pages) (???)
  - Allow the addition of notes per book
  - Store cover images for added books (does not use much storage) (???)
- Querying Book Database:
  - Return all books in database
  - Return all books from an author, year, genre, and off of labels
- Querying OpenLibrary API:
  - Prevent request for books already in database
  - Return data for an ISBN or title search
  - Return only 10 results at a time for title search
- User Metrics:
  - Display stats like: completed books, number of books in database, and favorite genre
  - Display current books
  - How many books completed over a period of time
  - Recommendations from uncompleted books in database(???)
- User Settings:
  - Theme for UI
  - Username (only for when referring to the user)
  - Export/import database as CSV for backups
  - Average page reading time (to calculate estimated completion time)
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

### Project Assumptions
{List any factors or conditions that are considered to be true, real, or certain for planning purposes but have not 
been confirmed. The assumptions made that could impact the ability of the project team to achieve the project 
objectives.}

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
{List any limitations or restrictions that can impact the planning, execution, and completion of a project. 
Specify the known dependencies that could constrain the ability of the project team to achieve the project objectives.}

### Project Resources Required
{List assets, tools, personnel, and materials required for the successful planning, execution, and 
completion of a project.}

### Team Collaboration and Communication 
{Specify the collaboration and communication tools / platforms that will be used in this project development. 
Describe how your group will use these tools / platforms during this project development.}

### Project Documentation 
{Specify the documentation tools / platforms that will be used in this project development. 
Describe how your group will use these tools / platforms during this project development.

### Project Management Plan and Methodologies
{Specify what project management methods and tools will be used in this project development. 
Describe how your group will use these project management methods and tools during this project development.}
