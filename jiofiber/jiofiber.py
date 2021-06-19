from requests.sessions import session
from bs4 import BeautifulSoup
import requests
import time
import socket





# Used to create profile object for the devices connected on the JioFiber Network
class NodeProfile:
  def __init__(self,vendorName,ipv4:str,mac:str,ntime:str,ap:list,security:list):
    self.name = vendorName
    self.ipv4 = ipv4
    self.mac = mac
    self.ntime = ntime
    self.ap = ap
    self.security = security


# Main class to make sessions and function calls over the session

# Note : only one session works for one user. So if you open JioFiber Router Page on your browser 
# and try to create a session here it wont work so please close all existing sessions.

# You can make multiple sessions just make sure each session uses different username and password
class JioFiberAPI:
  # Emulated Headers for the login and Access Sessions
  loginHeaders = {

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://192.168.29.1",
    "Connection": "keep-alive",
    "Referer": "http://192.168.29.1/platform.cgi",
    "Upgrade-Insecure-Requests": "1"
  }
  loginPayLoad = {

      'thispage':'index.html',
      'button.login.users.dashboard':'Login',
      'users.username':'admin', 
      'users.password':'Kidjet.123',  
  }
  sessionHeaders ={

    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://192.168.29.1",
    "Connection": "keep-alive",
    "Referer": "http://192.168.29.1/platform.cgi",
    "Upgrade-Insecure-Requests": "1"
  }
  pkgName = "jioFiberAPI"
  

  def __init__(self, username:str, password:str):
    self.loginHeaders["username"] = username
    self.loginHeaders["password"] = password

  # createSession creates a session from the supplied username and password passed during object creation
  # the session cookie is saved and used for further operations    
  def createSession(self):

    self.session = requests.Session()
    try:
      login = loginSession=self.session.post("http://192.168.29.1/platform.cgi", data=self.loginPayLoad,headers=self.loginHeaders)
    except requests.ConnectionError:
      print(self.pkgName,": You are not connected to JIOFiber or please check your credentials")
    except Exception as e:
      print(self.pkgName,": Error: ",e)

    if(login.status_code==404):
      raise Exception(self.pkgName,": You are not connected to JIOFiber")
    elif(login.status_code==200):
      s = BeautifulSoup(login.text, 'html.parser')
      if(s.find('h1','unAuthorised')):
        raise Exception(self.pkgName,": Please check your credentials and make sure you dont have")
    else:
      self.sessionCookie = "TeamF1Login="+loginSession.cookies.get_dict()['TeamF1Login']
      #Updates SessionHeaders with cookie for usage
      self.sessionHeaders['cookie']  = self.sessionCookie

  
  #Fetchs vendor when mac is supplied 

  def getVendor(self,mac:str)->str:
    url = "https://api.macvendors.com/"
    response = requests.get(url+mac)
    if response.status_code != 200:
      raise Exception("[!] Invalid MAC Address!")
    return response.content.decode()

  # get soup will return you a soup object of the supplied page parameter.
  def getSoup(self,page_name:str):
    urlParams = {"page":""}
    urlParams['page'] = page_name
    p = self.session.get("http://192.168.29.1/platform.cgi",params=urlParams,headers=self.sessionHeaders)
    return BeautifulSoup(p.text, 'html.parser')
      
  # helper function for parsing bytes from the soup
  def decoded(self,item:str)->str:
    return item.renderContents().strip().decode("utf-8")

  # common function for fetching table from different pages.
  def getTableFromPage(self,page:str)->list:
    fList = []
    soup = self.getSoup(page)
    for row in soup.find_all("tr", class_="gradeA"):
      fList.append(list(map(self.decoded,list(row.find_all("td")))))
    if(len(fList)==0):
      print(self.pkgName,": Make sure you are not logged into to the admin panel externally and make sure to call the createSession before calling any functions.")
      return 1
    return fList  
  
  # different methods already created for fetching tables of different pages.

  def getAccessPoints(self)->list:
    return self.getTableFromPage("accessPoints.html")

  def getLanClients(self)->list:
    return self.getTableFromPage("lanDhcpLeasedClients.html")

  def getApStats(self)->list:
    return self.getTableFromPage("wirelessStatistics.html")

  def getClientStats(self)->list:
    return self.getTableFromPage("wirelessClients.html")

  def getWirelessStats(self)->list:
    return self.getTableFromPage("wirelessStatus.html")

  def getWanInfo(self)->list:
    soup = self.getSoup("wanStatus.html")
    return soup.find_all("p", class_="display")
  
  def getLanInfo(self)->list:
    soup = self.getSoup(" lanStatus.html")
    return soup.find_all("p", class_="display")
  
  def getDeviceInfo(self)->str:
    soup = self.getSoup("deviceStatus.html")
    return soup.find_all("p", class_="display")

  # check if session exists
  def isLoggedIn(self)->bool:
    return len(self.sessionCookie) > 0

  def getCookie(self)->str:
    return self.sessionCookie


  # creates profiles of devices connected over the network and returns a dictionary 
  # faster than object method
  def createNodeProfiles(self)->dict:
    dtemp = {}
    aptemp = {}
    binfo = self.getLanClients()
    ainfo = self.getClientStats()
    apinfo = self.getAccessPoints()
    for ap in apinfo:
      aptemp[ap[1]]={'code':ap[1],'name':ap[2],'status':ap[0]}
    for node in ainfo:
      try:
        temp = {
            'ap':aptemp[node[0]],
            'mac':node[1],
            'security':node[2:5],
            'ntime':node[5],
            'vname':self.getVendor(str(node[1]))
        }
        dtemp[node[1].lower()] = temp

      except:
        pass
    for node in binfo:
        try:
          dtemp[node[2]]['ipv4'] = node[0]
        except:
          pass
    return dtemp

  # creates profile object of devices connected over the network and returns a list of objects
  # slower than createNodeProfiles
  def createNodeProfileObjects(self)->list:
    profileList = []
    tProfile = self.createNodeProfiles()
    for key,data in tProfile.items():
      #self,vendorName,ipv4:str,mac:str,ntime:str,apName:str,security:list
      profileList.append(NodeProfile(data['vname'],data['ipv4'],data['mac'],data['ntime'],data['ap'],data['security'])) 
    return profileList
      



# Please Make sure to call the end session after your successful requests are completed 
# it is nescessary to end the session make sure you add a except block with endsession 
# if your python program closes without calling endsession old session remains upto 3 min before you can use the api
# so make sure you end session cleanly. Please check the given example.

  def endSession(self):
    self.session.post("http://192.168.29.1/platform.cgi",headers={'Connection':'close'})
    self.sessionHeaders['Connection'] = 'close'
    self.session.get("http://192.168.29.1/platform.cgi",params={'page':'index.html'} ,headers=self.sessionHeaders)
    self.session.close()
    
    


Api = JioFiberAPI('admin','Kidjet.123')
Api.createSession()
try:
  x = Api.createNodeProfileObjects()
  print(x[0].ap)
except:
  Api.endSession()
Api.endSession()