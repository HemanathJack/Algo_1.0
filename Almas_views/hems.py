from Almas_views.Utils import Utils


class hems:
    def getHighLowofStock(symbol, timefrom, timeto):
        maxPrice=0
        minPrice=0
        HistoryData_timeranged = Utils.GetHistoryData(symbol, timefrom, timeto, Utils.defaultTimeframe)
        for items in HistoryData_timeranged:
                listofOpenClose=[]
                listofOpenClose.append(items["open"])
                listofOpenClose.append(items["close"])
                for litem in listofOpenClose:
                    if(litem>maxPrice):
                        maxPrice=litem 
                    if(litem<minPrice):
                         minPrice=litem
        return maxPrice, minPrice       