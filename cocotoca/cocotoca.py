from cStringIO import StringIO
from tilequeue.format import json_format
from tilequeue.tile import calc_meters_per_pixel_dim
from tilequeue.tile import coord_to_mercator_bounds
from tilequeue.tile import reproject_lnglat_to_mercator
from tilequeue.transform import mercator_point_to_lnglat
from tilequeue.transform import transform_feature_layers_shape
import shapely.geometry
import shapely.ops
import ujson as json


class Overzoomer(object):

    def __init__(self, tile_store, max_z, buffer_cfg):
        self.tile_store = tile_store
        self.max_z = max_z
        self.buffer_cfg = buffer_cfg

    def overzoom(self, version, layers, coord, fmt):
        """
        Create a higher zoom tile by taking a lower zoom tile which contains
        it and cutting out the section which corresponds to the requested tile.
        This is quicker than querying the database to create tiles which are
        beyond the maximum level of detail.
        """

        # as an overzooming server, don't handle anything which is at or below
        # the maximum zoom that's already handled by other datasets. that
        # request should not have been sent here anyway.
        if coord.zoom <= self.max_z:
            return None

        # translate the tile coordinates up to the max zoom. it's this
        # "parent" tile that we will read and cut the requested tile's data
        # from.
        parent = coord.zoomTo(self.max_z).container()

        # fetch that tile's data from upstream stores. fetch the all JSON
        # tile as that's the "canonical" tile with the highest level of detail.
        tile_data = self.tile_store.read_tile(parent, json_format, 'all')

        # if there's no tile, then we can't do any overzooming - will have to
        # fall back to the upstream tileserver.
        if tile_data is None:
            return None

        # reformat the tile data, dropping any unwanted layers
        tile_data = self._reformat_selected_layers(
            tile_data, coord, fmt, layers)

        return tile_data

    def _reformat_selected_layers(
            self, json_tile_data, coord, format, layers):
        """
        Reformats the selected (subset of) layers from a JSON tile containing
        all layers. We store "tiles of record" containing all layers as JSON,
        and this function does most of the work of reading that, pruning the
        layers which aren't needed and reformatting it to the desired output
        format.
        """

        feature_layers = self._decode_json_tile_for_layers(
            json_tile_data, layers)
        bounds_merc = coord_to_mercator_bounds(coord)
        bounds_lnglat = (
            mercator_point_to_lnglat(bounds_merc[0], bounds_merc[1]) +
            mercator_point_to_lnglat(bounds_merc[2], bounds_merc[3]))

        meters_per_pixel_dim = calc_meters_per_pixel_dim(coord.zoom)

        scale = 4096
        feature_layers = transform_feature_layers_shape(
            feature_layers, format, scale, bounds_merc,
            coord, meters_per_pixel_dim, self.buffer_cfg)

        tile_data_file = StringIO()
        format.format_tile(tile_data_file, feature_layers, coord,
                           bounds_merc, bounds_lnglat)
        tile_data = tile_data_file.getvalue()
        return tile_data

    def _decode_json_tile_for_layers(self, tile_data, layers):
        layer_names_to_keep = set(layers)
        feature_layers = []
        json_data = json.loads(tile_data)
        for layer_name, json_layer_data in json_data.items():
            if layer_name not in layer_names_to_keep:
                continue
            features = []
            json_features = json_layer_data['features']
            for json_feature in json_features:
                json_geometry = json_feature['geometry']
                shape_lnglat = shapely.geometry.shape(json_geometry)
                shape_mercator = shapely.ops.transform(
                    reproject_lnglat_to_mercator, shape_lnglat)
                properties = json_feature['properties']
                # Ensure that we have strings for all key values and not
                # unicode values. Some of the encoders except to be
                # working with strings directly
                properties = ensure_utf8_properties(properties)
                fid = None
                feature = shape_mercator, properties, fid
                features.append(feature)

            feature_layer = dict(
                name=layer_name,
                features=features,
                layer_datum=dict(is_clipped=True),
            )
            feature_layers.append(feature_layer)
        return feature_layers


def ensure_utf8_properties(props):
    new_props = {}
    for k, v in props.items():
        if isinstance(k, unicode):
            k = k.encode('utf-8')
        if isinstance(v, unicode):
            v = v.encode('utf-8')
        new_props[k] = v
    return new_props
