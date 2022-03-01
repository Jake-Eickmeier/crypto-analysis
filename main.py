from pycoingecko import CoinGeckoAPI
import time

from collectHistoryData import collectHistoryData


cg = CoinGeckoAPI()

#A list of hand-selected coins that I believe to be of interest
interesting_coins = ['metal', 'bitcoin-diamond', 'harmony', 'celo',
 'aave', 'balancer', 'yearn-finance', 'havven', 'kyber-network', 'numeraire', 'internet-computer',
 'bitcoin', 'ethereum', 'binancecoin', 'cardano', 'ripple', 'dogecoin',
 'stellar', 'polkadot','bitcoin-cash','uniswap','chainlink','solana','vechain',
 'matic-network', 'eos', 'shiba-inu', 'tron', 'filecoin', 'bitcoin-cash-sv',
 'iota', 'bittorrent-2', 'leo-token', 'near', 'chiliz', 'basic-attention-token', 'algorand',
 'golem', 'audius', 'cartesi', 'civic', 'pundi-x-2', 'aelf', 'just', 'revain', 'tezos' ]


#  Interesting tokens not yet added (by identifier)

if __name__ == '__main__':
    # Interval can be 'minutely' for up to 1 day duration, 'hourly' for up to 90 days, and 'daily' for 
    # a duration greater than 90 days

    #Collect data on all of the aforementioned interesting coins at once
    for coin in interesting_coins:
        try:
            collectHistoryData(cg, coin)
        except:
            print("Error when collecting " + coin + " data")

        #Sleep for 0.20 seconds to ensure that I do not go over the 10
        #requests per minute limit (sleeping for extra to be on safe side)
        time.sleep(0.20)

        #Uncomment below lines when a new 90d hourly data pull is desired
        #collectHistoryData(cg, coin, days_inp="90", interval_inp="hourly")
        #time.sleep(0.20)
