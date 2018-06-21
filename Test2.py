import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import time
from Exchange import Exchange

np.random.seed(int(time.time()))

class Agent:
    def __init__(self,c,s):
        self.cash=c
        self.shares=s

class Market:
    def __init__(self,n,startPrice):
        self.N=n
        self.start_price=startPrice
        self.participants=[]
        for _ in range(self.N):
            a=Agent(np.abs(np.random.normal(1000000.0,10000.0)),\
                    np.abs(int(np.random.normal(10000,100))))
            self.participants+=[a]
        self.prices=[self.start_price]
        self.order_to_agent={}
    def tradingSession(self):
        exchange=Exchange(self.prices[-1])
        last_price=self.prices[-1]
        self.order_to_agent={}
        for n in range(self.N):
            if np.random.random()>0.1:
                continue
            limit_price=np.abs(np.random.normal(1,0.02)*last_price)
            limit_price=int(100*limit_price)/100.0
            side,size='N',0
            if np.random.random()<0.5:
                side='S'
                size=int(np.random.random()*self.participants[n].shares)
            else:
                side='B'
                size=int(np.random.random()*self.participants[n].cash/limit_price)
            order_id=exchange.addOrder(side,limit_price,size)
            self.order_to_agent[order_id]=n
            exchange.prepareMatch()
            exchange.matchOrders()
            exchange.savePrices()
            buys_filled=exchange.buys_filled
            sells_filled=exchange.sells_filled
            for b_id,b_info in buys_filled.items():
                agent=self.order_to_agent[b_id]
                for F in b_info:
                    size,price=F[0],F[1]
                    self.participants[agent].shares+=size
                    self.participants[agent].cash-=price*size
            for s_id,s_info in sells_filled.items():
                agent=self.order_to_agent[s_id]
                for F in s_info:
                    size,price=F[0],F[1]
                    self.participants[agent].shares-=size
                    self.participants[agent].cash+=price*size         
        price=(exchange.bids[-1]+exchange.asks[-1])/2.0
        return price
    def run(self,T):
        for t in range(T):
            price=self.tradingSession()
            self.prices+=[price]
            
            
                
market=Market(1000,100.0)
market.run(10000)

"""
Plot the resulting stock price time series.
"""
    
prices=market.prices
        
plt.plot(prices)
plt.title("Stock price time series")
plt.show()

"""
Plot the resulting stock log returns time series.
"""

log_returns=[np.log(prices[i]/prices[i-1]) for i in range(1,len(prices))]
stats.probplot(log_returns, dist="norm", plot=plt)
plt.title("Normal Q-Q plot")
plt.show()

"""
Plot the final wealth distribution.
"""

wealth=[]
last_price=prices[-1]
for agent in market.participants:
    w=last_price*agent.shares+agent.cash
    wealth+=[w]

plt.hist(wealth,bins=50)
plt.title("Final wealth distribution")
plt.show()
