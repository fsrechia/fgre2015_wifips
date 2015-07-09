import urllib, json

web_url = 'http://robotcontrol.wilab2.ilabt.iminds.be:5056/Robot/LocationsMem'
jsonurl = urlopen(web_url)

text = json.loads(jsonurl.read())