
from surmount.base_class import Strategy, TargetAllocation
from surmount.data import ConsumerConfidence, CboeVolatilityIndexVix, CboeNasdaqHundredVolatilityIndex, StickyPriceConsumerPriceIndex, HousePriceIndex
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["AAPL"]
        self.data_list = [
            ConsumerConfidence(),
            CboeVolatilityIndexVix(),
            CboeNasdaqHundredVolatilityIndex(),
            StickyPriceConsumerPriceIndex(), 
            HousePriceIndex()
            ]

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        aapl_stake = 0
        
        consumer_confidence = data[("consumer_confidence",)][-1]['value']
        log("consumer_confidence: " + str(consumer_confidence))

        house_price_index = data[("house_price_index",)][-1]['value']
        log("house_price_index: " + str(house_price_index))

        sticky_price_consumer_price_index = data[("sticky_price_consumer_price_index",)][-1]['value']
        log("sticky_price_consumer_price_index: " + str(sticky_price_consumer_price_index))

        cboe_nasdaq_hundred_volatility_index = data[("cboe_nasdaq_hundred_volatility_index",)][-1]['value']
        log("cboe_nasdaq_hundred_volatility_index: " + str(cboe_nasdaq_hundred_volatility_index))

        cboe_volatility_index_vix = data[("cboe_volatility_index_vix",)][-1]['value']
        log("cboe_volatility_index_vix: " + str(cboe_volatility_index_vix))
        

        aapl_stake = 0.5
        return TargetAllocation({"AAPL": aapl_stake})

