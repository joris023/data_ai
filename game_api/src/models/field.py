class Field():
    def __init__(
        self, 
        rings:int,
        features:int
    ) -> None:
        self.rings = rings
        self.features = features

    def to_dict(self):
        return {
            "rings": self.rings,
            "features": self.features
        }