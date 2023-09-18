from enum import Enum
import os
from algoapp.py_files.Fyers_algo import StockAnalysis
from fyers_api import fyersModel
from algoapp.py_files.Init_data import InitData
from algoapp.py_files.access_otop import get_token


class Utils:
    #region - variables
    defaultTimeframe = 5
    access_token = get_token()
    client_id = "LB65IDSEJH-100"
    log_path =os.path.join(os.path.expanduser("~"), "Downloads")
    #endregion

    #region - FyersModel
    fyers = fyersModel.FyersModel(
            token=access_token, is_async=False, client_id=client_id, log_path=log_path)
    #endregion

    #region - place order enums
    class OrderType(Enum):
        LIMIT = 1
        MARKET = 2
        STOP = 3
        STOP_LIMIT = 4
    
    class Side(Enum):
        BUY = 1
        SELL = -1

    class ProductType(Enum):
        Forequityonly = "CNC"
        forallsegments = "INTRADAY"
        onlyforderivatives = "MARGIN"
        CoverOrder = "CO"
        BracketOrder = "BO"

    class OfflineOrderType(Enum):
        MARKET_OPEN = False  # Order placed when the market is open
        AMO_ORDER = True

    class ValidityType(Enum):
        IOC = "IOC"   # Immediate or Cancel
        DAY = "DAY"   # Valid till the end of the day

    #endregion

    #region - functions
    
    def GetHistoryData(stockSymbol, timefrom, timeto, timeframe):
        """
        Get historical stock data for a given symbol within a specified time period.

        Parameters:
        - stockSymbol: The symbol or identifier of the stock (e.g., NSE:SBIN-EQ).
        - timefrom: The start date of the historical data as a datetime object.(e.g.19022000)
        - timeto: The end date of the historical data as a datetime object.
        - timeframe: The time period for the historical data (e.g.,The candle resolution. Possible values are: Day : “D” or “1D”, 1 minute : “1”, 2 minute : “2", 3 minute : "3", 5 minute : "5", 10 minute : "10", 15 minute : "15", 20 minute : "20", 30 minute : "30", 60 minute : "60", 120 minute : "120", 240 minute : "240"etc.).
        Returns:
        - A list of historical stock data in the form of candles.
        """
        stock_details = {
                    "symbol": stockSymbol ,
                    "time_from": timefrom.strftime("%Y-%m-%d"),
                    "time_to": timeto.strftime("%Y-%m-%d"),
                    "time_period": timeframe,
                }
        stock_details = fyersModel.FyersModel(token=InitData.access_token, is_async=False, client_id=InitData.client_id, log_path=InitData.log_path)
        dictvalue = stock_details.HistoryData()
        return dictvalue["candles"]

    def placeOrder(symbol, qty, order_type, side, product_type, limit_price, stop_price, validity, disclosed_qty, offline_order):
        """
        Place an order

        Parameters:
        - fyers: Fyers API client instance.
        - symbol: The symbol or instrument identifier (e.g., NSE:SBIN-EQ).
        - qty: The quantity of the order.
        - order_type: The type of order (1 => Limit Order, 2 => Market Order, etc.).
        - side: The side of the order (1 => Buy, -1 => Sell).
        - product_type: The product type (e.g., CNC, INTRADAY, MARGIN, etc.).
        - limit_price: The limit price for Limit and Stoplimit orders (default => 0).
        - stop_price: The stop price for Stop and Stoplimit orders (default => 0).
        - validity: The validity of the order (e.g., IOC, DAY).
        - disclosed_qty: The disclosed quantity of the order (default => 0; allowed only for Equity).
        - offline_order: Whether the order is placed offline (True for AMO orders, False when the market is open).

        Returns:
        - Response from the Fyers API after placing the order.
        """
        data = {
        "symbol": symbol,
        "qty": qty,
        "type": order_type,
        "side": side,
        "productType": product_type,
        "limitPrice": limit_price,
        "stopPrice": stop_price,
        "validity": validity,
        "disclosedQty": disclosed_qty,
        "offlineOrder": offline_order,
        }
        response = Utils.fyers.place_order(data=data)
        print(response)

    def exitOrder(symbol):
        """
        Exits an order
        input : fyersmodel
        """
        data  = {
        "id" : symbol
        }
        response = Utils.fyers.exit_positions(data)
        return  
    

    #endregion
