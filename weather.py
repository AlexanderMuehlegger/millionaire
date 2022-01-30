import requests
import ids


class Weather:
    base_url = 'http://api.openweathermap.org/data/2.5/'

    def get_pollution(self):
        lat = '47.262691'
        lon = '11.394700'
        response = requests.get(self.base_url + 'air_pollution?lat={}&lon={}&APPID={}'.format(lat, lon, ids.openweathermap_key)).json()
        return_array = []
        return_array.append('CO: ' + str(response['list'][0]['components']['co']))
        return_array.append('O3: ' + str(response['list'][0]['components']['o3']))
        print(return_array)

    def get_weather(self):
        response = requests.get(self.base_url + 'weather?q=Innsbruck&units=matric&APPID=' + ids.openweathermap_key).json()
        return_array = []
        return_array.append(response['weather'][0]['main'])
        return_array.append(str(response['main']['temp']) + " C°")
        print (return_array)


weather1 = Weather()

weather1.get_weather()
weather1.get_pollution()