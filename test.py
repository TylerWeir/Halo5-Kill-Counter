########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': 'f83454ddd4fb4e4da43f9752693bf8e2',
}

params = urllib.parse.urlencode({
    # Request parameters
    'modes': '',
    'start': '',
    'count': '10',
    'include-times': 'False',
})

try:
    conn = http.client.HTTPSConnection('www.haloapi.com')
    conn.request("GET", "/stats/h5/players/Endurcat14/matches?%s" % params, "Players", headers)
    response = conn.getresponse()
    data = response.read()

    print()
    print("API Returned Data:")

    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################


