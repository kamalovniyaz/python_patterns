"""
Легковес — это структурный паттерн проектирования, который позволяет вместить бóльшее количество объектов в отведённую оперативную память.
Легковес экономит память, разделяя общее состояние объектов между собой, вместо хранения одинаковых данных в каждом объекте.

Проблема:
Вы написали игру с фишкой - реалистичная система частиц. Пули, снаряды, осколки от взрывов — всё это должно красиво летать и радовать взгляд.
На слабых ПК игра может тормозить, т.к частица - собственный объект, имеющих мн-во данных. Когда частиц много, новые объекты частиц
не помещаются в RAM.

Решение:
Если внимательно посмотреть на класс частиц, то можно заметить, что цвет и спрайт занимают больше всего памяти. Более того,
они хранятся в каждом объекте, хотя фактически их значения одинаковы для большинства частиц.

Цвет и спрайт — это данные, не изменяющиеся во времени. Остальные данные отличаются у всех частиц.
Неизменяемые данные объекта принято называть «внутренним состоянием». Все остальные данные — это «внешнее состояние».

Паттерн Легковес предлагает не хранить в классе внешнее состояние, а передавать его в те или иные методы через параметры.
Таким образом, одни и те же объекты можно будет повторно использовать в различных контекстах.
Но главное — понадобится гораздо меньше объектов, ведь теперь они будут отличаться только внутренним состоянием, а оно имеет не так много вариаций.
"""
import tkinter as tk


class Canvas:
    def __init__(self, width: int, height: int) -> None:
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()

    def draw_tree(self, x: int, y: int, color: str) -> None:
        # Рисуем простое дерево (квадрат) на холсте для примера
        self.canvas.create_rectangle(x, y, x + 10, y + 30, fill=color)
        self.canvas.create_rectangle(x - 5, y + 30, x + 15, y + 50, fill="brown")

    def mainloop(self) -> None:
        self.root.mainloop()


class TreeType:
    def __init__(self, name: str, color: str, texture: str):
        self.name = name
        self.color = color
        self.texture = texture

    def draw(self, canvas: Canvas, x: int, y: int) -> None:
        canvas.draw_tree(x, y, self.color)


class TreeFactory:
    tree_types = []

    @staticmethod
    def get_tree_type(name: str, color: str, texture: str) -> TreeType:
        for tree_type in TreeFactory.tree_types:
            if tree_type.name == name and tree_type.color == color and tree_type.texture == texture:
                return tree_type
        new_type = TreeType(name, color, texture)
        TreeFactory.tree_types.append(new_type)

        return new_type


class Tree:
    def __init__(self, x: int, y: int, tree_type: TreeType):
        self.x = x
        self.y = y
        self.tree_type = tree_type

    def draw(self, canvas: Canvas) -> None:
        if self.tree_type is not None:
            self.tree_type.draw(canvas, self.x, self.y)
        else:
            print(f"TreeType for tree at ({self.x}, {self.y}) is None")


class Forest:
    def __init__(self):
        self.trees = []

    def plant_tree(self, x: int, y: int, name: str, color: str, texture: str) -> None:
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, tree_type)
        self.trees.append(tree)

    def draw(self, canvas: Canvas) -> None:
        for tree in self.trees:
            tree.draw(canvas)


if __name__ == '__main__':
    forest = Forest()
    forest.plant_tree(20, 50, "Oak", "green", "rough")
    forest.plant_tree(80, 50, "Pine", "darkgreen", "smooth")
    forest.plant_tree(50, 50, "Birch", "lightgreen", "smooth")
    forest.plant_tree(50, 70, "Oak", "green", "rough")

    canvas = Canvas(100, 100)
    forest.draw(canvas)
    canvas.mainloop()
