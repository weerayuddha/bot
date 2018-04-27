import requests

# curl -X POST -F image=@test01.jpg "https://api.openalpr.com/v2/recognize?recognize_vehicle=1&country=th&secret_key=sk_e10fd59fb8ae37caf154ae5e"
v = '1'
c = 'th'
sk = "sk_xxxxx"

url = "https://api.openalpr.com/v2/recognize?recognize_vehicle=%s&country=%s&secret_key=%s"%(v,c,sk)
filename = 'test02.jfif'

r = requests.post(url, files={'image': open(filename,'rb')})
print(r.json())
