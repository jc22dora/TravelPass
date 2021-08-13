import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import uuid

API_URL = "https://www.metaweather.com/api/location/"

class AverageMaxTempature:
    def __init__(self, keys):
        self.cities = APICall(keys).tasks
        self.cities = [City(city) for city in self.cities]

    def printAverages(self):
        for city in self.cities:
            print(city.title+" Average Max Temp: ",city.average)


class City:
    def __init__(self, data):
        self.json = json.loads(data.text)
        self.key = self.json["woeid"]
        self.consolidated_weather = self.json["consolidated_weather"]
        self.max_temps = [self.consolidated_weather[i]["max_temp"] for i in range(5)]
        self.average = round(sum(self.max_temps)/len(self.max_temps), 2)
        self.title = self.json["title"]
        

    def getWeatherData(self):
        return requests.get(API_URL+self.key)

class APICall:
    def __init__(self, keys):
        self.keys = keys
        self.tasks =  []
        self.runner()

    def getData(self, key):
        try:
            response = requests.get(API_URL+key, stream=True)
            return response
        except requests.exceptions.RequestException as e:
            return e
            
    def runner(self):
        threads = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            for key in self.keys:
                threads.append(executor.submit(self.getData, key))
            
            for task in as_completed(threads):
                self.tasks.append(task.result())




if __name__ == "__main__":
    cityKeys = ["2487610","2442047","2366355"]
    test = AverageMaxTempature(cityKeys)
    test.printAverages()

