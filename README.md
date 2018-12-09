# google-drive-sync-test

## Overview

Google Sheet -> TravisCI + Github repository @ `build` -> Github repository @ `master` -> [Knative Build with Drools Server buildpack.]

NB: The Knative build part is not done yet and could be replaced with a direct docker image build.

## Workflow

- The `build` branch of this repository is built by [Travis CI](https://travis-ci.com).
- Travis CI invokes the `sync.py` script
- The `sync.py` script exports a Google Sheet identified by the `GOOGLE_SHEET_FILE_ID` environement variable as an Excel file in the `./build/` directory which is then exported to the `master` branch.

## Environment variables

| Environment variable   | Description                                                                          |
|------------------------|--------------------------------------------------------------------------------------|
| `GITHUB_TOKEN`         | Used to push the `./build` directory to the `master` branch                          |
| `GOOGLE_SHEET_FILE_ID` | ID of the Google Sheet document to export as Excel                                   |
| `GPG_KEY`              | GPG key used to decrypt the GCP Service Account JSON file `service-account.json.gpg` |

## Sample Google Script to trigger the Github build

Paste the following code in the Google Sheet script editor and replace the `<YOUR_TRAVISCI_TOKEN>`, `branch`, `user` and `repo` parameters :

```javascript
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Github')
      .addItem('Build', 'build')
      .addToUi();
}

function build() {

  var token = '<YOUR_TRAVISCI_TOKEN>';
  var branch = 'deploy';
  var user = 'cedricvidal';
  var repo = 'google-drive-sync-test';

  var headers = { 
    "Authorization" : "token " + token,
    "Travis-API-Version": "3"
  };

  var body = {
    "request": {
      "branch": branch
    }
  };

  var options =
   {
     "contentType" : "application/json",
     "method" : "post",
     "headers" : headers,
     "payload" : JSON.stringify(body)
   };

  var url = "https://api.travis-ci.com/repo/" + user +"%2F" + repo + "/requests";

  var response = UrlFetchApp.fetch(url, options);

  SpreadsheetApp.getActiveSpreadsheet()
   .toast("Published document", "Decision Table");
}

```
