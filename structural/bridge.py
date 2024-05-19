"""
Мост — это структурный паттерн проектирования, который разделяет один или несколько классов на две отдельные иерархии — абстракцию и реализацию,
позволяя изменять их независимо друг от друга.
Проблема:
У вас есть класс геометрических Фигур, который имеет подклассы Круг и Квадрат. Вы хотите расширить иерархию фигур по цвету,
то есть иметь Красные и Синие фигуры. Но чтобы всё это объединить, вам придётся создать 4 комбинации подклассов, вроде СиниеКруги и КрасныеКвадраты.
При добавлении новых видов фигур и цветов количество комбинаций будет расти в геометрической прогрессии.
Решение:
Паттерн Мост предлагает заменить наследование агрегацией или композицией. Для этого нужно выделить одну из таких «плоскостей»
в отдельную иерархию и ссылаться на объект этой иерархии, вместо хранения его состояния и поведения внутри одного класса.
Таким образом, мы можем сделать Цвет отдельным классом с подклассами Красный и Синий. Класс Фигур получит ссылку на объект
Цвета и сможет делегировать ему работу, если потребуется. Такая связь и станет мостом между Фигурами и Цветом.
При добавлении новых классов цветов не потребуется трогать классы фигур и наоборот.
"""
from abc import ABC, abstractmethod


# Можно расширять класс принтеров, не изменяя при этом класс компьютеров
# Все уст-ва имеют общий интерфейс. Поэтому с ними может работать любой принтер.
class Printer(ABC):
    @abstractmethod
    def print_file(self) -> None:
        pass


class Computer(ABC):
    """
    Абстрактный класс для компьютера.
    Содержит ссылку на объект принтера и методы для работы с ним.

    Класс компьютеров имеет ссылку на принтер, которым управляет.
    Методы этого класса делегируют работу методам связанного устройства.
    """

    def __init__(self, printer: Printer) -> None:
        self.printer = printer

    @abstractmethod
    def print(self) -> None:
        pass

    @abstractmethod
    def set_printer(self, printer: Printer) -> None:
        pass


class EpsonPrinter(Printer):
    """Конкретная реализация принтера Epson"""

    def print_file(self) -> None:
        print("Печать с помощью принтера Epson")


class HPPrinter(Printer):
    """Конкретная реализация принтера HP"""

    def print_file(self) -> None:
        print("Печать с помощью принтера HP")


class Mac(Computer):
    """Конкретная реализация компьютера на MAC OS"""

    def print(self) -> None:
        print("Печать для Mac")
        self.printer.print_file()

    def set_printer(self, printer: Printer) -> None:
        self.printer = printer


class Windows(Computer):
    """Конкретная реализация компьютера на Windows"""

    def print(self) -> None:
        print("Печать для Windows")
        self.printer.print_file()

    def set_printer(self, printer: Printer) -> None:
        self.printer = printer


if __name__ == '__main__':
    hp_printer = HPPrinter()
    epson_printer = EpsonPrinter()

    mac_computer = Mac(epson_printer)
    mac_computer.print()

    mac_computer.set_printer(hp_printer)
    mac_computer.print()

    windows_computer = Windows(hp_printer)
    windows_computer.print()

    windows_computer.set_printer(epson_printer)
    windows_computer.print()
