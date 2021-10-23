import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ["all", "january", "february", "march","april", "may","june"] 
days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def take_day_or_month( msg, array):
    """
    Takes the input from the user and check if it's a valid one against the sent array
    
    Returns:
        (str) day_or_month - specifies the day or month entered
    """
    day_or_month = input(msg).lower()
    while day_or_month not in array:
        print("Can't understand! Can you please tell me again") 
        day_or_month = input(msg).lower()
    return day_or_month
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid = False
    while not valid:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').lower()
        valid = city == 'chicago' or city == 'new york city' or city == 'washington'
    
    valid_filter = False
    while not valid_filter:
        # give the user the filtering options: either with the month, day, both ot none of them
        # and accordingly the filter is applied
        filter_applied = input('Would you like to filter the data by month, day, both or none of the previous? Type "none" to apply no filters\n').lower()
        month = "all"
        day = "all"
        
        if filter_applied == "none" or filter_applied == "month" or filter_applied == "day" or filter_applied == "both":
            valid_filter = True
        # get user input for month (all, january, february, ... , june)    
        if filter_applied == "month" or filter_applied == "both":
            month = take_day_or_month('Which month? Please enter a month name from January till June\n', months)

        # get user input for day of week (all, monday, tuesday, ... sunday)
        if filter_applied == "day" or filter_applied == "both":
            day = take_day_or_month('Which day? Please type the full name(e.g. Saturday, Sunday, Monday, ...etc.) \n', days)

        if not valid_filter:
            print(" Can't understand this filter:( , Please reenter in the same format")


    print('-'*40)
    return city, month, day

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
    # read the csv file into a data frame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
        # print(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # print(df)

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[ df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = months[ df['month'].mode()[0] ]
    print("What is the most popular month for traveling?")
    print( most_common_month )
    print()

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("What is the most popular day for traveling?")
    print( most_common_day )
    print()

    # display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print("What is the most popular hour for traveling?")
    print( popular_hour )
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most trips start from: ", most_common_start_station )

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("While most of then end at: ", most_common_end_station )


    # display most frequent combination of start station and end station trip
    df['comb'] = df['Start Station'] + " to " + df['End Station']
    most_common_comb = df['comb'].mode()[0]
    freq = df.groupby(["comb"])["comb"].count()[most_common_comb]
    
    print( "A total number",freq, "trips goes from", most_common_comb
          ,"which makes it the most used line! ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total duration: ", total_travel_time )


    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Avg Duration: ", mean_travel_time )


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if "User Type" in df:
        user_types = df.groupby(["User Type"])["User Type"].count()
        print(user_types)
    else:
        print("No user types data to share \n")

    # Display counts of gender
    if "Gender" in df:
        gender = df.groupby(["Gender"])["Gender"].count()
        print(gender)
    else:
        print("\nNo gender data to share\n")

    # Display earliest, most recent, and most common year of birth
    print("\nWhat is the oldest, youngest, and most popular year of birth, respectively?")
    if "Birth Year" in df:
        earliest = df["Birth Year"].min()
        most_recent = df["Birth Year"].max()
        most_common = df["Birth Year"].mode()[0]
        freq = df.groupby(["Birth Year"])["Birth Year"].count()[most_common]
        print("(",earliest,",", most_recent,",", most_common,"as", freq , "share this birth year )")
    else:
        print("\nNo birth year data to share\n")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    end_loc = df.shape[0]
    while (view_data != "no" and start_loc < end_loc):
        if (view_data == "yes"):
            print(df.iloc[start_loc : start_loc + 5])
            start_loc += 5
            if (start_loc < end_loc):
                view_data = input("Do you wish to continue?: ").lower()
            else:
                print("No more data to show!")
        else:
            view_data = input('\nSorry couldn\'t understand :(! Please enter yes or no only\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
