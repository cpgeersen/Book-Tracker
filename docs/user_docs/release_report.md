# CSC289 Programming Capstone Project

**Project Name**: BookTracker

**Team Number**: 2

**Team Project Manager**: Collin Geersen

**Team Members**: Joseph Candleana, Collin Geersen, Mireliz Gimenez, Holly Green, Nicholas Grudier, Christopher O'Brien

## Release Report BookTracker - Version 1.0

### Overview:

This software enables a user to maintain a local database to track books with a graphical user interface. 
The book information tracked can be as basic as ISBNs and titles to book genres and user defined notes. 
In conjunction with allowing a user to add books with their own information, it can pull data from an API to 
create or update books. With rich searching features and user tags, a user can organize their book backlog.

This release marks the first usable version with all the user functionality included. Additionally, it 
is the first version that is to be released for public use. A user has a choice of a Python wheel or 
Docker image. 

### Development Highlights

- **Project Initiation**:

    The project’s official kickoff meeting took place on January 28, 2026.  During this meeting, the development team 
    reviewed the software requirements specification (SRS) documentation and determined the project’s scope and goals.  
    The team also reviewed the project timeline, which consisted of five two-week sprints dedicated to feature development 
    and implementation.


- **Requirements Gathering**:

    The development team held sessions with identified stakeholders, customers, and end-users to gather 
    project requirements. Feedback from these meetings determined in-scope software features and functionalities to 
    focus build. The following user stories were identified and prioritized for project development:

        - As a user, I want to add a book to the database so that I can maintain a backlog of books.
        - As a user, I want to mark off the completion of chapters in a book so that I can track my progress for a given book.
        - As a user, I want to search the database for a specific book so that I can see the completion status of a given book.
        - As a user, I want to export/import the database as a CSV so that I can back up the database.

- **Design and Architecture**:

  Given the team's main skill sets, we decided on programming the project in Python. This gave us the needed flexibility
  for our diverse team. Since Python was decided, we opted to use flask as the framework to create the app. This decision
  came from the simplicity and power that fit our projects needs. Something like Django would have been unnecessary.
  
  <br>

  It was also decided as a team that we would use SQLite for the in-app database. This differs from the SRS where Oracle was
  picked. Upon consideration, it was determined that Oracle would add unnecessary project complexity. Also, given that the
  project is using flask, Python's native support for SQLite made more sense.

  <br>

  For maximum agility and separation of the front and back ends, we used the Model-View-Presenter architectural model.
  This application design decouples the front and back end, allowing for both ends to be created in parallel.


- **Development Progress**:
  - Key milestones:
    - Sprint 1 we finalized project decisions and the database schema
    - Sprint 2 we finished database functions
    - Sprint 3 we began integrating the front and back ends
    - Sprint 4 we began integrating OpenLibrary functionality into the main app
    - Sprint 5 we finished the initial version, fixed bugs, and created various ways for a user to install the app
  - Challenges:
    - Creating proper releases that a user can install
    - Accounting for data disparities that can arise from user data and OpenLibrary data
  - Achievements:
    - Three ways for a user to install the application
    - A scalable and performant local application
    - Can run on any mainstream desktop platform (Windows 10+. macOS, and Linux)
    - Flexible UI with a light and dark mode
    - In-app import and export functionality


- **Testing and Quality Assurance**:
    <br>
    Comprehensive automated unit and integration testing were developed and performed using pytest's capabilities to 
    ensure software features functioned as expected, both separately and in tandem. These tests reached the industry standard
    of 80% code coverage. Additionally, the unit and integration tests were integrated into GitHub for Continous Integration.
    This included testing for the OpenLibrary API integration to ensure desired information was pulled 
    and formatted correctly to meet project needs.
    
    <br>
    
    Acceptance testing was performed by the development team and end-users to ensure software functioned as expected 
    and met usability standards.  Reported issues, such as slow transition styling for submission buttons, were 
    corrected to improve the user’s experience.  
    
    <br>

    To further improve end-user experience, background, button, and text color themes utilized for page styling 
    underwent contrast testing for ADA accessibility.  The team determined theme colors passed at least one or 
    both WCAG AA and WCAG AAA standards for normal and large text.  Button styling met WCAG AA standards for 
    graphical objects and interface components. 

    <br>

    Thinking ahead for future releases, we did performance testing for a large amount of books. If a user has a database
    with over a thousand books, it still runs well.


