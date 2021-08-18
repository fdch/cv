import json
from pathlib import Path

ENCODING='utf8'

def parseSheet(source,target):

    with source.open(mode='r', encoding=ENCODING) as f:
        sheet_data = json.load(f)
            
    print("Parsing local sheet...")

    cats = {}

    for s in sheet_data:
        feed = s['feed']
        title = feed['title']['$t']
        entry = feed['entry']
        timestamp = feed['updated']['$t']

        if title not in cats.keys():
            cats.update({title:{}})

        subcats = {}

        for e in entry:
            if not e['gsx$category']["$t"]:
                print("NOSUBCAT: "+ e["gsx$header"]["$t"] + " " +e["gsx$title"]["$t"])
                scat = 'undefined'
            else:
                scat = e['gsx$category']["$t"].replace(" ","_")
            

            data = {
                "employer":e["gsx$employer"]["$t"],
                "dates":e["gsx$dates"]["$t"],
                "title":e["gsx$title"]["$t"],
                "location":e["gsx$location"]["$t"],
                "year":e["gsx$year"]["$t"],
                "month":e["gsx$month"]["$t"],
                "description":e["gsx$description"]["$t"],
                "narrative":e["gsx$narrative"]["$t"],
                "url":e["gsx$url"]["$t"],
                "timestamp" : e["gsx$timestamp"]["$t"],
            }
            
            if scat not in subcats.keys():
                subcats.update({scat:{}})
            
            subcats[scat].update({
                "subsection" : e["gsx$category"]["$t"],
            })
            
            if "data" not in subcats[scat].keys():
                subcats[scat].update({"data":[]})
            
            subcats[scat]['data'].append(data)
            
            cats[title].update({
                "section": e["gsx$header"]["$t"],
                "timestamp":timestamp,
                "subcategories":subcats,
            })


    # for i in cats:
    #     for j in cats[i]['subcategories']:
    #         emp = {}
    #         for k in cats[i]['subcategories'][j]['data']:
    #             # print(k)
    #             kk = cats[i]['subcategories'][j]['data']
    #             empkey = k['employer'].replace(" ","_")
    #             if k['employer'] not in kk:
    #                 emp.update({empkey:[]})
    #             for key,value in k.items():
    #                 # print(key,value)
    #                 if 'employer' not in key:
    #                     emp[empkey].append(value)
    #         cats[i]['subcategories'][j]['data'] = emp


    sheet_dicts = cats


    with target.open(mode='wb') as f:
        f.write(json.dumps(sheet_dicts, 
            sort_keys=True,
            indent=4,
            separators=(',',':'),
            ensure_ascii=False,
            ).encode(ENCODING)
        )

def listOut(source):

    data=[]

    with source.open(mode='r', encoding=ENCODING) as f:
        sheet_data = json.load(f)

    for s in sheet_data:
        feed = s['feed']
        title = feed['title']['$t']
        entry = feed['entry']

        for e in entry:
            en = {}
            for k,v in e.items():
                if 'gsx' in k:
                    en.update({k.replace('gsx$',''):v["$t"]})
            data.append(en)

    for i in data:
        print(json.dumps(i,
            indent=4,
            sort_keys=True,
            ensure_ascii=True)+",")

    # with target.open(mode='wb') as f:
    #     f.write(json.dumps(sheet_dicts, 
    #         sort_keys=True,
    #         indent=4,
    #         separators=(',',':'),
    #         ensure_ascii=False,
    #         ).encode(ENCODING)
    #     )
if __name__ == '__main__':

    source  = Path("../.data/.sheet_data.json")
    target  = Path("../.data/.sheet_data_parsed-test.json")

    # parseSheet(source, target)
    print("[")
    listOut(Path("../.data/.sheet_1.json"))
    listOut(Path("../.data/.sheet_2.json"))
    print("]")

