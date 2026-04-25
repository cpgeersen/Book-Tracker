# CSC289 Programming Capstone Project


Project Name: {Book Tracker}

Team Number: {2}

Team Project Manager: {Collin Geerson}

Team Members: {Nicholas Grudier, Collin Gerrson, Christopher, Holly, Mireliz, Johnathon.}

 

## Software Installation Guide: [Software Name]

 

### Introduction

This guide provides the necessary steps to install and access the Book Tracker application from its official GitHub release. It outlines system requirements, prerequisites, and clear instructions to help users set up the software quickly and smoothly.

 

### System Requirements

Operating System: Windows, macOS, or Linux

Python Version: Python 3.9

Disk Space: 200 MB

Internet Connection: Required for some features

 

### Downloading the Installer

The Book Tracker application is distributed as a wheel file, which contains the packaged version of the software ready for installation. Users can download the installer directly from the official GitHub release page:

GitHub Release (Version 1.0.0):  
https://github.com/cpgeersen/Book-Tracker/releases/tag/1.0.0

On the release page, scroll to the Assets section and download the file labeled: **Book-Tracker-1.0.0.whl**

This wheel contains the full application package. 

 

### Installing the Software

## 1. Locate the Downloaded Wheel File
After downloading, navigate to the folder where the file was saved.
The file: book_tracker-1.0.0-py3-none-any.whl

## 2. Open a Terminal or Command Prompt

Windows: Press Win + R, type cmd, and press Enter

macOS: Open Terminal from Applications → Utilities

Linux: Open your preferred terminal application

## 3. Navigate to the Folder Containing the Wheel File
Use the cd command to move into the directory where the wheel file is located. For example:
**cd Downloads**

## 4. Install the Application Using pip
Run the following command:
**pip install book_tracker-1.0.0-py3-none-any.whl**

## 5. Install requirements
Run the following command:
**pip install -r requirements.txt**



### Launching the Software

## Navigate to the Project Directory
Open a terminal or command prompt and move into the folder where your application files are located. For example:

**cd path/to/book-tracker**

## Run Flask
**python -m flask run**

## Access the Application
Open a web browser and go to:
**http://localhost:5000**

Your Book Tracker app will now be running and accessible.

### Uninstalling the Software
If you no longer need the Book Tracker application, you can remove it easily using pip. Uninstalling the software will remove the installed package and its associated files from your Python environment.

1. Open a Terminal or Command Prompt:

Windows: Press Win + R, type cmd, and press Enter

macOS/Linux: Open Terminal

2. Uninstall the Book Tracker Package:
Run the following command:
**pip uninstall book_tracker-0.1.0-py3-none-any.whl**
