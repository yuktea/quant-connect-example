# region imports
from AlgorithmImports import *
from collections import deque
# endregion


class ConsolidatorsAndRollingWindow(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2021, 1, 1)
        self.SetCash(199000)
        self.symbol = self.AddEquity("SPY", Resolution.Minute).Symbol
        self.rollingWindow = RollingWindow[TradeBar](2)
        self.Consolidate(self.symbol, Resolution.Daily, self.BarHandler)
        
        self.Schedule.On(self.DateRules.EveryDay(self.symbol),
                 self.TimeRules.BeforeMarketClose(self.symbol, 15),      
                 self.Exit)

    def OnData(self, data):
        
        if not self.rollingWindow.IsReady:
            return
        
        if not (self.Time.hour == 9 and self.Time.minute == 31):
            return
        
        # Gap is Up = Sell
        if data[self.symbol].Open >= 1.01*self.rollingWindow[0].Close:
            self.SetHoldings(self.symbol, -1)
        # Gap is Down = Buy
        elif data[self.symbol].Open <= 0.99*self.rollingWindow[0].Close:
            self.SetHoldings(self.symbol, 1)

    def BarHandler(self, bar):
        self.rollingWindow.Add(bar)

    def Exit(self):
        self.Liquidate(self.symbol)