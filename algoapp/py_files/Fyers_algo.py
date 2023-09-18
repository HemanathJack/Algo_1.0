import datetime
import pytz
from fyers_api import fyersModel
from .Init_data import InitData


class StockAnalysis:
    # comment check
    def __init__(self, stock_details):
        self.fyers = fyersModel.FyersModel(
            token=InitData.access_token, is_async=False, client_id=InitData.client_id, log_path=InitData.log_path)
        self.stock_details = stock_details

    def convertEpochToIST(self, epochtime):
        epoch_time = epochtime

        utc_time = datetime.datetime.utcfromtimestamp(epoch_time)

        india_tz = pytz.timezone('Asia/Kolkata')
        india_time = utc_time.astimezone(india_tz)
        india_time_str = india_time.isoformat()
        date_str, time_str = india_time_str.replace("T", " ").split()
        return date_str, time_str

    def convertEpochToIST(epochtime):
        epoch_time = epochtime

        utc_time = datetime.datetime.utcfromtimestamp(epoch_time)

        india_tz = pytz.timezone('Asia/Kolkata')
        india_time = utc_time.astimezone(india_tz)
        india_time_str = india_time.isoformat()
        date_str, time_str = india_time_str.replace("T", " ").split()
        return date_str, time_str

    def HistoryData(self):
        time_from = self.stock_details["time_from"]
        time_to = self.stock_details["time_to"]
        time_from_date = datetime.datetime.strptime(
            time_from, "%Y-%m-%d").date()
        time_to_date = datetime.datetime.strptime(time_to, "%Y-%m-%d").date()
        time_period = self.stock_details["time_period"]

        data = {"symbol": self.stock_details["symbol"], "resolution": time_period, "date_format": "1",
                "range_from": time_from_date, "range_to": time_to_date, "cont_flag": "1"}

        # print(self.fyers.history(data))

        History_data = self.fyers.history(data)
        return History_data

        print("\n\n\n")
        epochtime = History_data['candles'][0][0]
        date, time = self.convertEpochToIST(epochtime)
        OpenValue = History_data['candles'][0][1]
        HighestValue = History_data['candles'][0][2]
        LowestValue = History_data['candles'][0][3]
        CloseValue = History_data['candles'][0][4]
        volume = History_data['candles'][0][5]

        # print("Time:", date + " " + time.replace("+05:30", ""))
        # print("Open Value:", OpenValue)
        # print("Highest Value:", HighestValue)
        # print("Lowest Value:", LowestValue)
        # print("Close Value:", CloseValue)
        # print("Volume:", volume)
