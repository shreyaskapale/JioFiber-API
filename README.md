# JioFiber - API 




 [![Generic badge](https://img.shields.io/badge/Python-3.7-red.svg)](https://shields.io/) [![Generic badge](https://img.shields.io/badge/License-MIT-green.svg)](https://shields.io/) 
# Introduction
> JioFiber-API is an unofficial Python package for JioRouters. The Api can be used to get stats and configure jio router from python.
### Note:
I do not own JioFiber or any naming rights w.r.t to it .This is just an unoffical api made for jioFiber router. For any disputes related to naming of the package
send an email to : kapale.shreyas@gmail.com

### Installation
```sh
$ pip install jioFiber-Api==0.1.4
```

#### JioFiberAPI Class :
JioFiberAPI(<username>,<password>) is instantiated by username and password of your jioFiber Admin Page hosted at 192.168.29.1. The default username and password is admin and Jiocentrum. But make sure you login once externally via browser and change it.

##### NodeProfile Class:
NodeProfile consists of following data members
``` 
    name - MAC vendorName of the device
    ipv4 - local ipv4 address provided by Router (DHCP) of the device 
    mac  - MAC address of the device 
    ntime- Amount of time the device was on the network post start
    ap   - { } AP details of the device which it is on
    security - [ ]  security and auth details 
```

#### JioFiberAPI main methods:
.
#### `createSession()` 
creates a session with your jioRouter ( Logins in the router ), please make sure to logout any external browser sessions before calling this method. This method also creates a login cookie.

#### `createNodeProfiles()->dict`
returns a dictionary of all the devices connected to the jioFiber router 
```
# Format
{'9c:b2:d4:f0:e5:2f': 
    {'ap': {
                'code': 'ap1', 
                'ssid': 'AuroraHome', 
                'status': 'Enabled'
            }, 
            'mac': '9c:b2:d4:f0:e5:2f', 
            'security': ['WPA2', 'CCMP', 'PSK'], 
            'ntime': '0 days, 3 hours, 33 minutes, 42 seconds', 
            'vname': 'Rivet Networks',
            'ipv4': '192.168.29.45'
        
    }
```
#### `createNodeProfileObjects(self)->list`
returns a list of objects of device info, same as createNodeProfiles but in object form.


#### `getSoup(str)-> object`
returns the soup of the supplied param webpage.
Example - object.getSoup('accessPoints.html')

#### `getTableFromPage(str)->list`
returns the list of rows from the supplied param webage.
Example - object.getTableFromPage('accessPoints.html')

There are prebuilt methods which use getTableFromPage to fetch data from pages which contain tables
 - `getAccessPoints(str)->list < accessPoints.html >`
 - `getLanClients(str)->list < lanDhcpLeasedClients.html >`
 - `getApStats(str)->list  < wirelessStatistics.html >`
 - `getClientStats(str)->list < wirelessClients.html >`
 - `getWirelessStats(str)->list < wirelessStatus.html >`

#### Some helper functions

#### `isLoggedIn()->bool`
checks if the session exists.
#### `getCookie()->str`
returns token cookie

#### `getVendor(str)->str`
takes mac address and returns vendor uses https://api.macvendors.com/ api.

#### `decoded(str)->str`
takes byte string and decodes it




### Example
```
import jiofiber

Api = JioFiberAPI('admin','thanos.123')
Api.createSession()
try:
  print(Api.createNodeProfiles())
except:
  Api.endSession()
Api.endSession()
```
Please make sure you end the session successfully. If the program exits abruptly the session will still persist if the endSession was not called and this will stay for 3 mins until you can create new session. To avoid this put all your code inside a try except block as shown above.

## Next Goals
- Updating SSID and Password
- Device Usage Profiles
- Firewall configuration

## Contributing
Refer [CONTRIBUTING.md](CONTRIBUTING.md) for PR's and COC.


## LICENSE
MIT License 2021 
Developer - Shreyas Kapale 

