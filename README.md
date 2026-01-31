# Book-Tracker
CSC-289 Capstone Project - Book Tracker Source Code

## Project Objectives  
The primary goals of the software are to develop an application that allows a user to maintain a database for books. This database will track completed books compared to a backlog. This application will allow users to track progress and generate insights into their reading habits. 

## Data Assumptions: 
(1) Assumes data will be available from the Open Library Book data API. \n
(2) Assumes most books can be retrieved from the Open Library Book data API. \n
(3) Assumes if the Open Library Book API is down or unavailable, it can search the cache for potential results. \n 

## Project Features / Functions 
(I) Book Management: \n
  (1) Add/delete books to/from their database. \n
  (2) Book data will come from the open-source book API from the Open Library. \n
  (3) Add/edit/delete notes per book. \n
  (4) Search for a specific book in the database. \n
(II) Categorize By: \n
  (1) Author \n
  (2) Genre \n
  (3) Publish Date \n
  (4) Publisher \n
(III) Progress Tracking: \n
  (1) Mark a book as owned. \n
  (2) Apply premade tags to books. ]n
  (3) Currently Reading \n
  (4) Read \n
  (5) Favorite \n
  (6) Mark of book progress per chapter with an included overall completion status. \n
(IV) Analytics: \n
  (1) Give recommendations for books based on the books in the database on author, series, or genre. 
  (2) Estimate the time required to complete a book based on the number of pages and user provided average reading time per page. 
  (3) A dashboard that shows: 
  (4) Current books are being read. 
  (5) Average chapters read over time. 
  (6) Currently, most read genres. 
(V) Customization: 
  (1) Allow the user choice of a set of premade themes that can change the user interface color. 
