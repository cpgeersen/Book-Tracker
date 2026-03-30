# Tasks

## Sprint 1
### Theme: Business Logic Tasks
- [x] 1.1: Create database.
- [x] 1.2.1 - Create Book Record (US101)
- [x] 1.2.2 - Read Book Record (US102)
- [x] 1.3: Create backend logic for a user function to add notes to a book record. (US105)
- [x] 1.6: Create initial Mediator Module for helper functions.

### Theme: UI Tasks
- [x] 2.2: Create frontend for local search of the database. (US503)
  - [x] 2.2.1: Include search box with search button
  - [x] 2.2.9: Allow up to 10 book results per page.
- [x] 1.5: Create frontend for book database form to add books manually to local database. (US502)
  - [x] 1.5.1: Must provide an ISBN
  - [x] 1.5.2: Must provide a book title
  - [x] 1.5.3: Must provide an author, with optional second author
  - [x] 1.5.4: Must add publish year
  - [x] 1.5.5: Add publisher
  - [x] 1.5.6: Add chapter total
  - [x] 1.5.7: Can check any of the tags


## Sprint 2
### Theme: Business Logic Tasks
- [x] 2.5: Create functions that incorporates CRUD functions
  - [x] 2.5.1: Create Full Book Record
  - [x] 2.5.2: Read Full Book Record
  - [x] 2.5.3: Update Full Book Record
  - [x] 2.5.4: Delete Full Book Record
- [x] 2.7: Further develop CLI app to test new features
- [x] 1.2: Create user CRUD functionality. (US101 to US104)
  - [x] 1.2.3: Update Book Record
  - [x] 1.2.4: Delete Book Record
- [x] 2.8: Initial Interaction with OpenLibrary API
- [x] 2.11: Additional Read Functions for:
  - [x] 2.11.1: Read Book Record by Title
  - [x] 2.11.2: Read Book Record by Author
  - [x] 2.11.3: Read Book Record by Genre
- [x] 2.12: Refactor Routes
- [x] 2.9.1: Pull all required book data for an ISBN search
- [x] 2.6.1: Mediator Functions for Read

### Theme: UI Tasks
- [x] 2.4: Expand local search functionality to match requirements. (US503)
  - [x] 2.4.1: Have a back and home buttons.
  - [x] 2.4.2: Have radio buttons to either search for ISBN, Book Title, or Author.
  - [x] 2.4.3: Have placeholder book cover image for when is not present.
  - [x] 2.4.4: Each book result must have (if available information): author (and possible second author), publisher, publish date, Tags (owned, favorite, read, currently reading), and ISBN.
  - [x] 2.4.5: Show all books in database.
  - [x] 2.4.6: Filter on Tag element
  - [x] 2.4.7: Button to go to the individual book page.
- [x] 2.3: Create frontend for individual book view when clicking on a result. (US504)
- [x] 1.7: Add book manually genre functionality. (US502) 
- [x] 2.10: Frontend Scripting for Local Search

## Sprint 3
### Theme: Business Logic Tasks
- [x] 2.6: Mediator Module Refinement
  - [x] 2.6.2: Mediator Functions for Update
  - [x] 2.6.3: Mediator Functions for Delete
  - [x] 2.6.4: Mediator Functions tie-in to CRUD functions
- [x] 2.9: OpenLibrary API
  - [x] 2.9.2: Pull n-amount of book results based on book title
  - [x] 2.9.3: Pull n-amount of book results based on author name
- [x] 2.13: Start Creating Testing Suite
- [X] 3.1: Begin Frontend and Backend Integration
- [x] 3.2: Data Disparity Resolution Between Local and OpenLibrary Data
  - [x] Task 3.2.1 - Case: ISBN already present in database
  - [x] Task 3.2.2 - Case: Book not in OL database
  - [x] Task 3.2.3 - Case: Same book different ISBN
  - [x] Task 3.2.4 - Case: Adding a new book from OL where author/publisher was added to database by user
