class SimpleAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Start Date for Backtesting
        self.SetEndDate(2021, 1, 1) # End Date for Backtesting
        self.SetCash(99999)  # Cash
        
        spy = self.AddEquity("SPY", Resolution.Daily) # Daily Resolution

        spy.SetDataNormalizationMode(DataNormalizationMode.Raw) 

        self.spy = spy.Symbol
        self.SetBenchmark("SPY") # Setting a benchmark for this algo
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)
        
        self.entryPrice = 0
        self.period = timedelta(31)
        self.nextEntryTime = self.Time


    def OnData(self, data):
        if not self.spy in data:
            return
        price = data[self.spy].Close
        if not self.Portfolio.Invested:
            if self.nextEntryTime <= self.Time:
                self.SetHoldings(self.spy, 1)
                self.Log("BUY it for" + str(price))
                self.entryPrice = price
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.90 > price:
            self.Liquidate()
            self.Log("SELL it for" + str(price))
            self.nextEntryTime = self.Time + self.period