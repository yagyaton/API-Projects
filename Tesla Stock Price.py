import requests
from twilio.rest import Client

THRESHPRECENTAGE=2
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_API_KEY=alpha_api_key
FUNCTION="TIME_SERIES_DAILY"
NEWS_API_KEY=my_api_key
account_sid=my_sid
auth_token=my_auth_token

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").


response = requests.get(url=f"https://www.alphavantage.co/query?function={FUNCTION}&symbol={STOCK}&apikey={COMPANY_NAME}")
response.raise_for_status()
stockinfo=response.json()

#---------------------------------WEIRD WAY TO GET ALL INFO ABOUT LAST TWO DAYS IN A DICT-----------------------------------------#
#I know the comprehension below is a bit hard to comprehend. You created a list of dates by type coversion of stockinfo['Time Series (Daily)]
#and then slides it for the first two elements, which are the latest two dates, yesterday and day before
#After that, key is each element in that list, and value is its value in the original dictionary. 
#That is all.
# dayandbefore={list(stockinfo['Time Series (Daily)'])[:2][n] : stockinfo['Time Series (Daily)'][list(stockinfo['Time Series (Daily)'])[:2][n]] for n in range(len(list(stockinfo['Time Series (Daily)'])[:2]))}
# print(dayandbefore)
#---------------------------------------------------------------------------------------------------------------------------------#



#---------------------------------FUNCTION TO COMPARE STOCK PRICES OF LAST TWO DAYS-----------------------------------------------#
def lets_compare_stocks(x,y):
    diff=x-y
    perc=(abs(diff)/x)*100
    if diff>=0:
        return (perc, "🔺")
    else:
        return (perc, "🔻")

#---------------------------------------------------------------------------------------------------------------------------------#



#---------------------------------GETTING CLOSING STOCK PRICE FOR LAST TWO DAYS---------------------------------------------------#
lasttwodays=list(stockinfo['Time Series (Daily)'])[:2]
yesterdayclose=float(stockinfo['Time Series (Daily)'][lasttwodays[0]]['4. close'])
daybeforeclose=float(stockinfo['Time Series (Daily)'][lasttwodays[1]]['4. close'])

(percentage, symbol)=lets_compare_stocks(yesterdayclose, daybeforeclose)
print(percentage, symbol)
# if percentage>=2:
#     print("Get News!")
#---------------------------------------------------------------------------------------------------------------------------------#



#------------------------------GETTING NEWS IF PERCENTAGE ABOVE THRESHHOLD--------------------------------------------------------#
## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
if percentage>=THRESHPRECENTAGE:
    newsresponse=requests.get(url=f"https://newsapi.org/v2/everything?q={COMPANY_NAME}&language=en&to={daybeforeclose}&sortBy=publishedAt&apiKey={NEWS_API_KEY}")
    newsresponse.raise_for_status()
    news=newsresponse.json()
    # print(news['articles'][:3])
    newsdict={n:{'Headline': news['articles'][n]['title'], 'Brief': news['articles'][n]['description']} for n in range(len(news['articles'][:3]))}
    news1=f"Headline: {newsdict[0]['Headline']}\nBrief: {newsdict[0]['Brief']}\n"
    news2=f"Headline: {newsdict[1]['Headline']}\nBrief: {newsdict[1]['Brief']}\n"
    news3=f"Headline: {newsdict[2]['Headline']}\nBrief: {newsdict[2]['Brief']}\n"
    # print(news1)
    # print(news2)
    # print(news3)
# print(newsdict)
#---------------------------------------------------------------------------------------------------------------------------------#



#----------------------------SENDING THE MESSAGE IF PERCENTAGE ABOVE THRESHHOLD VALUE---------------------------------------------#
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
    client=Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body=f"\n{STOCK}: {symbol}{round(percentage,2)}%\n{news1}\n{news2}\n{news3}",
                     from_='+16822551650',
                     to='+91 9460186060'
                 )

    print(message.status)
#---------------------------------------------------------------------------------------------------------------------------------#



