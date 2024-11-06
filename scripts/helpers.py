class Location:
    def __init__(self, location: list[int, int]):
        self.x, self.y = location
    

    def copy(self):
        return Location([self.x, self.y])


    def to_string(self) -> str:
        return f"{self.x};{self.y}"

    
    def from_string(location_string: str) -> "Location":
        return Location(location_string.split(';'))
