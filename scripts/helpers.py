class Location:
    def __init__(self, location: tuple[int, int]):
        self.x, self.y = location

    def copy(self):
        return Location((self.x, self.y))

    def to_string(self) -> str:
        return f"{self.x};{self.y}"

    @staticmethod
    def from_string(location_string: str) -> "Location":
        x, y = location_string.split(';')
        return Location((int(x), int(y)))
