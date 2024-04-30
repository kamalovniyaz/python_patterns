"""
Абстрактная фабрика — это порождающий паттерн проектирования, который позволяет создавать семейства связанных объектов, не привязываясь к конкретным классам создаваемых объектов.

Пример:
Вы создаете интернет-магазин мебельного магазина. Например у вас есть большое кол-во мебели в разных стилях - кресло, диван, столик.
Также эта мебель представлена в разных стилях: Ар-деко, Викторианском и Модерне.

Вам нужен такой способ создавать объекты продуктов, чтобы они сочетались с другими продуктами того же семейства.
Кроме того, вы не хотите вносить изменения в существующий код при добавлении новых продуктов или семейcтв в программу.
Поставщики часто обновляют свои каталоги, и вы бы не хотели менять уже написанный код каждый раз при получении новых моделей мебели.

Решение:
Для начала паттерн Абстрактная фабрика предлагает выделить общие интерфейсы для отдельных продуктов, составляющих семейства.
Так, все вариации кресел получат общий интерфейс Кресло, все диваны реализуют интерфейс Диван и так далее.

Далее нужно создать общий интерфейс, который содержит методы создания всех продуктов семейства (создатьКресло, ...)
Эти операции должны возвращать абстрактные типы продуктов, представленные интерфейсами, которые мы выделили ранее — Кресла, Диваны и Столики.

Для каждой вариации семейства продуктов мы должны создать свою собственную фабрику, реализовав абстрактный интерфейс.
Фабрики создают продукты одной вариации. Например, ФабрикаМодерн будет возвращать только КреслаМодерн,ДиваныМодерн и СтоликиМодерн.

Клиентский код должен работать как с фабриками, так и с продуктами только через их общие интерфейсы.
Это позволит подавать в ваши классы любой тип фабрики и производить любые продукты, ничего не ломая.
"""
import platform
from abc import ABC, abstractmethod


class Button(ABC):
    def paint(self) -> None:
        pass


class WinButton(Button):
    def paint(self):
        print('Отрисовать кнопку в стиле windows')


class MacButton(Button):
    def paint(self):
        print('Отрисовать кнопку в стиле macOS')


class Checkbox(ABC):
    def paint(self):
        pass


class WinCheckbox(Checkbox):
    def paint(self):
        print('Отрисовать чекбокс в стиле windows')


class MacCheckbox(Checkbox):
    def paint(self):
        print('Отрисовать чекбокс в стиле macOS')


class GUIFactory(ABC):
    @abstractmethod
    def createButton(self) -> None:
        pass

    @abstractmethod
    def createCheckbox(self) -> None:
        pass


class WinFactory(GUIFactory):
    def createButton(self):
        return WinButton()

    def createCheckbox(self):
        return WinCheckbox()


class MacFactory(GUIFactory):
    def createButton(self):
        return MacButton()

    def createCheckbox(self):
        return MacCheckbox()


class Application:
    def __init__(self, factory):
        self.factory = factory
        self.button = None
        self.checkbox = None

    def createUI(self):
        self.button = self.factory.createButton()
        self.checkbox = self.factory.createCheckbox()

    def paint(self):
        self.button.paint()
        self.checkbox.paint()


class ApplicationConfigurator:
    def main(self):
        config_os = platform.system()

        match config_os:
            case 'Windows':
                self.factory = WinFactory()
            case 'Darwin':
                self.factory = MacFactory()
            case _:
                raise Exception("Error! Unknown operating system.")

        app = Application(self.factory)
        app.createUI()
        app.paint()


if __name__ == "__main__":
    configurator = ApplicationConfigurator()
    configurator.main()
