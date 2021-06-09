import json
from pathlib import Path

ENCODING='utf8'

sheetp  = Path("../.data/.sheet_data_parsed.json")

with sheetp.open(mode='r', encoding=ENCODING) as f:
    sheet_data = json.load(f)



print(json.dumps([i for i in data if "onference" in i['category'] and '2021' in i['content']['category']],indent=3))

# def filterTheDict(dictObj, callback):
#     newDict = dict()
#     # Iterate over all the items in dictionary
#     for (key, value) in dictObj.items():
#         # Check if item satisfies the given condition then add to new dict
#         if callback((key, value)):
#             newDict[key] = value
#     return newDict

#     