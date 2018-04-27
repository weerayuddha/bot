import json

result = open('result.json','r')
l = result.read()
result.close()

l = l.replace("'",'"')
l = l.replace("False",'false')
l = l.replace("True",'true')
# print(l)

obj = json.loads(l)
print(json.dumps(obj, sort_keys=True, indent=4))
