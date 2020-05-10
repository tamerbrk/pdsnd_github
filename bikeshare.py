#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  2 18:50:47 2020

This program is developed to analyze the Bike user data from 3 different cities.

@author: Tamer Berk
"""

import time
import pandas as pd

CITY_DATA = { 
            'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv' 
        }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

DAY_OF_WEEK = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'] 



def read_yes_no_from_console(message):
    """
    Reads yes or no from console
    Args:
        (str) message - The message displayed while asking for input
    Returns:
        (int) 1 for yes, 2 for no
    """
    answer_code=2
    while True:
        try:
            answer=input(message).lower()
            if answer=="yes":
                answer_code=1
                break
            elif answer=="no":
                break
            else:
                print('*> ERROR : Invalid answer. Please enter yes or no')               
        except Exception as exp:
            print('*> ERROR : {}'.format(exp))
    return answer_code
   

def read_int_from_console(message, min_value, max_value):
    """
    Reads an integer value from console in the given range
    Args:
        (str) message - The message displayed while asking for input
        (int) min_value - minimum value allowed
        (int) max_value - max value allowed
    Returns:
        (int) The input from tthe console
    """
    while True:
        try:
            code = int(input(message))
            if code<min_value or code>max_value:
                print('*> ERROR : Invalid code. Please enter a number in the given range (' + str(min_value) + '-' + str(max_value) + ')')
            else:
                break
        except ValueError:
            print('*> ERROR : The code has to be a numeric value')
        except Exception as exp:
            print(exp)
    return code
  

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('*'*40)
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). 
    print('*'*40)
    print('*>')
    print('*> Please enter the city code to analyze.')
    print('*> Valid values are 1: Chicago, 2: New York City, 3: Washington, 0: Exit')
    city_code = read_int_from_console('*> City code? :', 0, 3)
    if city_code==0:
        return '','',''
    else:
        if city_code == 1:
            city = 'chicago'
        elif city_code == 2:
            city = 'new york city'
        else:
            city = 'washington'
    
    print('*>') 
    # get user input for month (all, january, february, ... , june)
    print('*> Please enter the month code to filter by')
    print('*> Valid values are 1: January, 2: February, 3: March, 4: April, 5: May, 6: June, 7: All, 0:Exit')
    month_code = read_int_from_console('*> Month code? :', 0, 7)
    if month_code==0:
        return '','',''
    else:
        month = MONTHS[month_code-1]
    print('*>')   
    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('*> Please enter the day of week code to filter by')
    print('*> Valid values are 1: Monday, 2: Tuesday, 3: Wednesday, 4: Thursday, 5: Friday, 6: Saturday, 7: Sunday, 8: All, 0:Exit')
    day_of_week_code = read_int_from_console('*> Day of week code? :', 0, 8)
    if day_of_week_code ==0:
        return '','',''
    else:
        day=DAY_OF_WEEK[day_of_week_code-1]
    print('*>')
    print('*'*40)
    print('*> PARAMETERS')
    print('*> CITY    :{}'.format(city))
    print('*> MONTH   :{}'.format(month))
    print('*> DAY     :{}'.format(day))
    print('*'*40)   
    return city, month, day, 


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        status - The status of the read operation. If there is a problem returns False
    """
    try:
        df = pd.read_csv(CITY_DATA[city])
        df['Start Time'] =pd.to_datetime(df['Start Time'])
        df['month']=df['Start Time'].dt.month
        df['day']=df['Start Time'].dt.weekday
        df['hour']=df['Start Time'].dt.hour
        if month!="all":
            df=df[df['month']==MONTHS.index(month)+1]
        if day != "all":
            df=df[df['day']==DAY_OF_WEEK.index(day)]

    except Exception as exp:
        print('*> ERROR: {}'.format(exp))
        df=None
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('*> Calculating The Most Frequent Times of Travel...')
    start_time = time.time()
    try:
        # display the most common month
        busy_month = df['month'].value_counts()
        busy_month_index = busy_month.keys()[0]
        print('**> Most common month is "{}" with {} travels'.format(MONTHS[busy_month_index-1], busy_month[busy_month_index]))
    
        # display the most common day of week
        busy_day = df['day'].value_counts()
        busy_day_index=busy_day.keys()[0]
        print('**> Most common day is "{}" with {} travels'.format(DAY_OF_WEEK[busy_day_index], busy_day[busy_day_index]))

        # display the most common start hour
        busy_hours = df['hour'].value_counts()
        busy_hour_index=busy_hours.keys()[0]
        print('**> Most busy hour is "{}" with {} travels'.format(busy_hour_index, busy_hours[busy_hour_index]))
    except Exception as exp:
        print('**> ERROR : {}'.format(exp))
    print("*> This took %s seconds." % (time.time() - start_time))
    print('*'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('*> Calculating The Most Popular Stations and Trip...')
    start_time = time.time()

    try:
        # display most commonly used start station
        start_station = df['Start Station'].value_counts()
        station_index = start_station.keys()[0]
        print('**> Most commonly used start station is "{}" with {} travels'.format(station_index, start_station[station_index]))
    
        # display most commonly used end station
        end_station = df['End Station'].value_counts()
        station_index = end_station.keys()[0]
        print('**> Most commonly used end station is "{}" with {} travels'.format(station_index, end_station[station_index]))

        # display most frequent combination of start station and end station trip
        df['Start-End-Station'] = df['Start Station'] + '->' + df['End Station']
        popular_lines = df['Start-End-Station'].value_counts()
        line_index = popular_lines.keys()[0]
        print('**> Most frequent combination of start station is "{}" with {} trips'.format(line_index, popular_lines[line_index]))
    except Exception as exp:
       print('**> ERROR : {}'.format(exp)) 

    print("* This took %s seconds." % (time.time() - start_time))
    print('*'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('*> Calculating Trip Duration...')
    start_time = time.time()
    
    nan_trip_duration = df['Trip Duration'].isnull().sum()
    if nan_trip_duration>0:
        print ('**> INFO : There are {} entry(ies) with NaN value in Trip Duration field'.format(nan_trip_duration))
        
    # display total travel time
    try:
        total = df['Trip Duration'].sum()
        if (total<60*24):
            print('**> Total travel time is {} hours and {} minutes'.format(total // 60, total % 60))
        else:
            days = total // (60*24)
            total -= days*24*60
            print('**> Total travel time is {} days {} hours and {} minutes'.format(days, total // 60, total % 60))

        # display mean travel time
        mean = df['Trip Duration'].mean()
        if (mean<60*24):
            print('**> Mean travel time is {} hours and {} minutes'.format(mean // 60, mean % 60))
        else:
            days = mean // (60*24)
            mean -= days*24*60
            print('**> Mean travel time is {} days {} hours and {} minutes'.format(days, mean // 60, mean % 60))
    except Exception as exp:
         print('**> ERROR : {}'.format(exp))       
    print("*> This took %s seconds." % (time.time() - start_time))
    print('*'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('*> Calculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    try:
        nan_user_types = df['User Type'].isnull().sum()
        if nan_user_types>0:
            print ('**> INFO : There are {} entry(ies) with empty value in User Type field'.format(nan_user_types))
        user_types = df['User Type'].value_counts()
        for type in user_types.keys():
            print('**> Total travels of user type "{}" is {}'.format(type, user_types[type]))
    except Exception as exp:
        print('**> ERROR : {}'.format(exp)) 
    # Display counts of gender
    try:
        nan_gender = df['Gender'].isnull().sum()
        if nan_gender>0:
            print ('**> INFO : There are {} entry(ies) with empty value in Gender field'.format(nan_gender))
        user_genders = df['Gender'].value_counts()
        for type in user_genders.keys():
            print('**> Total travels of gender "{}" is {}'.format(type, user_genders[type]))       
    except Exception as exp:
        print("**> ERROR: while getting Gender data. ({})".format(exp))
    # Display earliest, most recent, and most common year of birth
    try:
        nan_birth_years = df['Birth Year'].isnull().sum()
        if nan_birth_years>0:
            print('**> INFO : There are {} entry(ies) with Nan (Not a Number) value in Birth Date field'.format(nan_birth_years))
            print('**> INFO : They are ignored')
        earliest = int(df['Birth Year'].min(skipna=True))
        recent = int(df['Birth Year'].max(skipna=True))
        common = int(df['Birth Year'].mode()[0])
        print('**> The earliest user is born in {}'.format(earliest))       
        print('**> The youngest user is born in {}'.format(recent))
        print('**> The common birth year is {}'.format(common))      
    except Exception as exp:
        print('**> ERROR: while getting Birth Year data. ({})'.format(exp))

 
    print("*> This took %s seconds." % (time.time() - start_time))
    print('*'*40)


def display_raw_data(df):
    """Displays raw data upon user request.
    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
    """
    index = 0
    answer = read_yes_no_from_console('*> Do you want to see the 5 lines of raw data? (yes/no) : ')
    while answer == 1:
        print(df.iloc[index:index+5])
        index+=5
        answer = read_yes_no_from_console('*> Do you want to see next 5 lines? (yes/no) : ')
    print('*'*40)

def main():
    """ The main module. Gets the parameters/filters from user and executes the analysis modules
    
    Returns
    -------
    None.

    """
    while True:
        city, month, day = get_filters()
        if city=='':
            print ('*> The application is stopped upon user request.')
            break
        df = load_data(city, month, day)
        if df is not None:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_raw_data(df)
        restart = read_yes_no_from_console('*> Would you like to restart? (yes/no) : ')
        if restart==2:
            break
        
if __name__ == "__main__":
	main()
