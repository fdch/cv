# gsheets.py - download all sheets of a google docs spreadsheet as csv

import contextlib, csv, itertools, os

from apiclient.discovery import build  # pip install google-api-python-client

SHEET = '1e5dh1sZX1QuFFioC-1ofcPIPhwU9i-lvUzOzn4_3SLQ'

def get_credentials(scopes, secrets='~/client_secrets.json', storage='~/storage.json'):
    from oauth2client import file, client, tools
    store = file.Storage(os.path.expanduser(storage))
    creds = store.get()
    if creds is None or creds.invalid:
        flow = client.flow_from_clientsecrets(os.path.expanduser(secrets), scopes)
        flags = tools.argparser.parse_args([])
        creds = tools.run_flow(flow, store, flags)
    return creds

def itersheets(id):
    doc = service.spreadsheets().get(spreadsheetId=id).execute()
    title = doc['properties']['title']
    sheets = [s['properties']['title'] for s in doc['sheets']]
    params = {'spreadsheetId': id, 'ranges': sheets, 'majorDimension': 'ROWS'}
    result = service.spreadsheets().values().batchGet(**params).execute()
    for name, vr in itertools.izip(sheets, result['valueRanges']):
        yield (title, name), vr['values']

def write_csv(fd, rows, encoding='utf-8', dialect='excel'):
    csvfile = csv.writer(fd, dialect=dialect)
    for r in rows:
        csvfile.writerow([c.encode(encoding) for c in r])

def export_csv(docid, filename_template='%(title)s - %(sheet)s.csv'):
    for (doc, sheet), rows in itersheets(docid):
        filename = filename_template % {'title': doc, 'sheet': sheet}
        with open(filename, 'wb') as fd:
            write_csv(fd, rows)

creds = get_credentials(['https://www.googleapis.com/auth/spreadsheets.readonly'])
service = build('sheets', version='v4', credentials=creds)

export_csv(SHEET)

def to_pandas(docid, **kwargs):
    from cStringIO import StringIO
    import pandas as pd
    for (doc, sheet), rows in itersheets(docid):
        with contextlib.closing(StringIO()) as fd:
            write_csv(fd, rows, encoding='utf-8', dialect='excel')
            fd.seek(0)
            df = pd.read_csv(fd, encoding='utf-8', dialect='excel', **kwargs)
        df.name = sheet
        yield df
