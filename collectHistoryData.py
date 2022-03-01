from pycoingecko import CoinGeckoAPI
import pandas as pd
from datetime import datetime
import os

#Calling this function collects a day worth of minutely coin data from CoinGecko for the target coin
def collectHistoryData(cgAPI_instance, target_coin, days_inp="1", interval_inp="minutely"):

    cg = cgAPI_instance

    data_raw = cg.get_coin_market_chart_by_id(id=target_coin, vs_currency='usd', days=days_inp, interval=interval_inp)
    data = pd.DataFrame.from_dict(data_raw)
    
    dateTime_values = [i for i, j in data.prices.values]

    #Divide i by 1000 below because timestamp is in milliseconds
    dateTime_values_UTC = [datetime.utcfromtimestamp(i/1000).strftime('%Y-%m-%d %H:%M:%S') for i in dateTime_values]
    #print(dateTime_values_UTC)

    prices_values = [j for i, j in data.prices.values]
    market_caps_values = [j for i, j in data.market_caps.values]
    total_volumes_values = [j for i, j in data.total_volumes.values]
    column_names = ["prices_usd", "market_caps", "total_volumes", "unix_timestamp"]
    
    data_organized = pd.DataFrame(list(zip(prices_values, market_caps_values, total_volumes_values, dateTime_values)), index=dateTime_values_UTC, columns=column_names)
    #print(data_organized)

    current_dt = datetime.now()
    filename = ""
    if (days_inp == "90"):
        filename = "data/" + target_coin + "/" + target_coin + "_" + "daily" + "_" + str(current_dt) + ".csv"
    else:
        filename = "data/" + target_coin + "/" + target_coin + "_" + str(current_dt) + ".csv"
    if (not os.path.isdir("data/" + target_coin)): 
        os.makedirs("data/" + target_coin)      #Make the directory if it doesn't already exist

    data_organized.to_csv(filename)     #Save the collected data to .csv format
    print("-------- Finished collecting " + target_coin + " data --------")
