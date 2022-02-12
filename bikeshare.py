import time
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs 
    city=input("Please enter the city you want to explore data from (chicago, new york city, washington): ")  
    while city.lower() not in CITY_DATA:
        print("no valid input - please try again")
        city=input("Please enter the city you want to explore data from (chicago, new york city, washington): ")
    month=input("Please enter the required month (name of month or 'all'): ")
    while month.lower() not in months:
        print("no valid input - please try again")
        month=input("Please enter the required month (name of month or 'all'): ")
    day=input("please enter the reqired day (name of day or 'all'):")
    while day.lower() not in days:
        print("no valid input - please try again")
        day=input("please enter the reqired day  (name of day or 'all'):")

        
    city=city.lower()
    month=month.lower()
    day=day.lower()
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
    df = pd.read_csv(CITY_DATA[city.lower()])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    month=month.lower()
    day=day.lower()
    
    # filter by month if applicable
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]


    # TO DO: display the most common day of week
    popular_dow = df['day_of_week'].mode()[0]

    # TO DO: display the most common start hour
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour   
    pop_hour = df['hour'].mode()[0]
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return popular_month, popular_dow, pop_hour


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start = df['Start Station'].mode()[0]


    # TO DO: display most commonly used end station
    pop_end = df['End Station'].mode()[0]


    # TO DO: display most frequent combination of start station and end station trip
    df['pop_kombi'] = df['Start Station']+ df['End Station']
    pop_combo = df['pop_kombi'].mode()[0]

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return pop_start, pop_end, pop_combo


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
   

    # TO DO: display total travel time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    df['travel_time']=(df['End Time']-df['Start Time']).dt.total_seconds()
    total_travel_time=df['travel_time'].sum()
    
   
    # TO DO: display mean travel time
    mean_travel_time=df['travel_time'].mean()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return total_travel_time, mean_travel_time

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()


    # TO DO: Display counts of gender
    gender_types = df['Gender'].value_counts()


    # TO DO: Display earliest, most recent, and most common year of birth
    earliest_yob=df['Birth Year'].min()
    latest_yob=df['Birth Year'].max()
    most_common_yob=df['Birth Year'].mode()[0]

   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return user_types, gender_types, earliest_yob, latest_yob, most_common_yob


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_st=time_stats(df)
        station_st=station_stats(df)
        trip_st=trip_duration_stats(df)
        user_st = user_stats(df)
        
        print("Time Statistics for {} in month {} and day {}". format(city, month, day))
        print('-'*80)
        print("Most Popular month in {}: {}". format(city, months[time_st[0]]))
        print("Most Popular day of week in {}: {}". format(city, time_st[1]))
        print("Most Popular Starting hour in {}: {}". format(city, time_st[2])) 
       
        
        print("Station Statistics for {} in month {} and day {}". format(city, month, day))
        print('-'*80)
        print("Most Popular Starting Station in {}: {}". format(city, station_st[0]))
        print("Most Popular Ending Station in {}: {}". format(city, station_st[1]))
        print("Most Popular Combinatipon of Start and Endin {}: {}". format(city, station_st[2])) 
        
        
        print("Trip Duration Statistics for {} in month {} and day {}". format(city, month, day))
        print('-'*80)
        print("Total Travel Time in {} in seconds: {}". format(city, trip_st[0]))
        print("Mean Travel Time in {} in seconds: {}". format(city, trip_st[1]))
        
    
        print("User Statistics for {} in month {} and day {}". format(city, month, day))
        print('-'*80)
        print("Count of Subscribers in {}: {}". format(city, user_st[0]['Subscriber']))
        print("Count of Customers in {}: {}". format(city, user_st[0]['Customer']))
        print("Count of Male Users in {}: {}". format(city, user_st[1]['Male']))
        print("Count of Female Users in {}: {}". format(city, user_st[1]['Female']))
       
        print("Earliest Year of Birth in {}: {}". format(city, user_st[2]))
        print("Latest Year of Birth in {}: {}". format(city, user_st[3]))
        print("Most Common Year of Birth in {}: {}". format(city, user_st[4])) 
    
        print('-'*80)
        N=0
        od=input("Do you also want to view the data? Enter yes or no.\n")
        while od.lower() == 'yes':
            N+=5
            dat=df.head(N)
            print(dat)
            od=input("Do you also want to view more data? Enter yes or no.\n")
            
  
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
