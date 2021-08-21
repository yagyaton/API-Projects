#Venv from current folder only
import requests
from twilio.rest import Client

openweather_api_key=op_key
MYLAT=28.354204
MYLNG=75.592577

#Pskov is a city in Russia, just used it's coordinates to check if the rain check conditions were working or not.
PSKOVLAT=57.815231
PSKOVLNG=28.339581



#Including Lat, Long, API key in the url, also excluding current, minutely and daily forcasts.
response=requests.get(url=f'https://api.openweathermap.org/data/2.5/onecall?lat={MYLAT}&lon={MYLNG}&exclude=current,minutely,daily&appid={openweather_api_key}')
response.raise_for_status()

weatherdata=response.json()
weather12hrs=weatherdata['hourly'][:12]

raintoday=False
for eachhour in weather12hrs:
    # print(type(eachhour['weather'][0]['id']))
    # print(eachhour['weather'][0]['id'])
    if eachhour['weather'][0]['id']<700:
        # print("Bring an Umbrella")
        raintoday=True

print(raintoday)


#----------------------Sending myself a message using my account credentials on Twilio----------------------------------#
account_sid=xyz
auth_token=abc

if raintoday:
    client=Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body="Hi Brother, How do you do \nMight rain today.\nYours sincerely,\nTon",
                     from_=twilionumber,
                     to=myno
                 )

    print(message.status)

