# -*- coding: utf-8 -*-
import zipfile
import StringIO
import time

class storage_type(object):
    file_based = "file based storage"
    memory_based = "memory based storage"

def get_storage(name):
    if name == storage_type.file_based:
        return storage_file_based()
    elif name == storage_type.memory_based:
        return storage_memory_based()
    raise docvert_exception.unrecognised_storage_type("Unknown storage type '%s'" % name)

class storage(object):
    def __init__(self, *args, **kargs):
        raise NotImplemented()

    def __setitem__(self, key, value):
        self.add(key, value)

    def has_key(self, key):
        return self.storage.has_key(key)

    def __getitem__(self, key):
        return self.get(key)

class storage_file_based(storage):
    def __init__(self):
        self.working_directory = tempfile.mkdtemp()
        self.created_at = time.time()

    def add(self, path, data):
        handler = open(os.path.join(self.working_directory, path), 'w')
        handler.write(data)
        handler.close()

    def get(self, path):
        handler = open(os.path.join(self.working_directory, path), 'r')
        return handler.read()

    def _dispose(self):
        os.removedirs(self.working_directory)

    def getzip(self):
        raise NotImplemented("Not implemented, yet...")

    def __str__(self):
        return '<file based storage at path "%s">' % self.working_directory


class storage_memory_based(storage):
    def __init__(self):
        self.storage = dict()
        self.created_at = time.time()

    def add(self, path, data):
        self.storage[path] = data

    def get(self, path):
        return self.storage[path]

    def to_zip(self):
        zipdata = StringIO.StringIO()
        archive = zipfile.ZipFile(zipdata, 'w')
        for key, value in self.storage.iteritems():
            archive.writestr(key.replace("\\", "/").encode("utf-8"),value)
        archive.close()
        return zipdata

    def _dispose(self):
        pass

    def __str__(self):
        return '<memory based storage with these keys "%s">' % self.storage.keys()
