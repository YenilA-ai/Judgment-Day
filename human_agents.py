
from collections import deque


class JohnConnor:
    def __init__(self, environment, start_position=(10, 2)):
        self.environment = environment
        self.position = start_position
        self.health = 100
        self.max_health = 100
        self.alive = True

        self.detection_range = 6
        self.detected_threat = None
        self.threat_distance = None

        self.state = "seeking_safety"
        self.last_position = None
        self.distance_travelled = 0

        if not self.environment.is_walkable(*self.position):
            raise ValueError("John's starting position is not walkable")

    def perceive(self, threat_position=None):
        self.detected_threat = None
        self.threat_distance = None

        if threat_position is None:
            return False

        threat_row, threat_col = threat_position

        if not self.environment.in_bounds(threat_row, threat_col):
            return False

        distance = (
            abs(self.position[0] - threat_row)
            + abs(self.position[1] - threat_col)
        )

        if distance <= self.detection_range:
            self.detected_threat = threat_position
            self.threat_distance = distance
            return True

        return False

    def find_safe_path(self):
        safe_positions = [
            (row, col)
            for row in range(self.environment.rows)
            for col in range(self.environment.columns)
            if self.environment.get_terrain(row, col) == "safe"
        ]

        queue = deque([(self.position, [])])
        visited = {self.position}

        while queue:
            current_position, path = queue.popleft()

            if current_position in safe_positions:
                return path

            for neighbour in self.environment.get_neighbours(
                *current_position
            ):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(
                        (neighbour, path + [neighbour])
                    )

        return []

    def choose_evasion_move(self):
        neighbours = self.environment.get_neighbours(*self.position)

        if not neighbours:
            return self.position

        threat_row, threat_col = self.detected_threat

        def safety_score(position):
            row, col = position

            distance_from_threat = (
                abs(row - threat_row) + abs(col - threat_col)
            )

            terrain = self.environment.get_terrain(row, col)
            hazard_penalty = 2 if terrain == "hazard" else 0

            safe_path = self.find_path_from(position)
            safe_distance = len(safe_path) if safe_path else 100

            previous_position_penalty = (
                1 if position == self.last_position else 0
            )

            return (
                distance_from_threat,
                -hazard_penalty,
                -safe_distance,
                -previous_position_penalty
            )

        return max(neighbours, key=safety_score)

    def find_path_from(self, start_position):
        safe_positions = {
            (row, col)
            for row in range(self.environment.rows)
            for col in range(self.environment.columns)
            if self.environment.get_terrain(row, col) == "safe"
        }

        queue = deque([(start_position, [])])
        visited = {start_position}

        while queue:
            current_position, path = queue.popleft()

            if current_position in safe_positions:
                return path

            for neighbour in self.environment.get_neighbours(
                *current_position
            ):
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(
                        (neighbour, path + [neighbour])
                    )

        return []

    def decide_action(self):
        if not self.alive:
            self.state = "eliminated"
            return self.position

        if self.detected_threat is not None:
            self.state = "evading"
            return self.choose_evasion_move()

        safe_path = self.find_safe_path()

        if safe_path:
            self.state = "seeking_safety"
            return safe_path[0]

        self.state = "searching_for_safety"
        return self.position

    def move(self, target_position):
        if not self.alive:
            return False

        if not self.environment.can_move(
            self.position,
            target_position
        ):
            return False

        self.last_position = self.position
        self.position = target_position
        self.distance_travelled += 1

        return True

    def update(self, threat_position=None):
        if not self.alive:
            self.state = "eliminated"
            return "eliminated"

        self.perceive(threat_position)

        target_position = self.decide_action()

        if target_position == self.position:
            if self.state == "evading":
                return "no_safe_escape"
            return "waiting"

        if self.move(target_position):
            if self.state == "evading":
                return "evading_threat"
            return "moving_to_safety"

        return "movement_blocked"

    def take_damage(self, amount):
        if amount <= 0 or not self.alive:
            return

        self.health = max(0, self.health - amount)

        if self.health == 0:
            self.alive = False
            self.state = "eliminated"
