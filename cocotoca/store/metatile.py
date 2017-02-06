from tilequeue.metatile import extract_metatile
from tilequeue.format import zip_format
from cStringIO import StringIO


class MetatileStore(object):

    def __init__(self, metatile_size, upstream_store):
        self.metatile_size = metatile_size
        self.upstream_store = upstream_store

    def read_tile(self, coord, fmt, layers):
        # metatile stores all layers, so quit early if the request is not for
        # all layers.
        if layers != 'all':
            return None

        raw_data = self.upstream_store.read_tile(coord, zip_format, 'all')
        if raw_data is None:
            return None

        zip_io = StringIO(raw_data)
        return extract_metatile(
            self.metatile_size, zip_io, dict(format=fmt))
