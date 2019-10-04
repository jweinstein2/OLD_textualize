import json

CONFIG_PATH = 'application.conf'
BACKUP_KEY = 'backup'
PROCESS_PROGRESS_KEY = 'analysis_progress'
LAST_ERROR_KEY = 'last_error'
default_configuration = {}

def get_last_error():
    return _get(LAST_ERROR_KEY)

def set_last_error(value):
    _set(LAST_ERROR_KEY, value)

def del_last_error():
    _del(LAST_ERROR_KEY)

def get_backup_path():
    return _get(BACKUP_KEY)

def set_backup_path(value):
    _set(BACKUP_KEY, value)

def del_backup_path():
    _del(BACKUP_KEY)

def get_process_progress():
    return _get(PROCESS_PROGRESS_KEY)

def set_process_progress(value):
    _set(PROCESS_PROGRESS_KEY, value)

def del_process_progress():
    _del(PROCESS_PROGRESS_KEY)

# MARK: helper methods
# TODO: This should have a read write lock
# http://effbot.org/zone/thread-synchronization.htm
def _get(key):
    config = _read()
    return config.get(key)

def _set(key, value):
    config = _read()
    config[key] = value
    _write(config)

def _del(key):
    config = _read()
    config.pop(key, None)
    _write(config)

def _read():
    # default configuration
    config = default_configuration

    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
    except IOError:
        _write(config)
    except:
        print("invalid JSON")
        _write(config)

    return config

def _write(dic):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(dic, f)
