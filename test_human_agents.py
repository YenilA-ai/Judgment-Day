
import unittest
from environment import GridEnvironment
from human_agents import JohnConnor


class TestJohnConnor(unittest.TestCase):

    def setUp(self):
        self.environment = GridEnvironment()
        self.john = JohnConnor(self.environment)

    def test_initial_position(self):
        self.assertEqual(self.john.position, (10, 2))

    def test_initial_health(self):
        self.assertEqual(self.john.health, 100)

    def test_initial_state(self):
        self.assertEqual(self.john.state, "seeking_safety")

    def test_starting_position_is_walkable(self):
        self.assertTrue(
            self.environment.is_walkable(*self.john.position)
        )

    def test_detect_nearby_threat(self):
        self.assertTrue(self.john.perceive((10, 4)))
        self.assertEqual(self.john.detected_threat, (10, 4))

    def test_ignore_distant_threat(self):
        self.assertFalse(self.john.perceive((19, 19)))
        self.assertIsNone(self.john.detected_threat)

    def test_move_towards_safety(self):
        original_position = self.john.position

        action = self.john.update()

        self.assertEqual(action, "moving_to_safety")
        self.assertNotEqual(self.john.position, original_position)

    def test_movement_uses_walkable_cells(self):
        self.john.update()

        self.assertTrue(
            self.environment.is_walkable(*self.john.position)
        )

    def test_threat_changes_johns_state(self):
        self.john.perceive((10, 4))
        self.john.decide_action()

        self.assertEqual(self.john.state, "evading")

    def test_evasion_increases_distance_from_threat(self):
        threat_position = (10, 4)

        initial_distance = (
            abs(self.john.position[0] - threat_position[0])
            + abs(self.john.position[1] - threat_position[1])
        )

        self.john.update(threat_position)

        new_distance = (
            abs(self.john.position[0] - threat_position[0])
            + abs(self.john.position[1] - threat_position[1])
        )

        self.assertGreater(new_distance, initial_distance)

    def test_distance_travelled(self):
        self.john.update()

        self.assertEqual(self.john.distance_travelled, 1)

    def test_damage_reduces_health(self):
        self.john.take_damage(20)

        self.assertEqual(self.john.health, 80)

    def test_health_cannot_go_below_zero(self):
        self.john.take_damage(150)

        self.assertEqual(self.john.health, 0)
        self.assertFalse(self.john.alive)

    def test_eliminated_agent_cannot_move(self):
        self.john.take_damage(100)

        result = self.john.move((10, 3))

        self.assertFalse(result)
        self.assertEqual(self.john.position, (10, 2))

    def test_zero_or_negative_damage_is_ignored(self):
        self.john.take_damage(0)
        self.john.take_damage(-10)

        self.assertEqual(self.john.health, 100)


if __name__ == "__main__":
    unittest.main()
