import googleapiauth
import datetime
import webbrowser
import json

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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
folderList = driveService.files().list(
    corpora="user", 
    fields="files(id,name)", 
    q="name = '{}' and mimeType = 'application/vnd.google-apps.folder'".format(NOTES_FOLDER_NAME)
    ).execute().get('files', [])

if not folderList:
    print("'{}' folder not found, creating it.".format(NOTES_FOLDER_NAME))
    folderMetadata = {
            'name': NOTES_FOLDER_NAME,
            'mimeType': 'application/vnd.google-apps.folder'
        }
    folderId = driveService.files().create(body=folderMetadata, fields='id').execute().get("id")
else:
    print("'{}' folder found.".format(NOTES_FOLDER_NAME))
    folderId = folderList[0]['id']    

# 5. Does this title already exist in folder location?
# TODO: REMOVE THIS DEBUG LINE:
# documentTitle += "OK"

files = driveService.files().list(
    corpora="user",
    fields="files(id,name)",
    q="'{}' in parents and name = '{}'".format(folderId, documentTitle)
    ).execute().get('files', [])

#   If so open it
if files:
    print("'{}/{}' file found, opening it.".format(NOTES_FOLDER_NAME, documentTitle))
    fileId = files[0]['id']
    
#   If not...
else:
    print("'{}/{}' file not found, creating and opening it.".format(
        NOTES_FOLDER_NAME,
        documentTitle))
# 6. Create document in Notes folder with today's title 
    file_metadata = {
        'name': documentTitle,
        'mimeType':'application/vnd.google-apps.document',
        'parents': [folderId]
    }
    file = driveService.files().create(
        body=file_metadata,
        fields='id'
        ).execute()
    fileId = file['id']

# 7. Populate document with template data via docs api
# templateJson = json.load(open("documentJSONs/templatefile.json", "r"))
# docsService.documents().batchUpdate(fileId, body=templateJson) # TODO: Make this guy actually update the file

# 8. Open document in browser (in a new tab preferrably, instead of window)
docsUrl = "https://docs.google.com/document/d/{}/edit#".format(fileId)
webbrowser.open(docsUrl)