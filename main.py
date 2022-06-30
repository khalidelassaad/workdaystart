import googleapiauth
import datetime

from googleapiclient.discovery import build

NOTES_FOLDER_NAME = "Notes"

# 1. Authenticate to Google
#   SCOPES needed, docs and drive
creds = googleapiauth.main()

# 2. Initialize API services
docsService = build('docs', 'v1', credentials=creds)
driveService = build('drive', 'v3', credentials=creds)

# 3. Format title for today's date
documentTitle = "{} Notes".format(datetime.date.today().strftime("%m-%d-%Y"))

# 4. Find the "Notes" folder id, if it doesn't exist, create it
folder = driveService.files().list(
    corpora="user", 
    fields="files(id,name)", 
    q="name = '{}' and mimeType = 'application/vnd.google-apps.folder'".format(NOTES_FOLDER_NAME)
    ).execute().get('files', [])

if not folder:
    print("'{}' folder not found, creating folder.".format(NOTES_FOLDER_NAME))
    folderMetadata = {
            'name': NOTES_FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
        }
    folderId = driveService.files().create(body=folderMetadata, fields='id').execute().get("id")
else:
    print("'{}' folder found.".format(NOTES_FOLDER_NAME))
    folderId = folder[0]['id']    

print(folderId)


# 5. Does this title already exist in folder location?
# for file in driveService.files().list(corpora="user", fields="*", q="'1Nbb96paDsE00Bq-Y87CKF_8x6cN5pM6W' in parents").execute().get('files', []):
#     print(file['name'])

#   If so open it
#   If not...
# 6. Create document with today's title
# 7. Populate document with info from templatefile.json (replacing title)
# 8. Open document in browser (in a new tab preferrably, instead of window)