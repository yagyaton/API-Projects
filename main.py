#Venv from current folder only
import requests
from twilio.rest import Client

openweather_api_key="6145ebebb8919b152b3c462cd034e5ca"
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
account_sid='ACf857a33fe35b711b4be39f7fabd7d58b'
auth_token='236a58c797e5d029228f648556ba2d0a'

if raintoday:
    client=Client(account_sid, auth_token)
    message = client.messages \
                .create(
                     body="Hi Brother, How do you do \nMight rain today.\nYours sincerely,\nTon",
                     from_='+16822551650',
                     to='+91 9460186060'
                 )

    print(message.status)

