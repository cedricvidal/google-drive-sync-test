from __future__ import print_function
from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
import os
from apiclient.http import MediaIoBaseDownload
import pathlib
import json

# Default scope seems to be sufficient
SCOPES = []

def main():

    credentials = service_account.Credentials.from_service_account_file(
        os.getenv('GOOGLE_APPLICATION_CREDENTIALS', './service-account.json'), scopes=SCOPES)

    drive_service = build('drive', 'v3', credentials=credentials)

    file_id = os.environ['GOOGLE_SHEET_FILE_ID']

    # Get file name
    results = drive_service.files().get(
        fileId=file_id, fields="name, id").execute()
    name = results.get('name')
    print("Goodle sheet file name is %s" % name)

    # Download file
    request = drive_service.files().export_media(fileId=file_id,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    build_dir = './build'
    pathlib.Path(build_dir).mkdir(parents=True, exist_ok=True) 
    path = pathlib.PurePath(build_dir, name + '.xlsx')
    print("Exporting to %s" % path)
    fh = io.FileIO(path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))


if __name__ == '__main__':
    main()
