import datetime as dt
from typing import cast, Any
import pytest

def yolo(x: int) -> int:
    return 43


p = yolo(42)



dt.datetime.now()

def add(a: int, b: int):  # powinno zwrócic warning
    return None if a > 42 else 42


x: float = cast(float, add(1, 2))

result = x + 42


def fields(s):
     return s.split(',')

def first_field(x: str) -> str:
    # Error: Returning Any from function declared to return "str"  [no-any-return]
    return fields(x)[0]
