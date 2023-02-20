import pandas as pd

from alpha_vantage.timeseries import TimeSeries


class ScriptData:
    """ScriptData class fetches US Stock data using Alpha Vantage."""
    
    def __init__(self, api_key="3RZYRTCYX1O2HPIG", interval_time="5min"):
        """Initilize the constructor"""
        self.api = api_key
        self.time_series = TimeSeries(key=self.api, output_format="pandas")
        self.time_interval = interval_time
        self.dt = dict()
    
    def fetch_intraday_data(self, script):
        """Fetches intraday data for given “script” (Example for script: “GOOGL”,
        “AAPL”) and stores as it is
        """
        try:
            data = self.time_series.get_intraday(script, interval=self.time_interval)
            return data
        except Exception as e:
            print(e)

    def convert_intraday_data(self, script, data):
        """Converts fetched intraday data as a pandas DataFrame (hereafter referred 
        as “df”)
        """
        try:
            df = data[0].reset_index()
            df.columns = ["timestamp", "open", "high", "low", "close", "volume"]            
            self.dt[script] = df
            return df
        except Exception as e:
            print(e)

    def indicator1(self, dataframe, timeperiod=5):
        """Takes df and timeperiod as inputs and give another pandas DataFrame as an output 
        with two columns:
        a. timestamp: Same as timestamp column in df
        b. indicator: Moving Average of the close column in df. The number of
        elements to be taken for a moving average is defined by timeperiod. 
        Ex, if timeperiod is 5, then each row in this column will be an average
        of total 5 previous values (including current value) of the close column
        """
        try:
            df = dataframe
            # df_copy = df.copy()
            df1 = df[["timestamp","close"]]
            df1["indicator"] = df["close"].rolling(timeperiod).mean()
            df1.drop(columns="close", axis=1, inplace=True)
            return df1
        except Exception as e:
            print(e)
    
    def __setitem__(self):
        pass

    def __getitem__(self, script):
        return self.dt[script]
    
    def __contains__(self, script):
        try:
            if script in self.dt: 
                return True
            else:
                return False
        except Exception as e:
            print(e)

