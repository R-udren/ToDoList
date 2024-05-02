class Priority:
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    LEVELS = {
        "Low": LOW,
        "Medium": MEDIUM,
        "High": HIGH,
    }

    def __init__(self, level: str | int):
        if isinstance(level, str):
            if level.isdigit() and int(level) in self.LEVELS.values():
                self.level = int(level)
            elif level.capitalize() in self.LEVELS:
                self.level = self.LEVELS[level.capitalize()]
            else:
                raise ValueError("Invalid priority level")
        elif isinstance(level, int) and level in self.LEVELS.values():
            self.level = level
        else:
            raise ValueError("Priority level must be a string, an integer, or an instance of Priority")

    def level(self):
        return self.level

    def __str__(self):
        return list(self.LEVELS.keys())[list(self.LEVELS.values()).index(self.level)]

    def __int__(self):
        return self.level

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
