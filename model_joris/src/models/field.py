
class Field():
    def __init__(
        self, 
        rings:int,
        features:int
    ) -> None:
        self.rings = rings
        self.features = features

    @staticmethod
    def from_dict(data):
        return Field(data["rings"], data["features"])