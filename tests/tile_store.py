import unittest
from tilequeue.format import json_format


class TestTileStore(unittest.TestCase):

    # check that the parent of the given tile at max_z maximum zoom is the
    # given parent. note that this tests the calculation, not the lookup -
    # the response from read_tile() is always None.
    def _check_tile_parent(self, max_z, tile, parent):
        from cocotoca.cocotoca import Overzoomer

        class FakeTileStore(object):

            def __init__(self, test, expect):
                self.test = test
                self.expect = expect

            def read_tile(self, tile, fmt, layers):
                self.test.assertEqual(json_format, fmt)
                self.test.assertEqual('all', layers)
                self.test.assertEqual(self.expect, tile)
                return None

        oz = Overzoomer(FakeTileStore(self, parent), max_z, None)
        self.assertIsNone(oz.overzoom(None, None, tile, None))

    def test_tile_store(self):
        from ModestMaps.Core import Coordinate as C

        self._check_tile_parent(0, C(0, 0, 1), C(0, 0, 0))
        self._check_tile_parent(10, C(0, 0, 11), C(0, 0, 10))
        self._check_tile_parent(11, C(0, 0, 12), C(0, 0, 11))
        self._check_tile_parent(12, C(0, 0, 13), C(0, 0, 12))

        self._check_tile_parent(10, C(128, 127, 11), C(64, 63, 10))
        self._check_tile_parent(9, C(128, 127, 11), C(32, 31, 9))
        self._check_tile_parent(8, C(128, 127, 11), C(16, 15, 8))
        self._check_tile_parent(7, C(128, 127, 11), C(8, 7, 7))
        self._check_tile_parent(0, C(128, 127, 11), C(0, 0, 0))
