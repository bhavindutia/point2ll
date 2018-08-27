# point2ll

Provides a way to multiple update GTM properties via Open APIs and without manually having to go into the Luna Portal. 

## Local Install
* Python 3+
* pip install edgegrid-python

### Credentials
In order to use this module, you need to:
* Set up your credential files as described in the [authorization](https://developer.akamai.com/introduction/Prov_Creds.html) and [credentials](https://developer.akamai.com/introduction/Conf_Client.html) sections of the Get Started pagegetting started guide on developer.akamai.com (the developer portal).
* When working through this process you need to give grants for the Global Traffic Management API.  The section in your configuration file should be called 'gtm'.

## Functionality
This program provides the following functionality:
 1. Update handout cname of multiple GTM properties(In this case from valid cname to localhost). Input to this program comes from file 'propertyToHandOutCname' file, which has entries like PROPERTY_NAME=HANDOUT_CNAME_TO_REPLACE
 2. Reverse the above change. Point properties back to original state (before 1)HANDOUT_CNAME_TO_REPLACE from localhost


### Usage
python3 point2ll.py -updateCnameToLh -property [LIST OF PROPERTIES]
* e.g. python3 point2ll.py -updateLhToCname -property www-geo store-geo

python3 point2ll.py -updateLhToCname -property [LIST OF PROPERTIES]
* python3 point2ll.py -updateLhToCname -property www-geo store-geo


