import json, time
from pathlib import Path
import subprocess

ENCODING='utf8'

def translateSheet(source, target, t):

    with source.open(mode='r', encoding=ENCODING) as f:
        sheet_data = json.load(f)
            
    print("Translating local sheet...")

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
                scat = t(e['gsx$category']["$t"].replace(" ","_"))
            

            data = {
                "employer":t(e["gsx$employer"]["$t"]),
                "dates":e["gsx$dates"]["$t"],
                "title":t(e["gsx$title"]["$t"]),
                "location":t(e["gsx$location"]["$t"]),
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
                "subsection" : t(e["gsx$category"]["$t"]),
            })
            
            if "data" not in subcats[scat].keys():
                subcats[scat].update({"data":[]})
            
            subcats[scat]['data'].append(data)
            
            cats[title].update({
                "section": t(e["gsx$header"]["$t"]),
                "timestamp":timestamp,
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

    source  = Path("../data/sheet_data.json")
    target  = Path("../data/sheet_data_translated-test.json")
    lang_tgt= 'de'

    def translator(text):
      t = text.replace("`","").replace("(","-").replace(")","-")
      cmd = f"trans -b -j en:{lang_tgt} {t}"
      # print(cmd)
      p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
      lines = p.stdout.read()
      # lines = " ".join([i for i in p.stdout.readlines()])
      print(lines)
      time.sleep(1)
      return lines


    translateSheet(source, target, translator)
