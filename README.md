# Book-Tracker
CSC-289 Capstone Project - Book Tracker Source Code

## Project Objectives  
The primary goals of the software are to develop an application that allows a user to maintain a database for books. This database will track completed books compared to a backlog. This application will allow users to track progress and generate insights into their reading habits. 

## Data Assumptions: 
1. Assumes data will be available from the Open Library Book data API.
2. Assumes most books can be retrieved from the Open Library Book data API.
3. Assumes if the Open Library Book API is down or unavailable, a user can manually add and search books from local database. 

## Project Features / Functions 
#### (I) Book Management:
1. Create, read, update, and delete book records from user database.
2. Book data will come from the open-source OpenLibrary book database API.
3. Create, read, update, and delete notes per book.
4. Search for a specific book in the local database.
5. Export/import CSV function
  
#### (II) Categorize By:
1. Author
2. Genre
3. Publish Date
4. Publisher
5. Premade Labels
  
#### (III) Progress Tracking:
1. Apply premade tags to books:
    - Owned
    - Currently Reading
    - Read
    - Favorite
2. Mark off each chapter of a book to track per book progress.
    
#### (IV) Analytics:
1. A dashboard that shows:
    - Number of books in database.
    - Number of completed books.
    - Most read genre
    - Currently reading books.
    - Number of books completed over a period of time (by month over a year). 

#### (V) Customization:
1. Theme options
2. Username (only for when referring to the user)


