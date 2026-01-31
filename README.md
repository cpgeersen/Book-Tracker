# Book-Tracker
CSC-289 Capstone Project - Book Tracker Source Code

## Project Objectives  
The primary goals of the software are to develop an application that allows a user to maintain a database for books. This database will track completed books compared to a backlog. This application will allow users to track progress and generate insights into their reading habits. 

## Data Assumptions: 
<p> (1) Assumes data will be available from the Open Library Book data API. 
<p>(2) Assumes most books can be retrieved from the Open Library Book data API. 
<p>(3) Assumes if the Open Library Book API is down or unavailable, it can search the cache for potential results. 

## Project Features / Functions 
<h4> (I) Book Management:</h4>
<p> (1) Add/delete books to/from their database.
<p> Book data will come from the open-source book API from the Open Library.
<p> Add/edit/delete notes per book.
<p> Search for a specific book in the database.
<h4>(II) Categorize By:</h4>
<p>(1) Author 
<p>(2) Genre
<p>(3) Publish Date
<p>(4) Publisher
<h4>(III) Progress Tracking:</h4>
  <p>(1) Mark a book as owned.
  <p>(2) Apply premade tags to books.
  <p>(3) Currently Reading
  <p>(4) Read
  <p>(5) Favorite
  <p>(6) Mark of book progress per chapter with an included overall completion status.
<h4>(IV) Analytics: </h4>
  <p>(1) Give recommendations for books based on the books in the database on author, series, or genre. 
  <p>(2) Estimate the time required to complete a book based on the number of pages and user provided average reading time per page. 
 <p>(3) A dashboard that shows: 
 <p>(4) Current books are being read. 
  <p>(5) Average chapters read over time. 
  <p>(6) Currently, most read genres. 
<h4>(V) Customization: </h4>
  <p>(1) Allow the user choice of a set of premade themes that can change the user interface color. 
