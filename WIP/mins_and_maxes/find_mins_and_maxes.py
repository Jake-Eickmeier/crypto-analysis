import pandas as pd
import os

import matplotlib.pyplot as plt

for i in os.listdir("data"):
    if ("lock" not in str(i)):
        file_loc = "data/" + str(i)
        df = pd.read_csv(file_loc)
        
        print(df.head())


        df['min'] = df.prices_usd[(df.prices_usd.shift(1) > df.prices_usd) & (df.prices_usd.shift(-1) > df.prices_usd)]
        df['max'] = df.prices_usd[(df.prices_usd.shift(1) < df.prices_usd) & (df.prices_usd.shift(-1) < df.prices_usd)]

        #print(df.head())

        df['date'] = df['Unnamed: 0'].str[:10]
        #for i in df['Unnamed: 0'][0:10]:
        #    print(i)
        print(df)
        for i in df['date'].unique():
            print("global max for date " + i + ": " + str(max(df.prices_usd[df['date']==i])))
            print("global min for date " + i + ": " + str(min(df.prices_usd[df['date']==i])))

        plt.scatter(df.index, df['min'], c='r')
        plt.scatter(df.index, df['max'], c='g')
        plt.xlabel("Index")
        plt.ylabel("Price (USD)")
        plt.title("Local Minima/Maxima Throughout a Day (BTC)")
        #plt.scatter(df['Unnamed: 0'], df['min'], c='r')
        #plt.scatter(df['Unnamed: 0'], df['max'], c='g')
        #print(df.columns)
        plt.plot(df.prices_usd)
        #plt.scatter(df.index, df['prices_usd'])
        plt.show()