from tilequeue.store import make_s3_store
from tilequeue.store import make_tile_file_store


def make_store(store_type, store_name, store_config):
    if store_type == 'directory':
        return make_tile_file_store(store_name)

    elif store_type == 's3':
        path = store_config.get('path', 'osm')
        date_prefix = store_config.get('date-prefix', '')
        reduced_redundancy = store_config.get('reduced_redundancy', True)
        return make_s3_store(
            store_name, path=path, reduced_redundancy=reduced_redundancy,
            date_prefix=date_prefix)

    else:
        raise ValueError('Unrecognized store type: `{}`'.format(store_type))
