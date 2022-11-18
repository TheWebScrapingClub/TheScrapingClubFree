# pygologin
 REST API provides programmatic access to GoLogin App. Create a new browser profile, get a list of all browser profiles, add a browser profile and running 

# class GoLogin - class for working with <a href="https://gologin.com" target="_blank">gologin.com</a> API
# Official Package

## Getting Started

GoLogin supports Linux, MacOS and Windows platforms.

### Installation

clone or download this repository

`git clone https://github.com/gologinapp/pygologin.git`

for running gologin-selenium.py install selenium

`pip install selenium`

for Selenium need download <a href="https://chromedriver.chromium.org/downloads" target="_blank">webdriver</a>

### Usage

Where is token? API token is <a href="https://app.gologin.com/#/personalArea/TokenApi" target="_blank">here</a>.
To have an access to the page below you need <a href="https://app.gologin.com/#/createUser" target="_blank">register</a> GoLogin account.

![Token API in Settings](https://user-images.githubusercontent.com/12957968/146891933-c3b60b4d-c850-47a5-8adf-bc8c37372664.gif)

### Example "gologin-selenium.py"

```py
import time
from sys import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from gologin import GoLogin
from gologin import get_random_port

# random_port = get_random_port() # uncomment to use random port

gl = GoLogin({
	"token": "yU0token",
	"profile_id": "yU0Pr0f1leiD",
	# "port": random_port
	})

if platform == "linux" or platform == "linux2":
	chrome_driver_path = "./chromedriver"
elif platform == "darwin":
	chrome_driver_path = "./mac/chromedriver"
elif platform == "win32":
	chrome_driver_path = "chromedriver.exe"

debugger_address = gl.start()
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", debugger_address)
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
driver.get("http://www.python.org")
assert "Python" in driver.title
driver.close()
time.sleep(3)
gl.stop()

```
### Running example:

`python gologin-selenium.py`

###
### Methods
#### constructor

- `options` <[Object]> Options for profile
    - `autoUpdateBrowser` <[boolean]> do not ask whether download new browser version (default false)
	- `token` <[string]> your API <a href="https://gologin.com/#/personalArea/TokenApi" target="_blank">token</a>
	- `profile_id` <[string]> profile ID
	- `executablePath` <[string]> path to executable Orbita file. Orbita will be downloaded automatically if not specified.
    - `remote_debugging_port` <[int]> port for remote debugging
	- `vncPort` <[integer]> port of VNC server if you using it
    - `tmpdir` <[string]> path to temporary directore for saving profiles
    - `extra_params` arrayof <[string]> extra params for browser orbita (ex. extentions etc.)
    - `uploadCookiesToServer` <[boolean]> upload cookies to server after profile stopping (default false)
    - `writeCookesFromServer` <[boolean]> download cookies from server and write to profile cookies file (default true)
    - `port` <[integer]> Orbita start port (uncomment out the lines with "random port" and "port" in `gologin-selenium.py` to select a random launch port)

```py
gl = GoLogin({
	"token": "yU0token",
	"profile_id": "yU0Pr0f1leiD",
	})

```
#### Example create profile
`python gologin-create-profile.py`
```py
from gologin import GoLogin


gl = GoLogin({
	"token": "yU0token",
	})

profile_id = gl.create({
    "name": 'profile_mac',
    "os": 'mac',
    "navigator": {
        "language": 'en-US',
        "userAgent": 'random', # Your userAgent (if you don't want to change, leave it at 'random')
        "resolution": '1024x768', # Your resolution (if you want a random resolution - set it to 'random')
        "platform": 'mac',
    },
    'proxyEnabled': True, # Specify 'false' if not using proxy
    'proxy': {
        'mode': 'gologin',
        'autoProxyRegion': 'us' 
        # 'host': '',
        # 'port': '',
        # 'username': '',
        # 'password': '',
    },
    "webRTC": {
        "mode": "alerted",
        "enabled": True,
    },
});

print('profile id=', profile_id);

# gl.update({
#     "id": 'yU0Pr0f1leiD',
#     "name": 'profile_mac2',
# });

profile = gl.getProfile(profile_id);

print('new profile name=', profile.get("name"));

# gl.delete('yU0Pr0f1leiD')

```

#### start()  

start browser with profile id

#### stop()  

stop browser with profile id

## Full GoLogin API
**Swagger:** <a href="https://api.gologin.com/docs" target="_blank">link here</a>

**Postman:** <a href="https://documenter.getpostman.com/view/21126834/Uz5GnvaL" target="_blank">link here</a>

