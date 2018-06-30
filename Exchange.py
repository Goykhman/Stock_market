from heapq import heappush, heappop 

class Exchange:
    def __init__(self,start_price):
        self.buys_prices=[]
        self.sells_prices=[]
        self.buys_info={}
        self.sells_info={}
        self.bids=[start_price]
        self.asks=[start_price]
        self.order_id=-1
        self.buys_filled={}
        self.sells_filled={}
    def reset(self):
        self.order_id=-1
    def addOrder(self,side,limit_price,size):
        self.order_id+=1
        if side=='B':
            if limit_price not in self.buys_info:
                heappush(self.buys_prices,-limit_price)
                self.buys_info[limit_price]={"ids":[],"sizes":{},"tot":0}
            self.buys_info[limit_price]["ids"]+=[self.order_id]
            self.buys_info[limit_price]["sizes"][self.order_id]=size
            self.buys_info[limit_price]["tot"]+=size
        elif side=='S':
            if limit_price not in self.sells_info:
                heappush(self.sells_prices,limit_price)
                self.sells_info[limit_price]={"ids":[],"sizes":{},"tot":0}
            self.sells_info[limit_price]["ids"]+=[self.order_id]
            self.sells_info[limit_price]["sizes"][self.order_id]=size
            self.sells_info[limit_price]["tot"]+=size
        return self.order_id
    def prepareMatch(self):
        self.buys_filled={}
        self.sells_filled={}
    def matchOrders(self):
        while len(self.buys_prices)>0 and self.buys_info[-self.buys_prices[0]]["tot"]==0:
            del self.buys_info[-self.buys_prices[0]]
            heappop(self.buys_prices)
        while len(self.sells_prices)>0 and self.sells_info[self.sells_prices[0]]["tot"]==0:
            del self.sells_info[self.sells_prices[0]]
            heappop(self.sells_prices)
        if len(self.buys_prices)==0 or len(self.sells_prices)==0 or -self.buys_prices[0]<self.sells_prices[0]:
            return
        bb=-self.buys_prices[0]
        bs=self.sells_prices[0]
        price=(bs+bb)/2.0
        price=int(100*price)/100.0
        buy_id=self.buys_info[bb]["ids"][0]
        buy_size=self.buys_info[bb]["sizes"][buy_id]
        sell_id=self.sells_info[bs]["ids"][0]
        sell_size=self.sells_info[bs]["sizes"][sell_id]
        filled=min(buy_size,sell_size)
        if buy_id not in self.buys_filled:
            self.buys_filled[buy_id]=[]
        if sell_id not in self.sells_filled:
            self.sells_filled[sell_id]=[]
        self.buys_filled[buy_id]+=[[filled,price]]
        self.sells_filled[sell_id]+=[[filled,price]]
        self.buys_info[bb]["tot"]-=filled
        self.sells_info[bs]["tot"]-=filled
        self.buys_info[bb]["sizes"][buy_id]-=filled
        self.sells_info[bs]["sizes"][sell_id]-=filled
        if self.buys_info[bb]["sizes"][buy_id]==0:
            self.buys_info[bb]["ids"]=self.buys_info[bb]["ids"][1:]
            del self.buys_info[bb]["sizes"][buy_id]
        if self.sells_info[bs]["sizes"][sell_id]==0:
            self.sells_info[bs]["ids"]=self.sells_info[bs]["ids"][1:]
            del self.sells_info[bs]["sizes"][sell_id]
        self.matchOrders()
    def savePrices(self):
        if len(self.buys_prices)==0 or len(self.sells_prices)==0:
            middle=(self.bids[-1]+self.asks[-1])/2.0
            self.bids+=[middle]
            self.asks+=[middle]
        else:
            self.bids+=[-self.buys_prices[0]]
            self.asks+=[self.sells_prices[0]]
