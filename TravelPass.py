import requests


API_URL = "https://www.metaweather.com/api/"

class AverageMaxTempature:
    def __init__(self, cities):
        self.cities = [lambda i: City(i)]

    def getWeatherData(self):
        for city in self.cities:
            city.data = requests.get(API_URL,params=city.key)
        
    def printWeatherData(self):
        for city in self.cities:
            print(city.datas)


class City:
    def __init__(self, key):
        self.key = key
        self.data = None


if __name__ == "__main__":
    cities = ["2487610","2442047","2366355"]
    avg = AverageMaxTempature(cities)

