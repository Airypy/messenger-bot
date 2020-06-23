import requests



def weather_be(city_name,time):
    url="http://api.openweathermap.org/data/2.5/forecast?q="+city_name+"&appid=b562f058be2d3259938133d7996169ce"
    json_data=requests.get(url).json()
    temp=None
    scheduled=None

    weather=json_data['list']
    for day in weather:
        l_current_day=day['dt_txt'].split()
        current_day=l_current_day[0]
        scheduled=l_current_day[1]
        if current_day==time:
            temp=day['main']['temp']


    return temp-273.5,scheduled
