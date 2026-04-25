# CSC289 Programming Capstone Project


Project Name: BookTracker

Team Number: 2

Team Project Manager: Collin Geersen

Team Members: Joseph Candleana, Collin Geersen, Mireliz Gimenez, Holly Green, Nicholas Grudier, Christopher O'Brien

 

## Release Report BookTracker - Version 1.0

 

### Overview [Collin]

[Provide a brief overview of the purpose of the software and the significance of this release.]

This software enables a user to maintain a local database to track books with a graphical user interface. 
The book information tracked can be as basic as ISBNs and titles to book genres and user defined notes. 
In conjunction with allowing a user to add books with their own information, it can pull data from an API to 
create or update books. With rich searching features and user tags, a user can organize their book backlog.

This release marks the first usable version with all the user functionality included. Additionally, it 
is the first version that is to be released for public use. A user has a choice of a Python wheel or 
Docker image. 

### Development Highlights

- Project Initiation [Holly]:

    The project’s official kickoff meeting took place on January 28, 2026.  During this meeting, the development team 
    reviewed the software requirements specification (SRS) documentation and determined the project’s scope and goals.  
    The team also reviewed the project timeline, which consisted of five two-week sprints dedicated to feature development 
    and implementation. 

- Requirements Gathering [Holly]:

    The development team held sessions with identified stakeholders, customers, and end-users to gather project requirements. Feedback from these meetings determined in-scope software features and functionalities to focus build. The following user stories were identified and prioritized for project development:

        - As a user, I want to add a book to the database so that I can maintain a backlog of books.
        - As a user, I want to mark off the completion of chapters in a book so that I can track my progress for a given book.
        - As a user, I want to search the database for a specific book so that I can see the completion status of a given book.
        - As a user, I want to export/import the database as a CSV so that I can back up the database.

- Design and Architecture [Collin]:

    [Explain the design decisions and architectural considerations.]

- Development Progress [Collin]:

    [Highlight key development milestones, challenges, and achievements.]

- Testing and Quality Assurance [Holly]:

    Comprehensive automated unit and integration testing was developed and performed using pytest capabilities to ensure software features functioned as expected, both separately and in tandem.  This included testing for the Open Library API integration to ensure desired information was pulled and formatted correctly to meet project needs.  

    Acceptance testing was performed by the development team and end-users to ensure software functioned as expected and met usability standards.  Reported issues, such as slow transition styling for submission buttons, were corrected to improve the user’s experience.  

    To further improve end-user experience, background, button, and text color themes utilized for page styling underwent contrast testing for ADA accessibility.  The team determined theme colors passed at least one or both WCAG AA and WCAG AAA standards for normal and large text.  Button styling met WCAG AA standards for graphical objects and interface components. 

- Bug Fixes and Enhancements [Collin]:

    [List any bugs that were fixed and enhancements that were implemented in this release.]

 

### Deployment [Nick/Collin]

For deployment, I packaged my Book Tracker app into a Python wheel (.whl). This allowed me to distribute the application as a built package instead of sending the raw source code.

I generated the wheel using my project’s setup configuration, then transferred the .whl file to the deployment environment. Once it was uploaded, I installed it using pip install <filename>.whl, which placed all the modules and dependencies into the environment.

After installation, I configured the runtime environment and started the application. The deployment itself was quick because the wheel contained everything needed to run the app.

During deployment, I encountered a few issues. One problem was missing dependencies that weren’t included in the wheel at first, which caused the app to fail on startup. I rebuilt the wheel with the correct dependencies and redeployed. There was brief downtime while I fixed this, but once the updated wheel was installed, the app ran without further issues.

Using a wheel file made the deployment process clean and repeatable, and after resolving the initial dependency issues, the app deployed successfully



### Release Notes

- New Features [Holly]:

    Book Tracker software release version 1.0.0 includes features that allow avid book readers to create their own personal database to track book inventory and completion progress.  These features include:

        - Manually add a book to user's database.
        - Add book to user's database by searching and selecting from Open Library's online database.
        - Add personalized tags to mark books as owned, favorite, personal, or academic.
        - Search user's database by ISBN, author, or title to locate specific book(s).
        - Further filter search results by tags or genre.  
        - Update book information manually or pull from Open Library.
        - Ability to remove duplicate books from user's database.
        - Analytic capabilties for tracking books in database, including owned, completed, reading, and favorite genre.
        - Export user's database to CSV file for backup purposes.
        - Ability to import a CSV file to populate user's database. 
        - Customize application appearance by choosing between light and dark themes. 

- Bug Fixes [Collin]:

    [List and describe any bugs that were fixed in this release.]

- Known Issues [Everyone]:

    [List any known issues or limitations in the release, along with plans for addressing them.]

    Book Tracker version release 1.0.0 is limited to English language users.  Translation to other languages, such as Spanish, may be explored in future releases. 



### Conclusion (Chris)

[Summarize the key outcomes of this release and discuss any future plans or considerations.]
