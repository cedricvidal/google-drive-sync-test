# google-drive-sync-test

## Overview

Google Sheet -> Github repository -> Knative Build with Drools Server buildpack.

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
