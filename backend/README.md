# Textualize

Pulling out insights from message history.

### Prerequisites

This project only works for iOS devices: android is currently unsupported.

You may have to grant full disk access to your terminal application.
http://osxdaily.com/2018/10/09/fix-operation-not-permitted-terminal-error-macos/

### Dependencies

### Setup

1. Create an unencrypted backup of your iOS device. This allows access to the
   data in Messages and Contacts.
2. Under the configuration section of `setup.py` add the correct path location
   to your unencrypted backup. It should be located under `Library/Application
   Support/MobileSync/Backup/[DEVICE_HASH]` for Mac users. For more information
   and backup locations on windows [http://osxdaily.com/2010/07/08/read-iphone-sms-backup/]
3. run `python3 setup.py`.
4. run `python3 analyze.py`.

### TODO

1. Deploy on Heroku
   https://realpython.com/flask-by-example-part-1-project-setup/
2. Analyze should only updates the pickles so that stats can calculate with ease
   Analyze and preprocess should be grouped into one function that does setup

