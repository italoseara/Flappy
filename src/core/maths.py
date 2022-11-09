from __future__ import annotations
from typing import Tuple, Callable
from dataclasses import dataclass

@dataclass
class Vector2:
    x: float
    y: float

    @staticmethod
    def from_tuple(tup: Tuple[float, float]) -> Vector2:
        (x, y) = tup
        return Vector2(x, y)

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def map(self, func: Callable[[float], float]) -> Vector2:
        return Vector2(x=func(self.x), y=func(self.y))

    def map_with_other(self, rhs: Vector2, func: Callable[[float, float], float]) -> Vector2:
        return Vector2(
            x=func(self.x, rhs.x),
            y=func(self.y, rhs.y),
        )

@dataclass
class Rectangle:
    x: float
    y: float
    w: float
    h: float

    @staticmethod
    def from_tuple(tup: Tuple[float, float, float, float]) -> Rectangle:
        (x, y, w, h) = tup
        return Rectangle(x, y, w, h)

    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.x, self.y, self.w, self.h)

    def map(self, func: Callable[[float], float]) -> Rectangle:
        return Rectangle(
            x=func(self.x),
            y=func(self.y),
            w=func(self.w),
            h=func(self.h),
        )

    def map_with_other(self, rhs: Rectangle, func: Callable[[float, float], float]) -> Rectangle:
        return Rectangle(
            x=func(self.x, rhs.x),
            y=func(self.y, rhs.y),
            w=func(self.w, rhs.w),
            h=func(self.h, rhs.h),
        )
