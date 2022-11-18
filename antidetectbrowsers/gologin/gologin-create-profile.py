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
        # "host": '',
        # "port": '',
        # "username": '',
        # "password": '',
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