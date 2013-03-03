'''
Created on Feb 26, 2013

@author: Kaiqun
'''

import json
import httplib
from time import sleep

def CityInput():
    try:
        OutCities = open('Output.txt', 'w')
        RawFile = open('RawCities.txt', 'r')

        i = 0
        for line in RawFile:
            if '(' in line:
                continue
            OutCities.write(line.split(",")[0].replace(' ', '+') + '|' + line.split(",")[1].strip() + '\n')

        OutCities.close()

    except Exception, e:
        print e

def CityFinal():
    OutCities = open('FinalOutput.txt', 'w')
    inputFile = open('Output.txt', 'r')
    for line in inputFile:
        flag = 0
        oneRslt = line.split("|")
        conn = httplib.HTTPConnection("maps.googleapis.com")
        conn.request("GET", "/maps/api/geocode/json?address=" + oneRslt[0] + "&sensor=false")
        r1 = conn.getresponse().read()
        json1 = json.loads(r1)
#        print json1["status"]
        for jsonobj in json1["results"]:
            try:
                for jobj in jsonobj["address_components"]:
                    if jobj["types"][0] == "country":
                        Nation = jobj["long_name"]
                        flagNat = jobj["short_name"]
                    if jobj["types"][0] == "administrative_area_level_1":
                        State = jobj["long_name"]
                        flagSta = jobj["short_name"]
                latitude = jsonobj["geometry"]["location"]["lat"]
                longitude = jsonobj["geometry"]["location"]["lng"]
                if flagNat != "US" or flagSta != "CA":
                    continue
                finalString = Nation + "|" + State + "|" + oneRslt[0] + "|\\N|" + str(latitude) + "," + str(longitude)
                OutCities.write(finalString + '\n')
                print oneRslt[0] + "|" + str(latitude) + "," + str(longitude)
            except Exception, e:
                print e
                pass

        sleep(0.2)

    OutCities.close()

def main():
    CityInput()
#    CityFinal()

if  __name__ == '__main__':
    main()