- **Bug Fixes and Enhancements**:
  <br>
  All major bugs were introduced and found while implementing the features and enhancements for this release were fixed.
  The main bug fixes stem from data integrity from user and API input, proper routing for flask, and having an installable
  release for users. Most of the bugs were corrected via error checking, testing, and validation.

  The enhancements for this release are all the features listed, since this is the initial release of version 1.0. This
  includes all user functionality with the database, OpenLibrary API interaction, user profile, searching, analytics, and
  themes.

### **Deployment** [Nick/Collin]

For deployment, we packaged the BookTracker app into a Python wheel (.whl) and a Docker Image. This allowed us to 
distribute the application as a built package instead of sending the raw source code (which is still an option for a user).

For the Python wheel, we generated it by using the project’s setup configuration, then transferred the .whl file 
to the deployment environment. Once it was uploaded, it can be installed by using pip install <filename>.whl, 
which places all the modules and dependencies into the user environment.

After installation, the configured runtime environment can start the application. The deployment itself is quick 
because the wheel contains everything needed to run the app.

During deployment, we encountered a few issues. One problem was missing dependencies that weren’t included in the wheel 
at first. This caused the app to fail on startup. We rebuilt the wheel with the correct dependencies and redeployed. 
There was a brief downtime while we fixed this, but once the updated wheel was installed, the app ran without further 
issues. Until the code was refactored to change directories. The wheel needed to be updated to accomandate these changes.

Using a wheel file made the deployment process clean and repeatable, and after resolving the initial dependency issues, 
the app deployed successfully.


For the Docker Image...


### Release Notes

- **New Features**:

    Book Tracker software release version 1.0.0 includes features that allow avid book readers to create their own 
    personal database to track book inventory and completion progress.  These features include:

        - Manually add a book to user's database.
        - Add book to user's database by searching and selecting from OpenLibrary's online database.
        - Add personalized tags to mark books as owned, favorite, currently reading, and personal or academic.
        - Track book chapter progress
        - Add user notes to a book
        - Search user's database by ISBN, author, or title to locate specific book(s).
        - Further filter search results by tags or genre.  
        - Update book information manually or pull from OpenLibrary.
        - Ability to remove duplicate books from user's database.
        - Analytic capabilties for tracking books in database, including owned, completed, reading, and favorite genre.
        - Export user's database to CSV file for backup purposes.
        - Ability to import a CSV file to populate user's database. 
        - Customize application appearance by choosing between light and dark themes.
        - In-app help on every page.

- **Bug Fixes**:
  - Fixed cover image regression for the cover image folder failing to be created
  - Fixed Dockerfile listening to the wrong host port
  - Fixed Python wheel regression from CSS and HTML refactor
  - Fixed improper pulling of foreign author name from the OpenLibrary API
  - Fixed regression in local author name search failing to search with middle names


- **Known Issues** [Everyone]: [List any known issues or limitations in the release, along with plans for addressing them.]
  - Book Tracker version release 1.0.0 is limited to English language users. 
  Translation to other languages, such as Spanish, may be explored in future releases.
  - Database backups do not back up cover images
  - Searching via OpenLibrary can pull no information for a valid search, this occurs when the result
  from OpenLibrary is missing information and cannot be used for the database.
  - Use the OpenLibrary rapidly can time the user out. This is to prevent overloading the API.


### **Conclusion** (Chris)

[Summarize the key outcomes of this release and discuss any future plans or considerations.]
