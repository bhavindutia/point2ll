'''
Author: Bhavin Dutia
Contact: bdutia@akamai.com
'''

'''
Test URLs for my troubleshooting 
http --auth-type edgegrid -a gtm: PUT :/config-gtm/v1/domains/bdutia.akadns.net/properties/test-geo  Content-Type:application/json @test-geo.json

'''

import json
from akamai.edgegrid import EdgeGridAuth
import argparse
import configparser
import requests
import os
import logging
import re


#Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')
logFile = os.path.join('logs', 'GTMPropUpdate_log.log')

headers1 = {
        "Content-Type": "application/json"
    }

#Set the format of logging in console and file seperately
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
consoleFormatter = logging.Formatter("%(message)s")
rootLogger = logging.getLogger()


logfileHandler = logging.FileHandler(logFile, mode='w')
logfileHandler.setFormatter(logFormatter)
rootLogger.addHandler(logfileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(consoleFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.INFO)

try:
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser("~"),'.edgerc'))
    client_token = config['gtm']['client_token']
    client_secret = config['gtm']['client_secret']
    access_token = config['gtm']['access_token']
    access_hostname = config['gtm']['host']
    session = requests.Session()
    session.auth = EdgeGridAuth(
    			client_token = client_token,
    			client_secret = client_secret,
    			access_token = access_token
                )
except (NameError, AttributeError, KeyError):
    rootLogger.info("\nLooks like '~/.edgerc' file is missing\n")
    exit()

#Main arguments
parser = argparse.ArgumentParser()
parser.add_argument("-help",help="Use -h for detailed help options",action="store_true")
parser.add_argument("-updateProperties",help="Enter Property Name to change",action="store_true")
parser.add_argument("-property",help="Enter property name",nargs='*')


parser.add_argument("-debug",help="DEBUG mode to generate additional logs for troubleshooting",action="store_true")

args = parser.parse_args()


if args.updateProperties:

    
    if not args.property:
        rootLogger.info('Please enter property name using -property option.')
        exit()
    
    property_names = args.property
    print (property_names)

    #Iterate through each property
    for propertyName in property_names:
        listPropertyUrl = 'https://' + access_hostname + '/config-gtm/v1/domains/bdutia.akadns.net/properties/'+propertyName
        listPropertyResponse = session.get(listPropertyUrl) 

        if listPropertyResponse.status_code == 200:
            propertyJson= json.dumps(listPropertyResponse.json(),
                indent=4, sort_keys=True,
                    separators=(',', ': '), ensure_ascii=False)
            print(f"Property:{propertyName} JSON is \n{propertyJson}")

            if (propertyName == 'www-geo'):
                handoutCnametoReplace = 'www-ip.bdutia.akadns.net'

            if (propertyName == 'store-geo'):
                handoutCnametoReplace = 'store-ip.bdutia.akadns.net'

            print (f"Handout Cname:{handoutCnametoReplace} replacement for {propertyName}")

            #new json which has replacing handout cname with localhost
            handoutCnameRegex = r".*" + re.escape(handoutCnametoReplace) + r".*"
            if re.search(handoutCnameRegex, propertyJson, re.IGNORECASE):
                print("Handout Cname Match")
                updatedPropertyJson = propertyJson.replace(handoutCnametoReplace,"localhost")
                print(f"Updated JSON is \n{updatedPropertyJson}")

                #Writing it to file so that we can reference what was written
                with open(propertyName+'.json','w',encoding='utf8') as propertyHandler:
                    propertyHandler.write(updatedPropertyJson)

                updatePropertyUrl = 'https://' + access_hostname + '/config-gtm/v1/domains/bdutia.akadns.net/properties/'+propertyName
                updatePropertyResponse = session.put(updatePropertyUrl,data=updatedPropertyJson,headers=headers)

                if updatePropertyResponse.status_code == 200:
                    print ("Update Successful")
                else:
                    print (f"Something failed for property:{propertyName} with response code:{updatePropertyResponse.status_code}")


            else:
                print("handoutcname in script is different from portal or its already pointing to localhost")


        else:
            rootLogger.info('Unable to fetch property details for propertyName')
            #exit()
