import googleapiauth
import datetime
import webbrowser
import json

from googleapiclient.discovery import build

NOTES_FOLDER_NAME = "Notes"
TEMPLATE_DOCUMENT_ID = "1S7U5g8ct0PmUCARfso6Y_3PkcTGbKT1l1OMmSBLo8ZA"
DATE_STRING_TO_REPLACE = "MM-DD-YYYY"

# 1. Authenticate to Google
#   SCOPES needed, docs and drive
creds = googleapiauth.main()

# 2. Initialize API services
docsService = build('docs', 'v1', credentials=creds)
driveService = build('drive', 'v3', credentials=creds)

# 3. Format title for today's date
todayDateString = datetime.date.today().strftime("%m-%d-%Y")
documentTitle = "{} Notes".format(todayDateString)

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

# 6. Create document in folder  by copying template doc
    fileId = driveService.files().copy(
        fileId=TEMPLATE_DOCUMENT_ID, 
        body={
            'parents': [folderId],
            'name': documentTitle
            }
    ).execute().get("id")
    
# 7. Use batchupdate to replace header in document
    requests = [
         {
            'replaceAllText': {
                'containsText': {
                    'text': 'MM-DD-YYYY',
                    'matchCase':  'true'
                },
                'replaceText': todayDateString,
            }
         }
    ]

    docsService.documents().batchUpdate(
        documentId=fileId, 
        body={'requests': requests}
        ).execute()

# 8. Open document in browser (in a new tab preferrably, instead of window)
docsUrl = "https://docs.google.com/document/d/{}/edit#".format(fileId)
webbrowser.open(docsUrl)