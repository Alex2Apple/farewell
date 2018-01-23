import time
import hashlib

def get_filename(filename):
    file = filename.lower().split('.')
    src = '%s_%s' % (file[0], time.time())
    m = hashlib.md5()
    m.update(src.encode())
    return m.hexdigest() + '.' + file[-1]