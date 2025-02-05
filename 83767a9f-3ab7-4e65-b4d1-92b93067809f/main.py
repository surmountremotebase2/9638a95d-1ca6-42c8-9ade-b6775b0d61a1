# SBP44 0 daily XX-61 RGTI-MVST-IONQ-QBTS
from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log
from datetime import datetime,timedelta
import pandas as pd
class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["RGTI", "MVST", "IONQ", "QBTS"]
        self.dur = 61
        self.durcalendar = int(self.dur * 252 / 365)
        self.start_date = datetime(2024, 1, 1)
        self.count = 0
        self.goodcount = 0

    @property
    def assets(self):
        return self.tickers
    @property
    def interval(self):
        return "1hour"
   

    def run(self, data):
        # Initialize an empty dictionary to store returns
        returns_since_start = {}

        def oscill(lower,upper,counter): 
          if int((counter-1) / upper)%2 == 0:
            direction = 1
          else:
            direction = 0
          if direction == 1:  # Forward direction
                value = max(lower, counter%upper)
          else:  # Backward direction
                value = max(lower, upper - counter%upper)
          return value

        def oscill63(lower,upper,counter): 
          return max(lower, counter%upper)

        #today = datetime.now()
        self.count +=1
        if self.count < 2:
          log(f" count. {self.count } ")
          log(f" data {data['ohlcv'][0]}")
        if data['ohlcv'] == []:
          if self.count%10 == 0:
            log(f" data empty warning: count. {self.count } ")
          return []
        else:
          self.goodcount +=1
          if self.goodcount == 1:
            log(f" data good notice: count. {self.count } data. {data['ohlcv'][0]}")
        todayx = data['ohlcv'][-1][self.tickers[0]]['date']  # AAPL date. 2024-11-19 00:00:00
        today =  datetime.strptime(todayx[:10], "%Y-%m-%d")
        self.start_date = today - timedelta(days=self.durcalendar)
        
        if self.count < 2:
          log(f" count. {self.count } today. {today} start_date {self.start_date} ") 
        if self.count < 2:
          log(f" xx -1 aapl date. { data['ohlcv'][-1][self.tickers[0]]['date'] }") 
        # calculate returns since A date
        for ticker in self.tickers:
            historical_data = data["ohlcv"]
            df = pd.DataFrame([historical_data[i][ticker] for i in range(len(historical_data)) if ticker in historical_data[i]])
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # Filter the data from a Date
            if 1==2:
              df_since_start = df[df.index >= self.start_date]
            else:
              if   self.dur in (21, 61, 101, 201):
                df_since_start = df[-max(7,min(self.count,self.dur-1)):]
              elif self.dur in (22, 62, 102, 202):
                df_since_start = df[-oscill(7,self.dur-1,self.count):]
              elif self.dur in (23, 63, 103, 203):
                df_since_start = df[-oscill63(7,self.dur-1,self.count):]
              else:
                df_since_start = df[-self.dur:]
                  
            if self.count < 1:
              log(f" df .{df}  ")
              log(f"  df_since_start. {df_since_start}  ")
            if not df_since_start.empty:
                # Calculate the returns
                start_price = df_since_start.iloc[0]['close']
                end_price = df_since_start.iloc[-1]['close']
                returns_since_start[ticker] = (end_price - start_price) / start_price
            else:
                returns_since_start[ticker] = 0
        # Pick the stock with the highest return
        best_performer = max(returns_since_start, key=returns_since_start.get)
        if self.count < 0:
          log(f" count. {self.count}    returns_since_start.  {returns_since_start}   ")
        if self.count < 0:
          log(f" count. {self.count}    best_performer.  {best_performer}   ")
        # Allocate 100% to the best performer
        allocation = {ticker: 0 for ticker in self.tickers}
        allocation[best_performer] = 1
        return TargetAllocation(allocation)