from .cocotoca import Overzoomer
from cocotoca.store import make_store
from cocotoca.store.metatile import MetatileStore
from ModestMaps.Core import Coordinate
from flask import Flask, abort, g
from tilequeue.format import lookup_format_by_extension
import os
import yaml


app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('COCOTOCA_SETTINGS', silent=True)


def _parse_config():
    """
    Create an Overzoomer object and the list of all available layer names by
    parsing the configuration files. This should only be called a small number
    of times, as it is cached in the Flask application.
    """

    config_file = os.environ['COCOTOCA_CONFIG']
    with open(config_file, 'r') as fh:
        config = yaml.load(fh)

    tile_store = None
    store_config = config.get('store')
    if store_config is not None:
        store_type = store_config.get('type')
        store_name = store_config.get('name')
        if store_type and store_name:
            tile_store = make_store(store_type, store_name, store_config)

    assert tile_store is not None, \
        "Tile store could not be configured, but is required. Please check " \
        "your configuration."

    # if metatiles are enabled, then wrap the store in a metatile decoder.
    metatile_size = None
    metatile_config = config.get('metatile')
    if metatile_config:
        metatile_size = metatile_config.get('size')

    if metatile_size is not None:
        tile_store = MetatileStore(metatile_size, tile_store)

    # TODO: this seems to be hardcoded in tileserver - should we make it
    # configurable here?
    max_z = 16
    buffer_cfg = config.get('buffer', {})
    all_layer_names = config.get('layer_names', [])

    return Overzoomer(tile_store, max_z, buffer_cfg), all_layer_names


def get_overzoomer():
    """
    Fetch pre-cached Overzoomer object, or create one.
    """

    oz = getattr(g, '_overzoomer', None)
    if oz is None:
        g._overzoomer, g._all_layer_names = _parse_config()
        oz = g._overzoomer
    return oz


def get_all_layer_names():
    """
    Fetch pre-cached layer names, or read the config to create them.
    """

    all_layer_names = getattr(g, '_all_layer_names', None)
    if all_layer_names is None:
        g._overzoomer, g._all_layer_names = _parse_config()
        all_layer_names = g._all_layer_names
    return all_layer_names


@app.route("/mapzen/vector/<version>/<layers>/<int:z>/<int:x>/<int:y>.<fmt>",
           methods=['GET'])
def handle(version, layers, z, x, y, fmt):
    if layers == "all":
        layers = get_all_layer_names()
    else:
        layers = layers.split(",")

    fmt = lookup_format_by_extension(fmt)

    oz = get_overzoomer()

    response = oz.overzoom(version, layers, Coordinate(y, x, z), fmt)

    if response is None:
        abort(404)

    return response
