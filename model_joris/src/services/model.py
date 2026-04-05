import pandas as pd
from ..models.enums.actions import Actions
import random

def get_action() -> Actions:
    tmp = list(Actions)
    return tmp[random.randint(0, len(tmp) - 1)]