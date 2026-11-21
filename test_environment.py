
import unittest
from environment import GridEnvironment


class TestGridEnvironment(unittest.TestCase):

    def setUp(self):
        self.environment = GridEnvironment()

    def test_grid_dimensions(self):
        self.assertEqual(self.environment.rows, 20)
        self.assertEqual(self.environment.columns, 20)

    def test_position_inside_boundaries(self):
        self.assertTrue(self.environment.in_bounds(0, 0))
        self.assertTrue(self.environment.in_bounds(19, 19))

    def test_position_outside_boundaries(self):
        self.assertFalse(self.environment.in_bounds(-1, 0))
        self.assertFalse(self.environment.in_bounds(20, 5))
        self.assertFalse(self.environment.in_bounds(5, 20))

    def test_buildings_are_not_walkable(self):
        self.assertFalse(self.environment.is_walkable(2, 3))

    def test_restricted_areas_are_not_walkable(self):
        self.assertFalse(self.environment.is_walkable(7, 16))

    def test_ground_is_walkable(self):
        self.assertTrue(self.environment.is_walkable(0, 0))

    def test_roads_are_walkable(self):
        self.assertTrue(self.environment.is_walkable(9, 0))

    def test_safe_zones_are_walkable(self):
        self.assertTrue(self.environment.is_walkable(1, 17))

    def test_hazards_are_walkable(self):
        self.assertTrue(self.environment.is_walkable(15, 7))

    def test_invalid_positions_are_not_walkable(self):
        self.assertFalse(self.environment.is_walkable(-1, 0))
        self.assertFalse(self.environment.is_walkable(20, 20))

    def test_valid_movement(self):
        self.assertTrue(
            self.environment.can_move((0, 0), (0, 1))
        )

    def test_movement_into_building(self):
        self.assertFalse(
            self.environment.can_move((2, 2), (2, 3))
        )

    def test_movement_into_restricted_area(self):
        self.assertFalse(
            self.environment.can_move((7, 15), (7, 16))
        )

    def test_movement_outside_boundary(self):
        self.assertFalse(
            self.environment.can_move((0, 0), (-1, 0))
        )

    def test_diagonal_movement(self):
        self.assertFalse(
            self.environment.can_move((0, 0), (1, 1))
        )

    def test_movement_over_multiple_cells(self):
        self.assertFalse(
            self.environment.can_move((0, 0), (0, 2))
        )

    def test_get_neighbours(self):
        neighbours = self.environment.get_neighbours(0, 0)

        self.assertEqual(neighbours, [(1, 0), (0, 1)])


if __name__ == "__main__":
    unittest.main()
