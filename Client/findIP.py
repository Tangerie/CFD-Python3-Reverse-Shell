import urllib.request

def getIP(url, ip):
	if url:
		try:
			return urllib.request.urlopen(url).readlines()[0].decode()
		except:
			return ip
	else:
		return ip