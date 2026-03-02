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
- [ ] 2.9: OpenLibrary API
  - [ ] 2.9.2: Pull n-amount of book results based on book title
  - [ ] 2.9.3: Pull n-amount of book results based on author name
- [ ] 2.1: Create function to use pulled information from the OpenLibrary API to add to book database (US201 and US202)
- [ ] 3.1: Begin Frontend and Backend Integration
- [ ] 3.2: Data Disparity Resolution Between Local and OpenLibrary Data
- [ ] 2.6: Mediator Module Refinement
  - [ ] 2.6.2: Mediator Functions for Update
  - [ ] 2.6.3: Mediator Functions for Delete
  - [x] 2.6.4: Mediator Functions tie-in to CRUD functions
[ ] 2.13: Start Creating Testing Suite
[ ] 3.9: Deprecate CRUD files outside of services

### Theme: UI Tasks
- [ ] 3.4: Create note frontend for book notes. (US505)
- [ ] 3.5: Create OpenLibrary API search frontend. (US506)
- [ ] 3.6: add_book.html Cleanup and Fixes
  - [ ] 3.6.1: Make the form less vertical, utilize more horizontal space.
  - [ ] 3.6.2: Make second author input a collapsible  that defaults to being collapsed?
- [ ] 3.7: view_book.html Fixes and Additions
  - [ ] 3.7.1: Change Total Chapters Input to only show when user clicks edit (add two buttons and a number input)
  - [ ] 3.7.2: Edit functionality for summary (adds two buttons and a text form)
  - [ ] 3.7.3: Add save button to tags to commit changes
    - Note: Should only be shown once a user toggles any of the tags
  - [ ] 3.7.4: Delineate the note button better
    - Note: Maybe switch update and note buttons
    - Note: Maybe add a left-hand offset to note button to make it more prominent

## Sprint 4
### Theme: Business Logic Tasks
- 4.1: Create user settings.
- 4.2: Create settings functionality for changing themes. (US401)
- 4.3: Create export/import CSV function. (US402)
- 4.4: Create database purge function. (US403)
- [ ] 4.5: Using existing database functionality, transition to using Flask's idiomatic way of using SQLite

### Theme: UI Tasks
- [ ] 1.4: Create the homepage frontend. (US501)
- 4.5: Create the analytics frontend. (US507)
- 4.6: Create the user settings frontend. (US508)

## Sprint 5
### Theme: Float
(Push any tasks here as needed)

### Theme: QA/QC
- 5.1: User can download 1.0 release and use application on supported hardware. (US601)
- 5.2: Make sure implementation of API follows documentation. (US602)
- 5.3: Make sure color and contrast ADA standards for the UI are followed. (US603)




