class Priority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    LEVELS = {
        "Low": LOW,
        "Medium": MEDIUM,
        "High": HIGH,
    }

    def __init__(self, level):
        level = level.capitalize()
        if level not in self.LEVELS:
            raise ValueError("Invalid priority level")
        self.level = self.LEVELS[level]

    def __str__(self):
        return list(self.LEVELS.keys())[list(self.LEVELS.values()).index(self.level)]

    def __repr__(self):
        return f"Priority({self.__str__()})"

    def __eq__(self, other):
        if isinstance(other, Priority):
            return self.level == other.level
        return False

    def __lt__(self, other):
        if isinstance(other, Priority):
            return self.level < other.level
        return False

    def __le__(self, other):
        if isinstance(other, Priority):
            return self.level <= other.level
        return False

    def __gt__(self, other):
        if isinstance(other, Priority):
            return self.level > other.level
        return False

    def __ge__(self, other):
        if isinstance(other, Priority):
            return self.level >= other.level
        return False