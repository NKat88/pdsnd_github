import time
import pandas as pd
import numpy as np
import calendar

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
    print('Hello! Let\'s explore some US bikeshare data!')

    city = input("Enter which city you'd like info for: {}:\n".format(list(CITY_DATA.keys()))).lower()
    while city not in list(CITY_DATA.keys()):
        city = input("Invalid city - please try again:\n")
        print("city entered:", city)
    print("Gathering information for {}...".format(city.title()))

    month_names = ["all"]
    for i in range(1,7):
        month_names.append(calendar.month_name[i].lower())

    month = input("Please enter which month you would like info for, or enter all:\n").lower()
    while month not in month_names:
        month = input("Invalid month - please try again:\n")
        print("month entered:", month)
    print("Gathering information for {}...".format(month.title()))

    day_names = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    day = input("Please enter a day of the week to get info for, or enter all:\n").lower()
    while day not in day_names:
        day = input("Invalid day - please try again:\n")
        print("day entered:", day)
    print("Gathering information for {}...".format(day.title()))


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

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('Most common month:', calendar.month_name[common_month])

    common_day = df['day_of_week'].mode()[0]
    print('Most common day:', common_day)

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most popular start hour:', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('Most popular start station:', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('Most popular end station:', common_end_station)

    common_station_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('Most popular station combination:', common_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time = int(round(df['Trip Duration'].sum()))
    days = total_travel_time//1440
    leftover_minutes = total_travel_time % 1440
    hours = leftover_minutes // 60
    mins = total_travel_time - (days*1440) - (hours*60)

    print('Total travel time:', days, 'days', hours, 'hours', mins, 'minutes')

    mean_travel_time = int(round(df['Trip Duration'].mean()))
    days = mean_travel_time//1440
    leftover_minutes = mean_travel_time % 1440
    hours = leftover_minutes // 60
    mins = mean_travel_time - (days*1440) - (hours*60)

    print('Mean travel time:', days, 'days', hours, 'hours', mins, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('Counts of user types:', user_types)

    try:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:', gender_counts)

        earliest_birth_year = df['Birth Year'].min()
        most_recent_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()
        print('Earliest birth year:', earliest_birth_year)
        print('Most recent birth year:', most_recent_birth_year)
        print('Most common birth year:', most_common_birth_year)
    except:
        print('Gender and birth year not available for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Asks user if they would like to see the raw data and displays
        5 rows of data at a time. """
    pd.set_option('display.max_columns', 200)
    start = 0
    raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
    while raw_data.lower() == 'yes':
        df_slice = df.iloc[start: start+5]
        print(df_slice)
        start += 5
        raw_data = input('\nWould you like to see moreeeee data?! Enter yes or no.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
