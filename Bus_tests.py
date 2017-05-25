import unittest
from Bus import Bus

class TestBusObject(unittest.TestCase):

    def setUp(self):
        self.coord1 = (32.7767, -96.7970)
        self.coord2 = (40.7128, -74.0059)
        self.bus_obj = Bus({'lat': self.coord1[0], 'lon': self.coord1[1]}, 0)

    def test_get_bearing(self):
        bearing = round(self.bus_obj.get_bearing(self.coord1, self.coord2), 2)
        self.assertTrue(bearing == 59.91)

    def test_get_distance(self):
        distance = round(self.bus_obj.get_distance(self.coord1, self.coord2), 2)
        self.assertTrue(distance == 1372.11)

    def test_get_speed(self):
        self.bus_obj.update({'lat': self.coord2[0], 'lon': self.coord2[1]}, 70000)

        speed = round(self.bus_obj.get_speed(), 1)
        self.assertTrue(speed == 70.6)

if __name__ == '__main__':
    unittest.main()