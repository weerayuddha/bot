import requests
class LicencePlate:
    def __init__(self):
        pass

    def process(self, filename):
        
        v = '1'
        c = 'th'
        sk = "sk_669bedbf9904c508fec6c614"

        url = "https://api.openalpr.com/v2/recognize?recognize_vehicle=%s&country=%s&secret_key=%s"%(v,c,sk)

        r = requests.post(url, files={'image': open(filename,'rb')})
        return r.json()


    
if __name__ == '__main__':
    lp = LicencePlate
    filename = 'car01.jpg'
    result = lp.process(filename)
    print(result)