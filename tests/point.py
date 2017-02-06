import unittest
from ModestMaps.Core import Coordinate
from tilequeue.format import json_format
import ujson as json


class TestPoint(unittest.TestCase):

    def test_sub_tile(self):
        from cocotoca.cocotoca import Overzoomer

        class FakeTileStore(object):

            def __init__(self, data):
                self.data = data

            def read_tile(self, tile, fmt, layers):
                return self.data

        z = 16
        x = 18876
        y = 24801
        store = FakeTileStore("""
{
  "places":{
    "type":"FeatureCollection",
    "features":[
      {
        "type":"Feature",
        "geometry":{
          "type":"Point",
          "coordinates":[-76.30567,40.03813]
        },
        "properties":{
          "name":"Lancaster"
        }
      }
    ]
  }
}
""")
        oz = Overzoomer(store, z, {})

        # test an empty subtile - this is checking that the subtile clips away
        # data which isn't in the subtile.
        tile = Coordinate(y * 2 + 1, x * 2 + 1, z + 1)
        data = oz.overzoom(None, ['places'], tile, json_format)
        self.assertEqual('{"type":"FeatureCollection","features":[]}', data)

        # test the one which should contain the point
        tile = Coordinate(y * 2, x * 2 + 1, z + 1)
        data = oz.overzoom(None, ['places'], tile, json_format)
        expect = dict(
            type='FeatureCollection',
            features=[
                dict(
                    type='Feature',
                    geometry=dict(
                        coordinates=[-76.30567, 40.03813],
                        type='Point'
                    ),
                    properties=dict(
                        name='Lancaster'
                    )
                )
            ])
        self.assertEqual(expect, json.loads(data))
