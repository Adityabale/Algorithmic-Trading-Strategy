import pandas as pd

from scriptdata import ScriptData

class Strategy:
    """class Strategy provides following signals, given a script name
    1. BUY (When: If indicator_data cuts close_data upwards)
    2. SELL (When: If indicator_data cuts close_data downwards)
    3. NO_SIGNAL (When: If indicator_data and close_data don’t cut
    each other)
    """

    def __init__(self, script):
        """Initilize the constructor"""
        self.script = script
        self.script_data = ScriptData()
        self.dt = []
        
    def get_signals(self):
        """Fetchs intraday historical day df using ScriptData class. Computes indicator 
        data on close of df using indicator1 function. Generates a pandas DataFrame called
        signals with 2 columns:
        i. timestamp: Same as timestamp column in df.
        ii. signal: BUY/SELL/NO SIGNAL.
        """
        data = self.script_data.fetch_intraday_data(self.script)
        df = self.script_data.convert_intraday_data(self.script, data)
        df2 = pd.DataFrame(df[["close"]].copy())
        # print(df2)
        df_indicator = self.script_data.indicator1(df, timeperiod=5)
        df_indicator.fillna(method="bfill", inplace=True)
        df2["indicator"] = df_indicator[["indicator"]]
        # print(df2)
        self.dt.append(df2)
        df_signal = pd.DataFrame(df[["timestamp"]].copy())
        # print(df_signal)
        df_signal['signal'] = df2.apply(lambda row:self.compare_values(row), axis=1)
        return df_signal

    def compare_values(self, row):
        """Compares value from each row of the dataframe based on conditions and generates
        output: BUY/SELL/NO SIGNAL"""
        if (row.indicator < row.close) and (-0.01 <= (row.indicator - row.close) <= 0):
           return 'BUY'
        elif (row.indicator > row.close) and (0 <= (row.indicator - row.close) <= 0.01):
           return 'SELL'
        else:
           return 'NO SIGNAL'