import json
from pathlib import Path
import requests

MAX_SHEETS=8
ENCODING='utf8'
sheet_data = []

def downloadSheet(sheet_id, target, maxsheets=MAX_SHEETS):

    print("Updating local sheet...")

    for i in range(maxsheets):
        try:
            url  = "https://spreadsheets.google.com/feeds/list/" 
            url += sheet_id + "/"
            url += str(i+1)   + "/" 
            url += "public/values?alt=json"
            r = requests.get(url)
            data = json.loads(r.text)
            sheet_data.append(data)
        except Exception as e:
            print(e)

    with target.open(mode='wb') as f:
        f.write(json.dumps(sheet_data, 
            sort_keys=True,
            indent=4,
            separators=(',',':'),
            ensure_ascii=False,
            ).encode(ENCODING)
        )

if __name__ == '__main__':
    import pickle
    
    with Path("../.data/.sheet_id.pkl").open(mode='rb') as f:
        downloadSheet(pickle.load(f), Path("../.data/.sheet_1.json"),8)
    
    with Path("../.data/.sheet_id_website.pkl").open(mode='rb') as f:
        downloadSheet(pickle.load(f), Path("../.data/.sheet_2.json"),6)
    