- [x] 3.8: Deprecate CRUD files outside of services
- [x] 3.3: Most commonly read genre function
- [x] 3.11 Database Analytics Functions
- [x] 3.12: Create Note Backend Functionality
- [x] 3.13: Create Cover Image Backend Functionality
- [x] 3.14: Add Cover Image upload functionality
- [x] 3.15: Proper usage of /book/{isbn} for individual book pages
- [x] 4.1: Create user settings.
- [x] 4.7: Correct User Settings to match pseudocode and more current project requirements
- [x] 4.8: Refactor Analytics Functions to remove out-of-scope functionality (refer to Project Development Plan)


### Theme: UI Tasks
- [x] 1.4: Create the homepage frontend. (US501)
- [x] 3.4: Create note frontend for book notes. (US505)
- [x] 3.5: Create OpenLibrary API search frontend. (US506)
- [x] 3.6: add_book.html Cleanup and Fixes
  - [x] 3.6.1: Make the form less vertical, utilize more horizontal space.
  - [x] 3.6.2: Make second author input a collapsible  that defaults to being collapsed?
- [x] 3.7: view_book.html Fixes and Additions
  - [x] 3.7.1: Change Total Chapters Input to only show when user clicks edit (add two buttons and a number input)
  - [x] 3.7.2: Edit functionality for summary (adds two buttons and a text form)
  - [x] 3.7.3: Add save button to tags to commit changes
    - Note: Should only be shown once a user toggles any of the tags

## Sprint 4
### Theme: Business Logic Tasks
- [x] 2.1: Create function to use pulled information from the OpenLibrary API to add to book database (US201 and US202)
- [ ] 3.2.5 - Case: Updating a Locally added book with OL data
- [x] 4.3: Create export/import CSV function. (US402)
- [x] 4.4: Create database purge function. (US403)
- [ ] 4.11: Tag filter functionality
- [ ] 4.12: Genre filter functionality
- [ ] 4.13: Implement proper back button functionality based on current route
- [ ] 4.19: Cache OpenLibrary searches with JSON
- [ ] 4.22: Finalize OpenLibrary Functionality


### Theme: UI Tasks
- [ ] 4.2: Create themes (US401)
- [ ] 4.5: Create the analytics frontend. (US507)
- [ ] 4.6: Create the user settings frontend. (US508)
- [ ] 4.8: Individual book page edits
  - [ ] 4.8.1: Fix cover image sizing to be fixed
  - [ ] 4.8.2: Fix spacing of page
  - [ ] 4.8.3: Add styling to buttons that are missing styling
- [x] 4.9: Add styling to individual book page pop-ups
  - [x] 4.9.1: Deletion Pop-up
  - [x] 4.9.2: Update OL Pop-up
- [x] 4.10: Genre Edit Frontend
- [ ] 4.14: Fix author input spacing in add book form
- [ ] 4.15: Add hover animations
- [x] 4.16: Add error modals for pages using flask extends
- [ ] 4.17: Add go to top of page button for search frontends
- [x] 4.18: Create error status code frontend pages
  - [x] 4.18.1: Status Code 500
  - [x] 4.18.2: Status Code 404
- [ ] 4.20: Local Search Edits
  - [ ] 4.20.1: Align filters with page title rather than nav bar
  - [ ] 4.20.2: Make filters in search frontend collapsible
  - [ ] 4.20.3: For book card results, move book page button link to right-middle
  - [ ] 4.20.4: Add genres into book card
- [ ] 4.21: Finalize OpenLibrary Search Frontend

## Sprint 5
### Theme: Business Logic Tasks
- [ ] 4.5: Using existing database functionality, transition to using Flask's idiomatic way of using SQLite

### Theme: UI Tasks
- 5.4: Better UI scaling for larger screen resolutions
- - [ ] 5.5: Move CSS to static flask folder

### Theme: Float
(Push any tasks here as needed)

### Theme: QA/QC
- 5.1: User can download 1.0 release and use application on supported hardware. (US601)
- 5.2: Make sure implementation of API follows documentation. (US602)
- 5.3: Make sure color and contrast ADA standards for the UI are followed. (US603)




