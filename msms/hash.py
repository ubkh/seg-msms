from hashids import Hashids
from django.conf import settings

hashids = Hashids(settings.HASHID_SALT, settings.HASHID_LENGTH)

def encode(id):
    return hashids.encode(id)

def decode(id):
    a = hashids.decode(id)
    if a:
        return a[0]

class HashIDConverter:
    regex = '[a-zA-Z0-9]{8,}'

    def to_python(self, value):
        return decode(value)

    def to_url(self, value):
        return encode(value)