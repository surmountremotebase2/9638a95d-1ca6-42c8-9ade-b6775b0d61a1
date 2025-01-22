from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset
from surmount.logging import log
from datetime import datetime,timedelta
import pandas as pd
class TradingStrategy(Strategy):
    def __init__(self): # 1x 7or7 to Dur 2x 7or3 to Dur  3x 3or3 to Dur  4x 7orDur/4 to Dur
        self.dur = 21080;self.debug = 0;self.adj_ma = 1; self.adj_bollinger=0.01*0  #self.adj_ma = 1; self.adj_bollinger=0.04
        self.tickers = ["QSI","AEYE","CDRO"]
        self.durcalendar = int(self.dur * 252 / 365)
        self.start_date = datetime(2024, 1, 1)
        self.count = 0
        self.goodcount = 0
    @property
    def assets(self):
        return self.tickers
    @property
    def interval(self):
        return "1day"
    def run(self, data):
        # Initialize an empty dictionary to store returns
        ma_scores = {}
        bollinger_scores = {}
        ma_bollinger_scores = {}
        self.count +=1
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

        def calculate_bollinger_scores(data, ticker,period=20, k=2):
            data['SMA'] = data['close'].rolling(window=period).mean()
            data['StdDev'] = data['close'].rolling(window=period).std()
            data['UpperBand'] = data['SMA'] + (k * data['StdDev'])
            data['LowerBand'] = data['SMA'] - (k * data['StdDev'])
            data['%B'] = (data['close'] - data['LowerBand']) / (data['UpperBand'] - data['LowerBand'])
            data['BandWidth'] = (data['UpperBand'] - data['LowerBand']) / data['SMA']
            # Current values
            last_row = data.iloc[-1]
            score = (1 - last_row['%B']) + last_row['BandWidth']               
            #scores.append((ticker, score))  
            # Sort stocks by score
            #scores = sorted(scores, key=lambda x: x[1], reverse=True)
            #scores[ticker] = score
            #scores.append((ticker, score)) 
            return score
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
          log(f" xx -1 ticker date. { data['ohlcv'][-1][self.tickers[0]]['date'] }") 
        # calculate returns since A date
        for ticker in self.tickers:
            historical_data = data["ohlcv"]
            df = pd.DataFrame([historical_data[i][ticker] for i in range(len(historical_data)) if ticker in historical_data[i]])
            if 1==1:
              boll_ticker_data = df[-20:]
              score=calculate_bollinger_scores(boll_ticker_data,20,k=2)
              bollinger_scores[ticker] = score

            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # Filter the data from a Date
            if 1==2:
              df_since_start = df[df.index >= self.start_date]
            else:
              locdur = self.dur%1000
              # good with 7  ... practically 99% close 2x0000
              if 11001 <= self.dur <= 11999:
                df_since_start = df[-max(7,min(self.count,locdur)):]
              elif 12001 <= self.dur <= 12999:
                df_since_start = df[-oscill(7,locdur,self.count):]
              elif 13001 <= self.dur <= 13999:
                df_since_start = df[-oscill63(7,locdur,self.count):]

              # like 1x000 but can handle short range better
              elif 21001 <= self.dur <= 21999:  
                df_since_start = df[-max(min(7,int(locdur/2)),min(self.count,locdur)):]
              elif 22001 <= self.dur <= 22999:
                df_since_start = df[-oscill(min(7,int(locdur/2)),locdur,self.count):]
              elif 23001 <= self.dur <= 23999:
                df_since_start = df[-oscill63(min(7,int(locdur/2)),locdur,self.count):]

              # good with 3 to ... helpfule for short end high fidelity
              elif 31001 <= self.dur <= 31999:
                df_since_start = df[-max(3,min(self.count,locdur)):]
              elif 32001 <= self.dur <= 32999:
                df_since_start = df[-oscill(3,locdur,self.count):]
              elif 33001 <= self.dur <= 33999:
                df_since_start = df[-oscill63(3,locdur,self.count):]

              # good for longer range like 150,125
              elif 41001 <= self.dur <= 41999:
                df_since_start = df[-max(max(7,int(locdur/4)),min(self.count,locdur)):]
              elif 42001 <= self.dur <= 42999:
                df_since_start = df[-oscill(max(7,int(locdur/4)),locdur,self.count):]
              elif 43001 <= self.dur <= 43999:
                df_since_start = df[-oscill63(max(7,int(locdur/4)),locdur,self.count):]


              else:
                df_since_start = df[-locdur:]

             
            if 1==1:     
              if self.count%100 == -100: 
                log(f" df .{df}  ")
                log(f" ticker. {ticker} dur. {self.dur}  df_since_start. {df_since_start}  ")
              if not df_since_start.empty:
                  # Calculate the returns
                  start_price = df_since_start.iloc[0]['close']
                  end_price = df_since_start.iloc[-1]['close']
                  ma_scores[ticker] = (end_price - start_price) / start_price
              else:
                  ma_scores[ticker] = 0
        if 1==1:
              for index,ticker in enumerate(self.tickers, start=0):
                ma_bollinger_scores[ticker] = ma_scores[ticker]*self.adj_ma + bollinger_scores[ticker]*self.adj_bollinger
               
        # Pick the stock with the highest return
        best_performer = max(ma_bollinger_scores, key=ma_bollinger_scores.get)
        if self.debug  == 1 and ( self.count%50 == 0 or self.count < 30):
          log(f" count. {self.count}   best_performer.  {best_performer} ma. {ma_scores}   boll. {bollinger_scores}   both. { ma_bollinger_scores }    ma_bollinger_scores.  {ma_bollinger_scores}    ")
        # Allocate 100% to the best performer
        allocation = {ticker: 0 for ticker in self.tickers}
        allocation[best_performer] = 1
        return TargetAllocation(allocation)