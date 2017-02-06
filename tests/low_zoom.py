import unittest


class TestLowZoom(unittest.TestCase):

    def test_low_zoom(self):
        from cocotoca.cocotoca import Overzoomer
        from ModestMaps.Core import Coordinate
        max_z = 10
        oz = Overzoomer(None, max_z, None)
        coord = Coordinate(0, 0, max_z)
        self.assertIsNone(oz.overzoom(None, None, coord, None))

    def test_lower_zoom(self):
        from cocotoca.cocotoca import Overzoomer
        from ModestMaps.Core import Coordinate
        max_z = 10
        oz = Overzoomer(None, max_z, None)
        coord = Coordinate(0, 0, 0)
        self.assertIsNone(oz.overzoom(None, None, coord, None))
