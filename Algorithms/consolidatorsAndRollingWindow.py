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
        self.Consolidate(self.symbol, Resolution.Daily, self.CustomBarHandler)
        
        self.Schedule.On(self.DateRules.EveryDay(self.symbol),
                 self.TimeRules.BeforeMarketClose(self.symbol, 15),      
                 self.ExitPositions)