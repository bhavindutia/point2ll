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
    for property_name in property_names:
        listPropertyUrl = 'https://' + access_hostname + '/config-gtm/v1/domains/bdutia.akadns.net/properties/'+property_name
        listPropertyResponse = session.get(listPropertyUrl) 

        if listPropertyResponse.status_code == 200:
            with open(property_name+'.json','w',encoding='utf8') as propertyHandler:
                propertyJson= json.dumps(listPropertyResponse.json(),
                 indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
                print(f"Property:{property_name} JSON is \n{propertyJson}")

                if (property_name == 'www-geo'):
                    handoutCnametoReplace = 'www-ip.bdutia.akadns.net'

                if (property_name == 'store-geo'):
                    handoutCnametoReplace = 'store-ip.bdutia.akadns.net1'

                print ("Handout Cname replacement ",handoutCnametoReplace,property_name)

                #new json which has replacing handout cname with localhost
                handoutCnameRegex = r".*" + re.escape(handoutCnametoReplace) + r".*"
                if re.search(handoutCnameRegex, propertyJson, re.IGNORECASE):
                    print("Handout Cname Match")
                    updatedPropertyJson = propertyJson.replace(handoutCnametoReplace,"localhost")
                    print(f"Updated JSON is \n{updatedPropertyJson}")
                    propertyHandler.write(updatedPropertyJson)


                else:
                    print("Either handout cname changed on portal or the one mentioned in this script isn't updated")


        else:
            rootLogger.info('Unable to fetch property details for property_name')
            #exit()



    '''
    #listPropertyUrl = 'https://' + access_hostname + '/config-gtm/v1/domains/bdutia.akadns.net/properties/www-geo'
    listPropertyUrl = 'https://' + access_hostname + '/config-gtm/v1/domains/bdutia.akadns.net/properties/'+property_name
    listPropertyResponse = session.get(listPropertyUrl) 

    if listPropertyResponse.status_code == 200:
         #with open('www-geo.json','w',encoding='utf8') as propertyHandler:
         with open(property_name+'.json','w',encoding='utf8') as propertyHandler:
            propertyJson= json.dumps(listPropertyResponse.json(),
                 indent=4, sort_keys=True,
                      separators=(',', ': '), ensure_ascii=False)
            print(propertyJson)

            #propertyHandler.write(propertyJson)

            propertyHandler.write(propertyJson.replace("www-ip.bdutia.akadns.net","localhost"))
 
    else:
        rootLogger.info('Unable to fetch property details')
        exit()

    with open(property_name+'.json','r') as propertyFileHandler:
            propertyRuleSet = json.loads(propertyFileHandler.read())
            propertyRuleSet = json.dumps(propertyRuleSet)
            print (propertyRuleSet)
            updatePropertyUrl = 'https://' + access_hostname + '/config-gtm/v1/domains/bdutia.akadns.net/properties/'+property_name
            updatePropertyResponse = session.put(updatePropertyUrl,data=propertyRuleSet,headers=headers1)

            if updatePropertyResponse.status_code == 200:
                print ("Update Successful")
            else:
                print ("Something failed with response code",updatePropertyResponse.status_code)
    '''
