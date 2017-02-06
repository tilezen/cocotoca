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
        x = 10442
        y = 25312
        store = FakeTileStore("""
{
  "water":{
    "type":"FeatureCollection",
    "features":[
      {
        "type":"Feature",
        "geometry":{
          "type":"Polygon",
          "coordinates":[
            [[-122.63488770,37.85316996],
             [-122.64038086,37.85316996],
             [-122.64038086,37.85750716],
             [-122.63488770,37.85750716],
             [-122.63488770,37.85316996]]]
        },
        "properties":{}
      }
    ]
  }
}
""")
        oz = Overzoomer(store, z, {})

        # check that the clipped geometry is returned, not the full one!
        tile = Coordinate(y * 2, x * 2, z + 1)
        data = oz.overzoom(None, ['water'], tile, json_format)
        geojson = json.loads(data)
        self.assertEqual('FeatureCollection', geojson.get('type'))
        self.assertEqual(1, len(geojson['features']))
        feature = geojson['features'][0]
        self.assertEqual('Feature', feature['type'])
        self.assertEqual({}, feature['properties'])
        self.assertEqual('Polygon', feature['geometry']['type'])
        rings = feature['geometry']['coordinates']
        self.assertEqual(1, len(rings))
        self.assertEqual(5, len(rings[0]))
        self.assertEqual([-122.63763428,37.85533859], rings[0][0])
        self.assertEqual([-122.64038086,37.85533859], rings[0][1])
        self.assertEqual([-122.64038086,37.85750716], rings[0][2])
        self.assertEqual([-122.63763428,37.85750716], rings[0][3])
        self.assertEqual([-122.63763428,37.85533859], rings[0][4])
