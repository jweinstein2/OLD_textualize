# Textualize

Pulling out insights from message history.

### Prerequisites

This project only works for iOS devices: android is currently unsupported.

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
