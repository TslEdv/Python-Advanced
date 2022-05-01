import unittest
from triangle_package_edvess import triangle


class TestTriangle(unittest.TestCase):

    def test_int(self):
        self.assertEqual(triangle.triangle_area(3, 4), 6, "Area should be 6")

    def test_float(self):
        self.assertEqual(triangle.triangle_area(3, 4.5), 6.75, "Area should be 6.75")

    def test_string(self):
        with self.assertRaises(TypeError):
            triangle.triangle_area("3", 4.5)


if __name__ == '__main__':
    unittest.main()
