def findOrCreateFolderAndGetId(driveService, folderName):
    folderList = driveService.files().list(
        corpora="user", 
        fields="files(id,name)", 
        q="name = '{}' and mimeType = 'application/vnd.google-apps.folder'".format(folderName)
        ).execute().get('files', [])

    if not folderList:
        print("'{}' folder not found, creating it.".format(folderName))
        folderMetadata = {
                'name': folderName,
                'mimeType': 'application/vnd.google-apps.folder'
            }
        folderId = driveService.files().create(body=folderMetadata, fields='id').execute().get("id")
    else:
        print("'{}' folder found.".format(folderName))
        folderId = folderList[0]['id'] 
    return folderId

def findOrCreateNotesFileAndGetId(
    driveService, 
    docsService, 
    folderId, 
    folderName, 
    documentTitle,
    documentTemplateId,
    dateStringToReplace,
    todayDateString,):

    files = driveService.files().list(
        corpora="user",
        fields="files(id,name)",
        q="'{}' in parents and name = '{}'".format(folderId, documentTitle)
        ).execute().get('files', [])

    if files:
        print("'{}/{}' file found, opening it.".format(folderName, documentTitle))
        notesFileId = files[0]['id']
    else:
        print("'{}/{}' file not found, creating and opening it.".format(
            folderName,
            documentTitle))
        notesFileId = driveService.files().copy(
            fileId=documentTemplateId, 
            body={
                'parents': [folderId],
                'name': documentTitle
                }
        ).execute().get("id")
        requests = [
            {
                'replaceAllText': {
                    'containsText': {
                        'text': dateStringToReplace,
                        'matchCase':  'true'
                    },
                    'replaceText': todayDateString,
                }
            }
        ]

        docsService.documents().batchUpdate(
            documentId=notesFileId, 
            body={'requests': requests}
            ).execute()
    return notesFileId