import json
from pathlib import Path

ENCODING='utf8'

def parseSheet(source,target):

    with source.open(mode='r', encoding=ENCODING) as f:
        spreadsheets = json.load(f)

    print("Parsing local sheet...")

    cats = {}

    for sheet in spreadsheets:

        title = sheet['range'].split("!")[0].replace("Final","").replace("Translated","")
        if title not in cats.keys():
            cats.update({title:{}})
        keys = sheet['values'][0]

        subcats = {}

        for e in sheet['values'][1:]:

            def get(key):
                idx = keys.index(key.title())
                # print(key, idx, e)
                if len(e) > idx and "#VALUE!" not in e[idx]:
                  return e[idx] # .replace("``","\"")
                else:
                  try:
                    return e[idx]
                  except Exception as ex:
                    print("Could not find key:", idx, len(e), ex)
                  finally:
                    return ""

            if not get('Category'):
                # print("NOSUBCAT: "+ get("Header") + " " +get("Title"))
                scat = 'undefined'
            else:
                scat = get("Category").replace(" ","_")

            data = {
                "employer":get("employer"),
                "dates":get("dates"),
                "title":get("title"),
                "location":get("location"),
                "year":get("year"),
                "month":get("month"),
                "description":get("description"),
                "narrative":get("narrative"),
                "url":get("url"),
                "timestamp" : get("timestamp"),
            }

            if scat not in subcats.keys():
                subcats.update({scat:{}})

            subcats[scat].update({
                "subsection" : get('Category'),
            })

            if "data" not in subcats[scat].keys():
                subcats[scat].update({"data":[]})

            subcats[scat]['data'].append(data)

            cats[title].update({
                "section": get('Header'),
                "timestamp":"",
                "subcategories":subcats,
            })

    sheet_dicts = cats

    with target.open(mode='wb') as f:
        f.write(json.dumps(sheet_dicts, 
            sort_keys=True,
            indent=4,
            separators=(',',':'),
            ensure_ascii=False,
            ).encode(ENCODING)
        )

if __name__ == '__main__':

    source  = Path("../data/sheets_english.json")
    target  = Path("../data/sheets_english-parsed-test.json")

    parseSheet(source, target)

    source2  = Path("../data/sheets_german.json")
    target2  = Path("../data/sheets_german-parsed-test.json")

    parseSheet(source2, target2)
