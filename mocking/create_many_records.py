import os
import shutil
import random
from app.services.Book.Book import create_book

first_names_list = ['Collin', 'Nick', 'Holly', 'Joseph', 'Christopher', 'Mireliz', 'John',
                    'Jane', 'Clive', 'Bert', 'Leon', 'Ashley', 'Alex', 'Eve', 'Alan', 'Sarah',
                    'Hannah', 'Luke', 'Sean', 'Nigel', 'Kiki', 'Ellen', 'Liam', 'Lucy', 'Nicole',
                    'Tom', 'Nancy', 'Ursula', 'Shirley', 'Stephen', 'Howard', 'Louise', 'Emma',
                    'Richard', 'Hugh', 'Vincent', 'Scott', 'Jackie', 'Gavin', 'Will', 'Lana',
                    'Michael']
last_names_list = ['Doe', 'Kain', 'King', 'Barker', 'Locke', 'Nixon', 'McVeigh', 'Sanders',
                   'Chen', 'Jackson', 'Wilson', 'Lane', 'Lynn', 'Washington', 'Kwan', 'Wells',
                   'Goldstein', 'Hayes', 'Simpson', 'Robertson', 'Lowe', 'Perez', 'Lesly',
                   'Morales', 'Lee', 'Rossi', 'Das', 'Petrov', 'Larsen', 'Silva', 'Lyons',
                   'Rhodes', 'Saxon', 'Salinger', 'Harrington', 'Summers', 'Dalton', 'Jones',
                   'Bishop', 'Wright', 'Dixon', 'Wesley']


publisher_list = ['Random House', 'Penguin', 'Addison-Wesley', 'Harper', 'MacMillian',
                  'Pearson', 'Putnam', 'Simon and Schuster', 'Wiley', 'Scholastic', 'Indie Press',
                  'Self Published', 'Scribner', 'Tor', 'Doubleday', 'Del Rey Books', 'Deep Vellum',
                  'Hachette', 'Signet']

title_list_1 = ['The', 'By', 'A', 'What','Many','Let', 'How']
title_list_2 = ['Chaos', 'Metal', 'Group', 'Lane', 'Lamp', 'Total', 'Disobedience', 'Terror',
                'Brute', 'Revolution',  'Kite', 'Computer', 'Mind', 'House', 'World', 'Wrong',
                'Spear', 'Bird', 'Swamp', 'Nature', 'Mud', 'Digit', 'Class', 'Death', 'Parents',
                 'Fall', 'Health', 'Few', 'Men', 'Women', 'Children', 'Woe', 'Loss', 'Reason',
                'Something', 'Con', 'Mirror', 'Stand', 'Broken', 'Real', 'Dog', 'Cat', 'End',
                'Flight', 'Up', 'Down', 'Time', 'Search', 'Help', 'Lone', 'North', 'South',
                'West', 'East', 'Lost', 'Painting', 'Future', 'Dragon', 'King', 'Queen', 'Prince',
                'Princess', 'Noise', 'Hill', 'City', 'State', 'County', 'Country', 'Town',
                'Cut', 'People', 'Mystery', 'Case', 'Affair']

tag_list = ['yes', 'no']
tag_list_personal_or_academic = ['personal', 'academic']

genre_1_list = ['fiction', 'nonfiction']
genre_list = ['speculative fiction', 'fantasy', 'science fiction', 'horror',
              'historical fiction', 'dystopian', 'mystery', 'detective', 'romance', 'action',
              'adventure', 'paranormal', 'literature', 'classic', 'postmodern', 'baby',
              'children', 'young adult', 'legend', 'epic', 'myth', 'folklore', 'fairy tale',
              'magic', 'suspense', 'crime', 'philosophy', 'drama', 'humor', 'thriller', 'animals',
              'coming-of-age', 'military', 'realist', 'education', 'religion', 'wellness',
              'self-help', 'cooking', 'exercise', 'science', 'biology', 'chemistry', 'physics',
              'programming', 'math', 'language', 'business', 'art', 'film', 'music', 'design',
              'photography', 'dance', 'painting', 'history', 'anthropology', 'archaeology',
              'politics', 'geography', 'psychology', 'novel', 'novella', 'short-stories', 'poetry',
              'play', 'essay', 'autobiography', 'biography', 'textbook', 'comic', 'graphic-novel',
              'manga', 'cookbook', 'anthology', 'picture book']

