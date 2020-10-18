import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_input(options_list,question):
    '''
    takes a question to input to the user and an options list (lower case) to validate the user's input
    '''
    answer = ""
    while True:
        options=""
        for i in range(len(options_list)):
            option = options_list[i]
            if i == (len(options_list)-1):
                options+=option.title() 
            elif i == (len(options_list)-2):
                options+=option.title() +" and "
            else:
                options+=option.title() + ", "
            

        answer = input(question + " (valid options are {})".format(options)+"\n")
        if answer.lower() in options_list:
            while True:
                check = input("are you sure? (y/n)")
                if check.lower() == "y":
                    return(answer.lower())
                elif check.lower() == "n":
                    return(get_input(options_list,question))
                else:
                    print("Please enter a valid choice")
        else:
            print("Please enter a valid choice")

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
    city= get_input(['chicago', 'new york city', 'washington'],"Please choose a city")
    # get user input for month (all, january, february, ... , june)
    month = get_input(['january', 'february', 'march', 'april', 'may', 'june', 'all'],"Please choose a month")
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_input(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'],"Please choose a day")

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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month
    # extract day from the Start Time column to create a day column
    df['day_of_week'] = df['Start Time'].dt.day_name()
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    print(df.head())
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
    
   
    print(df.head())
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    try:
        print("Most common month is : ", df['month'].mode()[0])
    except:
        print("Choose All filter on Months to view the most common month")

    # display the most common day of week
    try:
        print("Most common week is : ", df['day_of_week'].mode()[0])
    except:
        print("Choose All filter on days to view the most common day")

    # display the most common start hour
    print("Most common hour is : ", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most common start station is : ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("Most common end station is : ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most frequent combination of start station and end station trip is: ", str(combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time is : ", df['Trip Duration'].sum() , " seconds")

    # display mean travel time
    print("Average travel time is : ", df['Trip Duration'].mean() , " seconds")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Count of user types is : \n" , df['User Type'].value_counts())

    try:
        # Display counts of gender
        print("Count of gender is : \n" , df['Gender'].value_counts())
    except:
        #handles case of washington
        print("\nNo info within data is provided on gender ")
    # Display earliest, most recent, and most common year of birth
    try:
        print("Earliest year of birth is :",int(df['Birth Year'].min()))
        print("Most recent year of birth is :",int(df['Birth Year'].max()))
        print("Most common year of birth is :",int(df['Birth Year'].mode()[0]))
    except:
        #handles case of washington
        print("\nNo info within data is provided on birth year ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
