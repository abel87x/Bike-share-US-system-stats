import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv', 'new york city': 'new_york_city.csv', 'washington': 'washington.csv' }
city_dict = {'a':'chicago', 'b':'new york city', 'c':'washington'}
months_dict = {'a':'january', 'b':'february', 'c':'march', 'd':'april', 'e':'may', 'f':'june', 'h':'all'}
days_dict = {'a':'saturday', 'b':'sunday', 'c':'monday', 'd':'tuesday', 'e':'wednesday', 'f':'thursday', 'h':'friday', 'i':'all'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city_letter = input("Would you like to see the data for Chicago, NewYork or Washington? \n a: for Chicago\n b: for NewYork\n c: for Washington\n").lower()
            print('\n')
            if city_letter in ['a','b','c']:
                break
            else:
                print("invalid input! please re-enter your input")
        except KeyboardInterrupt:
            print("invalid input! please re-enter your input\n")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            print("Would you like to filter by a certain month or choose all(no filter)?\n")
            print("Choose:\n a: for January\n b: for February\n c: for March\n d: for April\n e: for May\n f: for June\n h: for all\n")
            month_letter = input().lower()
            print('\n')
            if month_letter in ['a','b','c','d','e','f','h']:
                break
            else:
                print("invalid input! please re-enter your input\n")
        except KeyboardInterrupt:
            print("invalid input! please re-enter your input\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            print("Would you like to filter by a certain day or choose all(no filter)?\n")
            print("Choose:\n a: for saturday\n b: for Sunday\n c: for Monday\n d: for Tuesday\n e: for Wednesday\n f: for Thursday\n h: for Friday\n i: for all")
            day_letter = input().lower()
            print('\n')
            if day_letter in ['a','b','c','d','e','f','h','i']:
                break
            else:
                print("invalid input! please re-enter your input\n")
        except KeyboardInterrupt:
            print("invalid input! please re-enter your input\n")

    city = city_dict[city_letter]
    month = months_dict[month_letter]
    day = days_dict[day_letter]
    #return city, month, day
    return(city, month, day)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    print("\nPrinting a sample of the original unfiltered data:\n")
    print(df.head())
    print('')

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month != 'all':
        print("\nSince you've used the months filter, the only month presented here is {} and most common month is meaningless".format(month.title()))
    else:
        print("\nMost common month is {}".format(df['month'].mode()[0]))


    # display the most common day of week
    if day != 'all':
        print("\nSince you've used the days filter, the only day presented here is {} and most common day is meaningless".format(day.title()))
    else:
        print("\nMost common day is {}".format(df['day_of_week'].mode()[0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nMost common start hour is {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("\nThe total travel time in the selected period is {} hours".format(round(total_time)))

    # display mean travel time
    average_time = df['Trip Duration'].mean()
    print("\nThe average travel time in the selected period is {} hours".format(round(average_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nPrinting ordered start stations:\n")
    print(df['Start Station'].value_counts().head())
    start_st = df['Start Station'].mode()[0]
    print("\nMost common start station is: {}".format(start_st))

    # display most commonly used end station
    print('')
    print("\nPrinting ordered end stations:\n")
    print(df['End Station'].value_counts().head())
    end_st = df['End Station'].mode()[0]
    print("\nMost common end station is: {}".format(end_st))

    # display most frequent combination of start station and end station trip
    df['Total Route'] = df['Start Station'] +'   to   ' + df['End Station']
    print('')
    print("\nPrinting ordered routes:\n")
    print(df['Total Route'].value_counts().head())
    most_common_route = df['Total Route'].mode()[0]
    print("\nMost frequent route is:  {}".format(most_common_route))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\n\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types, as a pd series
    user_type_count = df['User Type'].value_counts()
    print('')
    print("Most frquent user type is {} with a total count of {}".format(user_type_count.idxmax(), user_type_count.max()))

    # Display counts of gender
    try:
        gender_count = df['Gender'].value_counts()
        print("\nMost frquent gender is {} with a total count of {}".format(gender_count.idxmax(), gender_count.max()))
    except:
        print('\nNo gender data for this city')

    # Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].mode()[0])
        print("\nEarliest year of birth is {}, most recent is {} and most common is {}".format(earliest, most_recent, most_common))
    except:
        print('\nNo birth year data for this city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    print("\nWould you like to read a chunk of raw data?\n y: for yes\n any key: for no\n")
    choice = str(input()).lower()
    print('')

    while choice == 'y':
        for chunk in pd.read_csv(CITY_DATA[city], chunksize = 5):
            print(chunk)
            print("\nWould you like to continue reading raw data?\n y: for yes\n any key: for no\n")
            choice = str(input()).lower()
            if choice != 'y':
                print("\nThank you!\n")
                print('-'*40)
                break


def main():
    while True:
        city, month, day = get_filters()
        print('-'*40)

        df = load_data(city, month, day)
        print('-'*40)
        print("\nYou have chosen to view data of {} in the month of {} and day of {}\n".format(city.title(), month.title(), day.title()))
        print("Printing a sample of the filtered data:\n")
        print(df.head())
        print('-'*40)


        time_stats(df, month, day)

        trip_duration_stats(df)

        station_stats(df)

        user_stats(df)

        display_raw_data(city)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
