import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data only for the cities (chicago, new york city, washington)!')
    #get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city=input('Would you like to see data for chicago, new york city or washington ?').lower()
            if city not in CITY_DATA: # if the entred city name is invalid
                print('The entred city is not in the list')
            elif city == None:
                raise ValueError("None input cityname!")
                break
        except:
            print("Sorry, ValueError!")
            break
        if city in CITY_DATA:
            break
    # get user input for month (all, january, february, ... , june)
    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    while True:
        try:
            month=input('Which Month would you like to filter by?').lower()
            if month not in months: # if the entred month is not in the months' list
                print('The entred Month is not in the list')
            elif month == None:
                raise ValueError("None input!")
                break
        except:
            print("Sorry, ValueError!")
            break
        if month in months:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days_of_week=['all', 'monday', 'tuesday', 'wednesday', 'thursday','friday','saturday','sunday']
    while True:
        try:
            day=input('Which Day would you like to filter by?').lower()
            if day not in days_of_week: # if the entred day is not in the days_of_week list
                print('The entred month is not in the list')
            elif day == None:
                raise ValueError("None input!")
                break
        except:
            print("Sorry, ValueError!")
            break
        if day in days_of_week:
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
     # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name

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


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

        # display the most common month
    df['month'] = df['Start Time'].dt.strftime('%b')
    most_common_month = df['month'].mode()[0]
    print('the most common month is: {}'.format(most_common_month))

        # display the most common day of week
    df['day'] = df['Start Time'].dt.day
    most_common_day = df['day'].mode()[0]
    print('the most common day of week is: {}'.format(most_common_day))

        # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['hour'].mode()[0]
    print('the most common hour is: {}'.format(most_common_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].mode()[0]
    start_number=df['Start Station'].value_counts(normalize=True,ascending=True).max()
    print('The most commonly used start station: {} with {} times'.format(most_used_start_station, start_number))

    # display most commonly used end station
    most_used_end_station = df['End Station'].mode()[0]
    end_number=df['End Station'].value_counts(normalize=True,ascending=True).max()
    print('The most commonly used End station: {} with {} times'.format(most_used_end_station, end_number))

    # display most frequent combination of start station and end station trip
    df['start_end combined'] ='From--'+df['Start Station']+' --TO-- '+df['End Station']
    startend_commonly_used= df['start_end combined'].mode()[0]
    combine_number=df['start_end combined'].value_counts(normalize=True,ascending=True).max()
    print('The most commonly used start to End station combination: {} with {} times '.format(startend_commonly_used, combine_number))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('total travel time (second):',total_travel_time)
    day= total_travel_time//86400
    hour= (total_travel_time%86400)//3600
    minute= ((total_travel_time%86400)%3600)//60
    second= ((total_travel_time%86400)%3600)%60
    print('Or simply it is: {} day,{} hour,{} minute,{} second'.format(day, hour, minute,second))
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('mean travel time (s): {}'.format(mean_travel_time))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User Type:\n', user_types)
    try:
        if ('Gender' and 'Birth Year') not in df.columns:
            print('Sorry!, Washington dataset has no data for Gender and year of birth!')
            raise
        elif ('Gender' and 'Birth Year') in df.columns:
            # Display counts of gender
            gender_counts = df['Gender'].value_counts()
            print(gender_counts)
            # Display earliest, most recent, and most common year of birth
            earliest=df['Birth Year'].min()
            most_recent=df['Birth Year'].max()
            most_common= df['Birth Year'].mode()[0]
            print('the earliest year of birth: {} \n the most recent year of birth: {} \n , the most common year of birth {}'.format(earliest,most_recent,most_common))
    except:
        print("Oops!  There was no data.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df): #this function is created to ask the user whether he wants to see some rows of data
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while True:
        print(df.iloc[start_loc : start_loc+5, 0:])
        start_loc += 5
        view_display = input("Do you wish to continue?: ").lower()
        if view_display.lower() != 'yes':
            break

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
