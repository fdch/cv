import json
from pathlib import Path
import requests

MAX_SHEETS     = 9     # range of sheets to pull from (non inclusive)
ENCODING       = 'utf8'
sheet_data     = []

def downloadSheet(sheet_id, target, maxsheets=MAX_SHEETS, offset=False):

    print("Updating local sheet...")
    if offset:
      SHEET_OFFSET = MAX_SHEETS
    else:
      SHEET_OFFSET = 0

    for i in range(maxsheets):
        num = i + 1 + SHEET_OFFSET
        url = f"https://spreadsheets.google.com/feeds/list/{sheet_id}/{num}/public/values?alt=json"
        print(url)
        try:
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
    
    with Path("../data/sheet_id.pkl").open(mode='rb') as f:
        downloadSheet(pickle.load(f), Path("../data/sheet_1.json"),8)
    
    with Path("../data/sheet_id_website.pkl").open(mode='rb') as f:
        downloadSheet(pickle.load(f), Path("../data/sheet_2.json"),6)
    

