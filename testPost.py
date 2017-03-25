from urllib import request, parse

params = {'person':'elie'}
url = 'http://localhost:9000/testPost'

# Encode the query string
querystring = parse.urlencode(params)

# Make a POST request and read the response
u = request.urlopen(url, querystring.encode('ascii'))
mp3Response = u.read()
print(mp3Response)
