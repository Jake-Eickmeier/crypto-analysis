import pandas as pd
import os
import datetime
import time as TIME
import numpy as np
import random

import matplotlib.pyplot as plt
import matplotlib as mpl

day_dict = {
    "Sunday": 0,
    "Monday": 1,
    "Tuesday": 2,
    "Wednesday": 3,
    "Thursday": 4,
    "Friday": 5,
    "Saturday": 6
}

#Returns day of week (e.g. "Wednesday") in GMT/UTC from epoch/unix timestamp
def unix_timestamp_to_day(ts):
    return TIME.strftime("%A", TIME.gmtime(ts/1000))

def identify_weekdays(df):
    print("-----------")
    print(df.columns)
    print("-----------")

def create_time_bins(intervals=24):
    interval_list = []
    interval_list_string = []

    if intervals==24:
        for i in range(24):
            interval_list.append(datetime.time(i, 0))
            interval_list_string.append("{}:00".format(i))
    elif (intervals == 48):
        for i in range(24):
            interval_list.append(datetime.time(i, 0))
            interval_list.append(datetime.time(i, 30))

            interval_list_string.append("{}:00".format(i))
            interval_list_string.append("{}:30".format(i))
    elif (intervals == 96):
        for i in range(24):
            interval_list.append(datetime.time(i, 0))
            interval_list.append(datetime.time(i, 15))
            interval_list.append(datetime.time(i, 30))
            interval_list.append(datetime.time(i, 45))
            interval_list_string.append("{}:00".format(i))
            interval_list_string.append("{}:15".format(i))
            interval_list_string.append("{}:30".format(i))
            interval_list_string.append("{}:45".format(i))
    else:
        print("Please select a supported number of intervals, i.e. 24, 48, or 96")
    return interval_list, interval_list_string

test_half_hourly, test_half_hourly_strings = create_time_bins(96)

hist_dict = dict.fromkeys(test_half_hourly, 0)
hist_dict_neg = dict.fromkeys(test_half_hourly, 0)
print(hist_dict)


