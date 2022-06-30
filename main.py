import googleapiauth
import datetime
import json

from googleapiclient.discovery import build

# 1. Authenticate to Google
#   SCOPES needed, docs and drive
creds = googleapiauth.main()

# 2. Initialize API services
docsService = build('docs', 'v1', credentials=creds)
driveService = build('drive', 'v3', credentials=creds)

# 3. Format title for today's date
documentTitle = "{} Notes".format(datetime.date.today().strftime("%m-%d-%Y"))

# 4. Does this title already exist in folder location?
for file in driveService.files().list(corpora="user", fields="*").execute().get('files', []):
    if file['id'] == "1Nbb96paDsE00Bq-Y87CKF_8x6cN5pM6W":
        print(json.dumps(file))
#   If so open it
#   If not...
# 5. Create document with today's title
# 6. Populate document with info from templatefile.json (replacing title)
# 7. Open document in browser (in a new tab preferrably, instead of window)