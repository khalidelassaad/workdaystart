import datetime
import googleapiauth
import googleapiactions
import webbrowser

from googleapiclient.discovery import build

def createAndOpenTodaysNotes(notesFolderName, templateDocumentId, dateStringToReplace):
    # 1. Authenticate to Google API
    creds = googleapiauth.main()

    # 2. Initialize API services
    docsService = build('docs', 'v1', credentials=creds)
    driveService = build('drive', 'v3', credentials=creds)

    # 3. Format document title with today's date
    todayDateString = datetime.date.today().strftime("%m-%d-%Y")
    documentTitle = "{} Notes".format(todayDateString)

    # 4. Find the "Notes" folder id, if it doesn't exist, create it
    folderId = googleapiactions.findOrCreateFolderAndGetId(driveService, notesFolderName)

    # 5. Find today's notes file id, if it doesn't exist, create it
    notesFileId = googleapiactions.findOrCreateNotesFileAndGetId(
        driveService,
        docsService,
        folderId,
        notesFolderName,
        documentTitle,
        templateDocumentId,
        dateStringToReplace,
        todayDateString
    )

    # 6. Open document in browser
    docsUrl = "https://docs.google.com/document/d/{}/edit#".format(notesFileId)
    webbrowser.open(docsUrl)

if __name__ == "__main__":
    createAndOpenTodaysNotes(
        notesFolderName="Notes",
        # All Algolians have viewer access to this template
        templateDocumentId="1S7U5g8ct0PmUCARfso6Y_3PkcTGbKT1l1OMmSBLo8ZA", 
        dateStringToReplace="MM-DD-YYYY"
    )