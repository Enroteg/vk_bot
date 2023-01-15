import time
import requests
import json

start = time.time()

link = 'https://api.opendota.com/api/players/146636026'
r = requests.get(link)
data = r.json()
#print(data)
print(str(data['rank_tier'])+" "+str(time.time()-start))
