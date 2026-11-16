import hashlib


class HashReader:
    def __init__(self, stream, guard):
        self.stream, self.guard, self.digest = stream, guard, hashlib.sha256()

    def read(self, size=-1):
        self.guard.check()
        raw = self.stream.read(size)
        self.digest.update(raw)
        return raw
