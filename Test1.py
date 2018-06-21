import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time
from Exchange import Exchange

np.random.seed(int(time.time()))
    
start_price=100.0      
exchange=Exchange(start_price)

for _ in range(300):
    side='B'
    price=np.random.normal(99,5)
    if np.random.random()<0.5:
        side='S'
        price=np.random.normal(100,5)
    price=int(price*10)/10.0
    size=int(200*np.random.random())
    print "\n\n Adding order, side={}, price={}, size={}\n\n".\
   format(side,price,size)
    exchange.addOrder(side,price,size)
    exchange.prepareMatch()
    exchange.matchOrders()
    exchange.savePrices()
    print "\n Buys filled:"
    print exchange.buys_filled
    print "\n Sells filled:"
    print exchange.sells_filled
    print "\n\n\n"
    print "The buy book:\n"
    print exchange.buys_prices
    print "\n"
    print exchange.buys_info
    print "\n\n"
    print "The sell book:\n"
    print exchange.sells_prices
    print "\n"
    print exchange.sells_info
    print "\n\n\n"
    

"""
Plot the resulting buy and sell order books. After the books have been
balanced, there is no overlap.
"""

Buys={-p:exchange.buys_info[-p]["tot"] for p in exchange.buys_prices}
Sells={p:exchange.sells_info[p]["tot"] for p in exchange.sells_prices}
sns.distplot(list(Buys.keys()), hist_kws={"weights":list(Buys.values())},\
             kde=False,label="buys")
sns.distplot(list(Sells.keys()), hist_kws={"weights":list(Sells.values())},\
             kde=False,label="sells")
plt.legend(loc="upper right")
plt.title("Balanced buy/sell order books")
plt.show()

"""
Plot the time series of the best bid and the best ask prices.
Notice that the bid price is lower than the sell price, or equal to
the sell price, the latter being the artifact of one or both of the
buy and/or sell order books being completely filled.
"""

Bids=exchange.bids
Asks=exchange.asks
plt.plot(Bids,label="bid price")
plt.plot(Asks,label="ask price")
plt.title("bid/ask prices times series")
plt.legend(loc="upper right")
plt.show()