def create_many_records(num_of_records):
        #random.seed(24)

        # Shuffle the name lists for extra randomness
        random.shuffle(first_names_list)
        random.shuffle(last_names_list)

        # Generate information for each book record and create the book in database
        for record in range(num_of_records+1):
                # Generates ISBN 13 numbers
                isbn = random.randint(1000000000000, 9999999999999)

                # Generate year, favoring dates closer to modern times
                year = int(random.triangular(1650, 2026, 1920))

                # Generate the number of chapters for a book
                chapters = random.randint(1, 100)
                chapters_completed = random.randint(0, chapters)

                # Generate a name from the list
                author_first_name_1 = random.choice(first_names_list)
                author_last_name_1 = random.choice(last_names_list)

                # One-in-Twenty chance there is a second author
                another_author = random.randint(1, 20)
                if another_author == 20:
                    author_first_name_2 = random.choice(first_names_list)
                    author_last_name_2 = random.choice(last_names_list)
                else:
                    author_first_name_2 = ''
                    author_last_name_2 = ''

                # Generate a publisher from the list
                publisher_name = random.choice(publisher_list)

                # Get first part of a book title
                title_part_1 = random.choice(title_list_1)

                # Generate the other parts of a title (up to 3 more words)
                number_of_title_subjects = random.randint(1,3)
                title_part_2 = random.sample(title_list_2, k=number_of_title_subjects)

                title = title_part_1
                for subjects in title_part_2:
                        title += ' ' + subjects

                # Generate the tags for the book
                owned = random.choice(tag_list)
                favorite = random.choice(tag_list)
                completed = random.choice(tag_list)
                currently_reading = random.choice(tag_list)
                personal_or_academic = random.choice(tag_list_personal_or_academic)

                # Generate the genres for the book
                genre_1 = random.choice(genre_1_list)
                genres = random.sample(genre_list, k=3)

                # Generate cover images
                file_name = f'{isbn}_cover_image.jpg'
                file_path = os.path.join('app', 'static', 'images', 'cover_images', file_name)
                # Image Courtesy of: https://unsplash.com/photos/long-coated-black-and-white-dog-during-daytime-mx0DEnfYxic
                shutil.copy(os.path.join('mocking', 'baptist.jpg'), file_path)

                book = {"ISBN": f"{isbn}",
                        "Title": f"{title}",
                        "Publish_Year": f"{year}",
                        "Summary": "",
                        "Chapters": f"{chapters}",
                        "Chapters_Completed": f"{chapters_completed}",
                        "Cover_Image": f'/static/images/cover_images/{file_name}',
                        "Author_First_Name_1": f"{author_first_name_1}",
                        "Author_Last_Name_1": f"{author_last_name_1}",
                        "Author_First_Name_2": f"{author_first_name_2}",
                        "Author_Last_Name_2": f"{author_last_name_2}",
                        "Publisher_Name": f"{publisher_name}",
                        "Owned": f"{owned}",
                        "Favorite": f"{favorite}",
                        "Completed": f"{completed}",
                        "Currently_Reading": f"{currently_reading}",
                        "Personal_Or_Academic": f"{personal_or_academic}",
                        "Genre_1": f"{genre_1}",
                        "Genre_2": f"{genres[0]}",
                        "Genre_3": f"{genres[1]}",
                        "Genre_4": f"{genres[2]}"}

                create_book(book)


if __name__ == '__main__':
    pass














