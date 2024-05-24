"""
Компоновщик — это структурный паттерн проектирования, который позволяет сгруппировать множество объектов в древовидную структуру,
а затем работать с ней так, как будто это единичный объект.

Проблема:
Паттерн Компоновщик имеет смысл только тогда, когда основная модель вашей программы может быть структурирована в виде дерева.
Например, есть два объекта: Продукт и Коробка. Коробка может содержать несколько Продуктов и других Коробок поменьше.
Те, в свою очередь, тоже содержат либо Продукты, либо Коробки и так далее.
Теперь предположим, ваши Продукты и Коробки могут быть частью заказов. Каждый заказ может содержать как простые Продукты без упаковки,
так и составные Коробки. Ваша задача состоит в том, чтобы узнать цену всего заказа.

Решение:
Компоновщик предлагает рассматривать Продукт и Коробку через единый интерфейс с общим методом получения стоимости.
Продукт просто вернёт свою цену. Коробка спросит цену каждого предмета внутри себя и вернёт сумму результатов.
Если одним из внутренних предметов окажется коробка поменьше, она тоже будет перебирать своё содержимое, и так далее,
пока не будут посчитаны все составные части.
"""
from abc import ABC, abstractmethod
from typing import List


class Graphic(ABC):
    @abstractmethod
    def move(self, x: int, y: int) -> None:
        pass

    @abstractmethod
    def draw(self) -> None:
        pass


class Dot(Graphic):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def move(self, x: int, y: int) -> None:
        self.x += x
        self.y += y

    def draw(self):
        print('Нарисовать точку в координате X, Y')


class Circle(Dot):
    def __init__(self, x: int, y: int, radius: int) -> None:
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self) -> None:
        print('Нарисовать окружность в координате X, Y и с радиусом R')


class CompoundGraphic(Graphic):
    def __init__(self):
        self.children: List[Graphic] = []

    def add(self, child: Graphic) -> None:
        print('Добавить компонент в список дочерних')

    def remove(self, child: Graphic) -> None:
        print('Убрать компонент из списка дочерних')

    def move(self, x: int, y: int) -> None:
        for child in self.children:
            child.move(x, y)

    def draw(self) -> None:
        print(" 1. Для каждого дочернего компонента:"
              "- Отрисовать компонент."
              "- Определить координаты максимальной границы."
              "2. Нарисовать пунктирную границу вокруг всей области.")


class ImageEditor:
    def __init__(self):
        self.all = CompoundGraphic()

    def load(self) -> None:
        self.all = CompoundGraphic()
        self.all.add(Dot(1, 2))
        self.all.add(Circle(5, 3, 10))

    def group_selected(self, components: List[Graphic]) -> None:
        group = CompoundGraphic()
        for component in components:
            group.add(component)
            self.all.remove(component)
        self.all.add(group)
        self.all.draw()


if __name__ == '__main__':
    editor = ImageEditor()
    editor.load()
    components_to_group = [Dot(3, 4), Circle(6, 7, 15)]
    editor.group_selected(components_to_group)
