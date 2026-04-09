from src.scrum_game.models.field import Field
from src.scrum_game.models.position import Position

default_board = {
    Position(product=1, sprint=1): Field(rings=4, features=3),
    Position(product=1, sprint=2): Field(rings=2, features=3),
    Position(product=1, sprint=3): Field(rings=1, features=2),
    Position(product=1, sprint=4): Field(rings=1, features=1),
    Position(product=2, sprint=1): Field(rings=5, features=2),
    Position(product=2, sprint=2): Field(rings=3, features=2),
    Position(product=2, sprint=3): Field(rings=2, features=1),
    Position(product=2, sprint=4): Field(rings=1, features=1),
    Position(product=3, sprint=1): Field(rings=6, features=1),
    Position(product=3, sprint=2): Field(rings=4, features=1),
    Position(product=3, sprint=3): Field(rings=3, features=1),
    Position(product=3, sprint=4): Field(rings=2, features=1),
    Position(product=4, sprint=1): Field(rings=5, features=2),
    Position(product=4, sprint=2): Field(rings=3, features=2),
    Position(product=4, sprint=3): Field(rings=2, features=2),
    Position(product=4, sprint=4): Field(rings=1, features=1),
    Position(product=5, sprint=1): Field(rings=4, features=3),
    Position(product=5, sprint=2): Field(rings=3, features=2),
    Position(product=5, sprint=3): Field(rings=2, features=2),
    Position(product=5, sprint=4): Field(rings=1, features=1),
}