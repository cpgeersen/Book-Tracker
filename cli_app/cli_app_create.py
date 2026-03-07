def main():
    while True:
        try:
            print('---------------------')
            print('1 - Create a New Book Record')
            print('2 - Exit')
            print('---------------------')
            user_choice = int(input('Choose an Option: '))
            if user_choice == 1:
                print('Creating New Book Record')
            elif user_choice == 2:
                print('Exiting')
                break
            else:  # Any other value
                continue
        except ValueError as error:
            print(f'Input must be an integer 1-2: {error}')


if __name__ == '__main__':

    main()
