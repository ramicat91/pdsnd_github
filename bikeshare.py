import time
import sys
from datetime import datetime
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

list_months=['january', 'february', 'march', 'april', 'may', 'june','july','august','september','october','november','december']
list_days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
p_day='' #public 
p_month=''#public
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global p_day
    global p_month
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Availible cities to analyze: chicago, new york city, washington')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=str(input("Enter the city to analyze:")).lower().strip()
    while city not in CITY_DATA:
        print("Please select a city from the following:(chicago, new york city, washington)")
        city=str(input("Enter the city to analyze:")).lower().strip()
        if city in CITY_DATA:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    by_month_yes_no=input("Do you want to filter by month?(y/n)")
    while by_month_yes_no not in ('y','n','Y','N'):
        print("Please answer with y for Yes or n for No ")
        by_month_yes_no=input("Do you want to filter by month?(y/n)")
        if by_month_yes_no in ('y','n','Y','N'):
            break
    if(by_month_yes_no in ('N','n')):
        month='all'
        p_month=month
    else:
        month=str(input("Enter the month to filter with(ex:january....december):")).lower().strip()
        p_month=month
        while month not in list_months:
            print("Please Enter a valid month name!")
            month=str(input("Enter the month to filter with(ex:january....december):")).lower().strip()
            if month in list_months:
                p_month=month
                break
            
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    by_day_yes_no=input("Do you want to filter by day?(y/n)")
    while by_day_yes_no not in ('y','n','Y','N'):
        print("Please answer with y for Yes or n for No ")
        by_day_yes_no=input("Do you want to filter by day?(y/n)")
        if by_day_yes_no in ('y','n','Y','N'):
            break
    if(by_day_yes_no in ('N','n')):
        day='all'
        p_day=day
    else:
        day=str(input("Enter the day of week to filter with(ex:saturday....friday):")).lower().strip()   
        p_day=day
        while day not in list_days:
            print("Enter a valid day of week!") 
            day=str(input("Enter the day of week to filter with(ex:saturday....friday):")).lower().strip()     
            if day in list_days:
                p_day=day
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
    global p_day
    global p_month
    
    start_time = time.time()
    print('Loading The Dataset...')
    df=pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #create a new column named Month 
    df['Month']=df['Start Time'].dt.month
    #create a new column named Day_Of_Week
    df['Day Of Week']=df['Start Time'].dt.dayofweek
    #create a new column named Start Hour
    df['Hour']=df['Start Time'].dt.hour
    
    #check if the entered month exist in the dataset
    existed_months=list(df['Month'].unique())
    existed_months.sort()
    #check if the entered day exist in the dataset
    existed_days=list(df['Day Of Week'].unique())
    existed_days.sort()
    
    if(month!='all'):
    #filter by month
        if(list_months.index(month)+1 in existed_months):
            month=list_months.index(month) + 1
            df=df[df['Month']==month]

        else:
            
            #force the user to enter the month from the existed months in the dataset
            print('the month {} does not exist in the dataset!\n'.format(month))
            print('Enter the month from this list:')
            for m in existed_months:
                 print('\t{}'.format(list_months[m-1]))
            print('Or type \'none\' for no filter.')
            while 1:
                
                new_month=str(input("Enter the month to filter with:")).lower().strip()
                
                try:
                    if(new_month=='none'):
                        new_month='all'
                        p_month=new_month
                        break
                    
                    if(new_month in list_months and list_months.index(new_month)+1 in existed_months):
                        p_month=new_month
                        new_month=list_months.index(new_month) + 1
                        df=df[df['Month']==new_month]
                        break
                except ValueError:
                    print('the month {} does not exist in the dataset!\n'.format(month))
                    print('Enter the month from this list:')
                    for m in existed_months:
                        print('\t{}'.format(list_months[m-1]))
                    print('Or type \'none\' for no filter.')
                    continue
                
    if(day!='all'):
            #filter by day of week       
        if(list_days.index(day) in existed_days):
            day = list_days.index(day)
            df=df[df['Day Of Week']==day]
        else:
            #force the user to enter the day from the existed days in the database
            print('the day {} does not exist in the dataset!\n'.format(day))
            print('Enter the day from this list:')
            for d in existed_days:
                print('\t{}'.format(list_days[d]))
            print('Or type \'none\' for no filter.')
            
            while 1:
                
                new_day=str(input("Enter the day to filter with:")).lower().strip()

                try:
                    if new_day=='none':
                        new_day='all'
                        p_day=new_day
                        break
                    if(new_day in list_days and list_days.index(new_day) in existed_days):
                        p_day=new_day
                        new_day=list_days.index(new_day)
                        df=df[df['Day Of Week']==new_day]
                        break
                except ValueError:
                    print('Please enter the day from this list:')
                    for d in existed_days:
                        print('\t{}'.format(list_days[d]))
                    continue
                
    print("\nLoading took %s seconds." % round((time.time() - start_time),6))
    print('-'*40)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    
    print('\nCalculating The Most Frequent Times of Travel...with filter(month={} , day={})\n'.format(p_month,p_day))

    start_time = time.time()

    # TO DO: display the most common month
    popular_month=df['Month'].mode()[0]
    
    # TO DO: display the most common day of week
    popular_day=df['Day Of Week'].mode()[0]
    popular_day=str(list_days[popular_day]).title()
    
    # TO DO: display the most common start hour
    popular_hour=df['Hour'].mode()[0]
    
    print("most popular month: {} ({}) \nmost popular day: {}\nmost popular hour: {}".format(popular_month,str(list_months[popular_month-1]).title(),popular_day,popular_hour))
    print("\nThis took %s seconds." % round((time.time() - start_time),6))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...with filter(month={} , day={})\n'.format(p_month,p_day))
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station=df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    popular_end_station=df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    combination=df.groupby(['Start Station', 'End Station']).size().reset_index(name='counts').sort_values(['counts'], ascending=False).head(1)
    populaire_combination=combination.iloc[0]['Start Station']+" --> "+combination.iloc[0]['End Station']  
       
    print("most popular Start Station: {} \nmost popular End Station: {} \nmost popular Combinition: {}".format(popular_start_station,popular_end_station,populaire_combination))
    print("\nThis took %s seconds." % round((time.time() - start_time),6))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...with filter(month={} , day={})\n'.format(p_month,p_day))
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration=df['Trip Duration'].sum()
    #convert to days
    total_trip_duration/=60*60*24
    
    # TO DO: display mean travel time
    mean_trip_duration=df['Trip Duration'].mean()
    #convert to minutes
    mean_trip_duration/=60
    print("Total trip duration: {} day\nMean trip duration: {} minutes".format(round(total_trip_duration,1),round(mean_trip_duration,1)))
    print("\nThis took %s seconds." % round((time.time() - start_time),6))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...with filter(month={} , day={})\n'.format(p_month,p_day))
    start_time = time.time()

    # TO DO: Display counts of user types
    users=df['User Type'].value_counts()
    users_dict={index:users.loc[index] for index in list(users.index)}
    for user_type,count in users_dict.items():
        print('{} : {}'.format(user_type,count)) 
    
    # TO DO: Display counts of gender
    #check if Gender columns exist in the dataset
    if('Gender' in list(df.columns)):
        gender=df['Gender'].value_counts()
        gender_dict={index:gender.loc[index] for index in list(gender.index)}
        for gndr,count in gender.items():
            print('{} : {}'.format(gndr,count))
        print('Unkown gender count: {}\n'.format(df['Gender'].isnull().sum()))
    else:
        print("No Gender data to calculate!")
        
    # TO DO: Display earliest, most recent, and most common year of birth
    #check if Birth Year columns exist in the dataset
    if('Birth Year' in list(df.columns)):
        earliest_birth=df['Birth Year'].min()
        recent_birth=df['Birth Year'].max()
        common_birth=df['Birth Year'].mode()[0] 
        print("Earliest birth year: {} \nRecent birth year: {}\nCommon birth year: {}".format(earliest_birth,recent_birth,common_birth))
        print('Unkown birth year count: {}'.format(df['Birth Year'].isnull().sum()))
    else:
        print("No Birth year data to calculate!")
    
    print("\nThis took %s seconds." % round((time.time() - start_time),6))
    print('-'*40)


def main():
    
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        while True:
            time_stats(df)
            show_next=str(input("Do you want to show  more stats ?(y/n)")).lower().strip()
            sys.stdout.flush()
            while show_next not in ['y','n']:
                show_next=str(input("Do you want to show  more stats ?(y/n)")).lower().strip()
                sys.stdout.flush()
            if(show_next!='y'):
                break
            station_stats(df)
            show_next=str(input("Do you want to show  more stats ?(y/n)")).lower().strip()
            sys.stdout.flush()
            while show_next not in ['y','n']:
                show_next=str(input("Do you want to show  more stats ?(y/n)")).lower().strip()
                sys.stdout.flush()
            if(show_next!='y'):
                break
            trip_duration_stats(df)
            show_next=str(input("Do you want to show  more stats ?(y/n)")).lower().strip()
            sys.stdout.flush()
            while show_next not in ['y','n']:
                show_next=str(input("Do you want to show  more stats ?(y/n)")).lower().strip()
                sys.stdout.flush()
            if(show_next!='y'):
                break
            user_stats(df)
            break
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()



