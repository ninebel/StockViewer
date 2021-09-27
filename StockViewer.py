import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class view:

   def __init__ (self, stock, date1, date2):
      
      self.stock = stock
      self.data = yf.download(self.stock , date1, date2)

      self.plotsSMA = []
      self.plotsEMA = []
      self.parallelGraph = ''

   def SMA (self, n , plot=True , data=[]):

      if len(data) == 0:

         data = self.data['Close']

      sma = []

      for i in range (0, n-1):

         sma.append(data[0])

      for i in range (n-1 , len(data)):

         soma = 0

         for j in range (0, n):

            soma += data[i-j]

         sma.append(soma / n)

      if plot == True:

         self.data.insert(len(self.data.columns), 'sma' + str(n), sma)
         self.plotsSMA.append('sma' + str(n))

      return sma

   def EMA (self, n , plot=True , data=[]):

      if len(data) == 0:
         
         data = self.data['Close']

      ema = [data[0]]
      k = 2/(n+1)

      for i in range (1, len(data)):

         ema.append(data[i] * k + ema[len(ema)-1] * (1-k))

      if plot == True:
         
         self.data.insert(len(self.data.columns), 'ema' + str(n), ema)
         self.plotsEMA.append('ema' + str(n))
      
      return ema

   def VOL (self):

      self.parallelGraph = "vol"
      

   def VAR (self, plot=True , data=[]):

      if len(data) == 0:

         data = self.data['Close']

      var = []
      var.append(0)

      for i in range (1, len(data)):

         closeToday = data[i]
         closeYesterday = data[i-1]

         var.append((closeToday/closeYesterday - 1)*100)

      if plot == True:

         self.data.insert(len(self.data.columns), 'var', var)
         self.parallelGraph = 'var'

      return var

   def MACD (self, plot=True):

      ema12 = self.EMA(12, plot=False)
      ema26 = self.EMA(26, plot=False)
   
      fastMACD = []

      for i in range (len(ema12)):
      
         fastMACD.append(ema26[i] - ema12[i])

      slowMACD = []
      slowMACD = self.EMA(9, plot=False, data=fastMACD)

      if plot == True:

         self.data.insert(len(self.data.columns), 'fastMACD', fastMACD)
         self.data.insert(len(self.data.columns), 'slowMACD', slowMACD)
         self.parallelGraph = 'macd'

      return fastMACD, slowMACD

   def MACDhistogram (self):

      fastMACD , slowMACD = self.MACD(plot=False)

      MACDhist = []

      for i in range (len(fastMACD)):

         MACDhist.append(fastMACD[i] - slowMACD[i])

      self.data.insert(len(self.data.columns), 'MACDhist', MACDhist)   
      self.parallelGraph = 'MACDhist'


   def plot (self):

      if self.parallelGraph != '':

         fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 6), gridspec_kw={'height_ratios': [3, 1]})
         
         ax1.plot(self.data.index , self.data['Close'] , label=self.stock)

         for i in self.plotsSMA:

            ax1.plot(self.data.index , self.data[i] , label=i.upper())

         for i in self.plotsEMA:

            ax1.plot(self.data.index , self.data[i] , label=i.upper())


         ax1.legend()
         ax1.grid()

         
         if self.parallelGraph == 'macd':
            
                  ax2.plot(self.data.index, self.data['fastMACD'], label='Fast MACD') 
                  ax2.plot(self.data.index, self.data['slowMACD'], label='Slow MACD')
                  
         elif self.parallelGraph == 'MACDhist':
            
                  ax2.plot(self.data.index, self.data[self.parallelGraph] , label='MACD Hist.')
                  ax2.fill_between(self.data.index , self.data['MACDhist'])
                  
         elif self.parallelGraph == 'var':
            
                  ax2.plot(self.data.index, self.data[self.parallelGraph], label='Var%')

         elif self.parallelGraph == 'vol':
            
                  ax2.plot(self.data.index, self.data['Volume'], label='Volume')
                  ax2.fill_between(self.data.index , self.data['Volume'])

         ax1.set_ylabel('Price')
         ax2.set_xlabel('Date')
         ax2.legend()         
         ax2.grid()

      else:

         self.data['Close'].plot(label=self.stock.upper())

         for i in self.plotsSMA:

            self.data[i].plot(label=i.upper())

         for i in self.plotsEMA:

            self.data[i].plot(label=i.upper())

         plt.xlabel('Date')
         plt.ylabel('Price')
         plt.legend()
         plt.grid()

      plt.subplots_adjust(hspace=0)
      plt.show()