for i in os.listdir("data"):
    if ("lock" not in str(i)):
        file_loc = "data/" + str(i)
        df = pd.read_csv(file_loc)
        df['Unix_Timestamp_Difference'] = df.unix_timestamp - df.unix_timestamp.shift(1)
        time_difference_threshold = 10
        df['Price_Shift'] = np.where(df.Unix_Timestamp_Difference < (time_difference_threshold * 60 * 1000),
            df.prices_usd - df.prices_usd.shift(1), 0)  

        #Create empty columns for coming row iteration 
        df["nearest_timeslot_hours"] = ""
        df["nearest_timeslot_minutes"] = ""
        df['day_of_week'] = ""
        df['shift_classification'] = ""
        df['day_of_week_num'] = ""
        
        #identify_weekdays(df)
        #df['day_of_week'] = unix_timestamp_to_day(df['unix_timestamp'])
        #df.to_csv("price_shift_incl.csv")

        df_head = df.head()
        print(df_head)
        #print(df_head["Unnamed: 0"].str[11:])
        #for t in df_head["Unnamed: 0"].str[11:]:

        start_loop_time = TIME.time()
        prev_date = ""  #Will be used to keep track of when a date is actually unique and requires conversion
        for index, row in df.iterrows():   #TODO: This is not a very performant strategy. I need to change this to not require iterating over the rows of the df
            t = row["Unnamed: 0.1"][11:]    #TODO: Fix the usage of "Unnamed" columns to proper convention
            curr_date = row["Unnamed: 0.1"][:10]
            #print(row)

            t_hours = int(t[:2])
            t_minutes = int(t[3:5])
            tmp_timestamp = datetime.time(t_hours, t_minutes)

            closest_time_index = 0
            hourly_interval = (len(test_half_hourly)/24)
            minutely_interval = 60/((len(test_half_hourly)/24))
            closest_time_index = int(hourly_interval*t_hours)
            
            #print(t_minutes % minutely_interval / minutely_interval) # Get just the decimal
            closest_time_index += int(t_minutes / minutely_interval)
            if ((t_minutes % minutely_interval / minutely_interval) >= 0.5):    #Can later adjust this to include weightings if desired
                closest_time_index += 1
                if (closest_time_index >= len(test_half_hourly)):
                    closest_time_index = 0
            #row["nearest_timeslot_hours"] = int(test_half_hourly_strings[closest_time_index][:2])
            #row["nearest_timeslot_minutes"] = int(test_half_hourly_strings[closest_time_index][3:5])
            df.at[index, "nearest_timeslot_hours"] = int(test_half_hourly[closest_time_index].hour)
            df.at[index, "nearest_timeslot_minutes"] = int(test_half_hourly[closest_time_index].minute)

            #Only bother calculating the day of week/num representation when the date is newly unique
            if (curr_date != prev_date):
                df.at[index, "day_of_week"] = unix_timestamp_to_day(row['unix_timestamp'])
                df.at[index, "day_of_week_num"] = day_dict[df.day_of_week[index]]
                prev_date = curr_date


            #TODO: Below may be an area where I can work on finding a way to optimize the variables to put the data into the most optimal perspective
            #Now we can find whether the trend is up or down and add to the respective bin accordingly
            multiplier_percentage_interval = 0.05    #For every multiplier_percentage_interval that the price shift is greater or less than the
                                                    #previous price by, an additional point will be added to the respective bin. This should
                                                    #create some weighting to allow bigger price chances to have more impact than small ones.
                                                    #This will have a maximum limit so that outliers won't have too much impact
                                                    #A value of 0.1, for example, represents a 0.1% price shift
            maximum_multiplier = 10
            if (row["Price_Shift"] < 0):
                prev_price = row["prices_usd"] - row["Price_Shift"]
                percentage_shift = ((prev_price / row["prices_usd"]) - 1.0) * 100
                weighted_value = int(percentage_shift / multiplier_percentage_interval)
                if (weighted_value > maximum_multiplier):
                    hist_dict_neg[test_half_hourly[closest_time_index]] += maximum_multiplier
                    df.at[index, "shift_classification"] = -maximum_multiplier
                else:
                    hist_dict_neg[test_half_hourly[closest_time_index]] += weighted_value
                    df.at[index, "shift_classification"] = -weighted_value
                #hist_dict_neg[test_half_hourly[closest_time_index]] += 1
            elif (row["Price_Shift"] > 0):
                prev_price = row["prices_usd"] - row["Price_Shift"]
                percentage_shift = (1.0 - (prev_price / row["prices_usd"])) * 100
                weighted_value = int(percentage_shift / multiplier_percentage_interval)
                if (weighted_value > maximum_multiplier):
                    hist_dict[test_half_hourly[closest_time_index]] += maximum_multiplier
                    df.at[index, "shift_classification"] = maximum_multiplier
                else:
                    hist_dict[test_half_hourly[closest_time_index]] += weighted_value
                    df.at[index, "shift_classification"] = weighted_value

                #hist_dict[test_half_hourly[closest_time_index]] += 1
            
            
            #print(t.shift(1))
        

        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)  #Replace whitespace with NaN so that we can use ffill below
        df.day_of_week.fillna(method='ffill', inplace=True)     #Forward fill both day of week and num representation 
        df.day_of_week_num.fillna(method='ffill', inplace=True) #This is far more performant than converting each within the loop
        print(df.head)
        end_loop_time = TIME.time()
        print("-------------------------------")
        print("Done Looping. Loop time: " + str(end_loop_time - start_loop_time))   #Using this as a reference to help improve loop time/remove
                                                                                    #inperformant techniques from iteration where possible
        print("-------------------------------")
        df.to_csv("price_shift_incl.csv")

        x = test_half_hourly_strings
        print(x)
        #y = [i+random.gauss(0,1) for i,_ in enumerate(x)]  #Use this jsut to plot random data for testing purposes
        y = list(hist_dict.values())    #list is necessary since dict.values() returns a view of the values instead of a list of values
        y2 = list(hist_dict_neg.values())
        print(len(hist_dict.values()))
        print("Upward values:   " + str(list(hist_dict.values())))
        print("Downward values: " + str(list(hist_dict_neg.values())))

        
        fig, ax = plt.subplots()

        #Below bar calls can be used for stacked histogram, which appears less clear than a standard plot imo
        #ax.bar(range(len(x)),y,color='g', label='Upward')
        #ax.bar(range(len(x)),y2,color='r', bottom=y, label='Downward')

        ax.plot(range(len(x)),y,color='g', label='Upward')
        ax.plot(range(len(x)),y2,color='r', label='Downward')
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x, rotation=40)

        #Below tickLabel iteration can be used to hide every nth tick label, which can result in a less
        #cluttered view of the x axis
        for tickLabel in ax.get_xticklabels()[::2]:
            tickLabel.set_visible(False)

        ax.set_xlabel("Time of Day")
        ax.set_ylabel("Numerical Value of Upward/Downward Trends")
        ax.set_title("Average Trends Throughout a Day (BTC)")  #TODO: Group data by day of week instead of clumping every day together in dataset
        #ax.gcf().autofmt_xdate()
        plt.show()



