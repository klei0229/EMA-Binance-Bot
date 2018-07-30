#15 minute candle on the BTCUSDT with ema 13 and ema 31 

from datetime import datetime, timedelta

import time
from binance.client import Client

#used for seeding the ema
def sma(n,client):
	klines40 = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "10 hour ago UTC")
	formated_klines40 = format_klines(klines40)

	sum = 0
	for i in range (0,n):
		sum += formated_klines40[len(formated_klines40)-i-1][5]
	average = sum/n
	return average

#Calculate ema of period 'n' using price_today and ema_yesterday
def ema(price_t,n,ema_y):
	n = float(n)
	#print "n is %s" %(n)
	k = float(2/(n+1))
	#print "k is %s" %(k)
	ema_t = ((price_t)*k) + ((ema_y)*(1-k))

	return ema_t


def OHLCavg(openVal,highVal,lowVal,closeVal):
	return ((openVal + highVal + lowVal + closeVal) / 4)

def format_klines(klines):
	length = len(klines)
	formatedList = []
	for i in range ( 0, length):
			
		instance = klines[i]
		openTime = instance[0]
		openVal = instance[1]
		highVal = instance[2]
		lowVal = instance [3]
		closeVal = instance[4]
		volumeVal = instance[5]
		closeTime = instance[6]

		openValF = openVal.encode("utf-8")
		openValfloat = float(openValF)
	
		highValF = highVal.encode("utf-8")
		highValfloat = float(highValF)

		lowValF = lowVal.encode("utf-8")
		lowValfloat = float(lowValF)

		closeValF = closeVal.encode("utf-8")
		closeValfloat = float(closeValF)

		formatedInstance = []


		instance_avg = OHLCavg(openValfloat,highValfloat,lowValfloat,closeValfloat)
		#print(instance_avg)
		formatedInstance.append(openTime)
		formatedInstance.append(openValfloat)
		formatedInstance.append(highValfloat)
		formatedInstance.append(lowValfloat)
		formatedInstance.append(closeValfloat)
		formatedInstance.append(instance_avg)
		formatedInstance.append(closeTime)

		formatedList.append(formatedInstance)

		
	return formatedList
		

def format_Lowest_Ask(askOrderBook):
	
	price = askOrderBook[0][0]
	priceF = price.encode("utf-8")
	priceFFloat = float(priceF)	
	return priceFFloat


def main():
	print("Start")
	api_key = "6X3oPrSmRanw9VwBGs3fv8lwl0ygFMvpj7ydKmTxvZ206G6AgugiexNjORC9n09nj"
	api_secret = "qmywzSWrAGtreHjwuz4HwTcuNbW5Nr9uoXhHg9xKnP7gk7ltSID1JlJqKFmdAqSw" 
	client = Client(api_key,api_secret)	

	begin = True
	ema_t12 = 0
	ema_t32 = 0
	balance = 0
	bought = False

	ordersFile = open("orders.txt","w+")


	while(True):


		if (begin == True):
			ema_t12 = sma(12,client)
			ema_t32 = sma(32,client)
			begin = False
			buyPrice = 0

	
		klines1 = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_15MINUTE, "15 minute ago UTC")
		formatedklines1 = format_klines(klines1)
		#print formatedklines1
		price_t = formatedklines1[0][5]
		#formated_klines40 = format_klines(klines40)
		ema_t12 = ema(price_t,12,ema_t12)
		ema_t32 = ema(price_t,32,ema_t32)


		print ("_____________________________________________________________________________")
		print("Time: %d " %(formatedklines1[0][0]))
		print("ema12 = %f" %(ema_t12))
		print("ema32 = %f" %(ema_t32))
		print("Average Price= %f" %(price_t))
		
		order_book = client.get_order_book(symbol='BTCUSDT')
		asks = order_book['asks']
		bids = order_book['bids']

		
		#print(order_book)	
		#print("here")
		#print(asks)

		bid_price = format_Lowest_Ask(bids)
		ask_price = format_Lowest_Ask(asks)
		 
		print ("Bid Price: %f" %(bid_price))
		print ("Ask Price: %f" %(ask_price))

		ordersFile = open("orders.txt","a+")
		ordersFile.write("_____________________________________________________________________________\n")
		ordersFile.write("Time: %d \n" %(formatedklines1[0][0]))
		ordersFile.write("ema12 = %f\n" %(ema_t12))
		ordersFile.write("ema32 = %f\n" %(ema_t32))

		if (ema_t12 > ema_t32 and bought == False):
			print ("Action: BUY")
			ordersFile.write("BUY at %f \n" %(ask_price))
			buyPrice = ask_price
			bought = True


		elif (ema_t12 < ema_t32 and bought == True):

			sellPrice = bid_price
			balance = sellPrice - buyPrice
			print("Action: SOLD")
			ordersFile.write("BOUGHT at %f and SOLD at %f\n" %(buyPrice,sellPrice))	
			bought = False

		else:
			print("Action: none")
			ordersFile.write("none\n")

			if(bought == True):
				print(buyTime)
				print ("Bought at %f" %(buyPrice))

				
		print ("Balance: %f" %(balance))

		ordersFile.close()	
		time.sleep(15*60)	


			
if __name__ == "__main__":
	main()





