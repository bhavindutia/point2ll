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
* Update multiple GTM properties belonging to a domain and point them to localhost using command line 

### Usage
python3 point2ll.py -updateProperties -property [LIST OF PROPERTIES]
* e.g. python3 point2ll.py -updateProperties -property www-geo store-geo

