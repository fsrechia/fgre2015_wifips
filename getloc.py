import simplejson

x = open("LocationsMem").read()
y = simplejson.loads(x)

print y


