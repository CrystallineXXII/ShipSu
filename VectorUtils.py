import math


class Vector2:

  def __init__(self, x, y):
    self._x = x
    self._y = y

  @property
  def x(self):
    return self._x
  @property
  def y(self):
    return self._y
  @property
  def magnitude(self):
    return (self._x**2 + self._y**2)**0.5

  def normalized(self):
    return Vector2(self._x/self.magnitude,self._y/self.magnitude)
  @property
  def direction(self):
    if self._x == 0:
      return 0
    if self._y == 0:
      return 90
    try:
      val =  180 - math.degrees(math.atan(self._y / self._x))
    except ZeroDivisionError:
      return 90 if self._y > 0 else 270

 
    if self._x > 0 and self._y > 0: return val + 90
    if self._x < 0 and self._y > 0: return val + 270
    if self._x < 0 and self._y < 0: return val + 270
    if self._x > 0 and self._y < 0: return val + 90

  @classmethod
  def CreateFromComponents(cls, x, y):
    return cls(x, y)

  @classmethod
  def CreateFromDirection(cls, dir, mag):
    x = mag * math.sin(dir)
    y = mag * math.cos(dir)
    return cls(x, y)

  @classmethod
  def zero(cls):
    return cls(0, 0)

  @classmethod
  def infinity(cls):
    return cls(math.inf, math.inf)

  def __str__(self):
    return str((self._x, self._y))
  
  def intuple(self):
    return (self._x, self._y)

  def __add__(self, operand):
    x = self._x + operand.x
    y = self._y + operand.y
    return Vector2(x, y)

  def __sub__(self, operand):
    x = self._x - operand.x
    y = self._y - operand.y
    return Vector2(x, y)

  def __mul__(self, operand):
    x = self._x * operand
    y = self._y * operand
    return Vector2(x, y)

if __name__ == '__main__':
  v = Vector2(150,150)
  print(v.normalized())