from StockViewer import view


#Dependencies: yfinance, pandas, matplotlib 

googleStock = view("GOOG", "2019-01-10" , "2020-05-07") # Creates an analysis, from 2018-11-01 to 2020-04-21

# Variation in %
#googleStock.VAR()

# Traded volume
#googleStock.VOL()

# MACD lines (fast and slow) - Default is 12, 26 and 9 days.
#googleStock.MACD()

# MACD Histogram
googleStock.MACDhistogram()

# SMA - Simple moving average
googleStock.SMA(15) # Creates SMA of 15 days

# EMA - Exponential moving average
#googleStock.EMA(10)  # Creates EMA of 10 days

# EMA - Exponential moving average
googleStock.EMA(50)  # Creates EMA of 50 days

# Plot all the data + indicators
googleStock.plot()

#  You can add how many indicators you want
#  You can comment or remove the line if you
#  want to remove an indicator, for example:
#  #googleStock.EMA(25)

