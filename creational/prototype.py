"""
Прототип — это порождающий паттерн проектирования, который позволяет копировать объекты, не вдаваясь в подробности их реализации.
Паттерн Прототип поручает создание копий самим копируемым объектам. Он вводит общий интерфейс для всех объектов, поддерживающих клонирование.
Это позволяет копировать объекты, не привязываясь к их конкретным классам. Обычно такой интерфейс имеет всего один метод clone.
Реализация этого метода в разных классах очень схожа. Метод создаёт новый объект текущего класса и копирует в него значения всех полей собственного объекта.
Так получится скопировать даже приватные поля, так как большинство языков программирования разрешает доступ к приватным полям любого объекта текущего класса.
"""
from abc import ABC, abstractmethod


class Shape(ABC):
    x: int
    y: int
    color: str

    def __init__(self, source=None) -> None:
        if source:
            self.x = source.x
            self.y = source.y
            self.color = source.color
        else:
            self.x = 0
            self.y = 0
            self.color = ''

    @abstractmethod
    def clone(self) -> 'Shape':
        ...


class Rectangle(Shape):
    width: int
    height: int

    def __init__(self, source=None) -> None:
        super().__init__(source)
        if source:
            self.width = source.width
            self.height = source.height
        else:
            self.width = 0
            self.height = 0

    def clone(self) -> 'Rectangle':
        return Rectangle(self)


class Circle(Shape):
    radius: int

    def __init__(self, source=None) -> None:
        super().__init__(source)
        if source:
            self.radius = source.radius
        else:
            self.radius = 0

    def clone(self) -> 'Circle':
        return Circle(self)


def business_logic(shapes: list[Shape]) -> None:
    shapes_copy: list[Shape] = []
    for s in shapes:
        shapes_copy.append(s.clone())


if __name__ == '__main__':
    shapes = []
    circle: Circle = Circle()
    circle.x = 10
    circle.y = 10
    circle.radius = 20
    shapes.append(circle)

    another_circle: Circle = circle.clone()
    shapes.append(another_circle)

    another_circle.x = 20
    another_circle.y = 20
    another_circle.radius = 40
    shapes.append(another_circle)

    rectangle = Rectangle()
    rectangle.width = 10
    rectangle.height = 20
    shapes.append(rectangle)

    business_logic(shapes)
