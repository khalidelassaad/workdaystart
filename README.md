# workdaystart

Automation to initialize a new Google Docs notes page for the day!

By default, this script finds your "Notes" folder in Google Drive (if one does not exist, it creates one).

Inside that folder, it creates a new file from [this template](https://docs.google.com/document/d/1S7U5g8ct0PmUCARfso6Y_3PkcTGbKT1l1OMmSBLo8ZA/edit) and replaces the document title and header with today's date.

If you already have a notes page for the day, this script DOES NOT overwrite it.

Finally, the script opens today's notes in your browser.