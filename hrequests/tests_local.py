import hrequests

session = hrequests.Session('chrome')
tls_test=session.get('https://tls.browserleaks.com/json')
print(tls_test.text)