"""
Цепочка обязанностей — это поведенческий паттерн проектирования, который позволяет передавать запросы последовательно по
цепочке обработчиков. Каждый последующий обработчик решает, может ли он обработать запрос сам и стоит ли передавать запрос дальше по цепи.
Проблема:
Хотим выполнять разные проверки, например: только авторизованные пользователи могли создавать заказы или доступ к
подробностям заказа был у админов.
Мы понимаем что проверки нужно выполнять последовательно, так как иногда не имеет смысла делать следующую проверку.
За несколько месяцев добавилось еще множество проверок. Код становится более запутанным. Поддерживать такой код затратно и хлопотно.

Решение:
Цепочка обязанностей базируется на том, чтобы превратить отдельные поведения в объекты. В нашем случае каждая проверка
переедет в отдельный класс с единственным методом выполнения. Данные запроса, над которым происходит проверка, будут
передаваться в метод как аргументы.

А теперь по-настоящему важный этап. Паттерн предлагает связать объекты обработчиков в одну цепь. Каждый из них будет иметь
ссылку на следующий обработчик в цепи. Таким образом, при получении запроса обработчик сможет не только сам что-то с ним
сделать, но и передать обработку следующему объекту в цепочке.

Передавая запросы в первый обработчик мы должны быть уверены, что все объекты в цепи смогут его обработать. Длина цепочки не имеет значения.
Обработчик не обязательно передаст запрос дальше. Например: если у нас много обработчиков и мы понимаем, что с запросом
что-то не так, то нет смысла тратить ресурсы на дальнейшие проверки.

Но есть и другой подход, при котором обработчики прерывают цепь только когда они могут обработать запрос.
В этом случае запрос движется по цепи, пока не найдётся обработчик, который может его обработать.

Очень важно, чтобы все объекты цепочки имели общий интерфейс. Обычно каждому конкретному обработчику достаточно знать
только то, что следующий объект в цепи имеет метод выполнить. Благодаря этому связи между объектами цепочки будут более гибкими.
Кроме того, вы сможете формировать цепочки на лету из разнообразных объектов, не привязываясь к конкретным классам.
"""
from abc import ABC, abstractmethod
from typing import Optional, List


class ComponentWithContextualHelp(ABC):
    @abstractmethod
    def show_help(self) -> None:
        pass


# Базовый класс простых компонентов.
class Component(ComponentWithContextualHelp):
    def __init__(self, tooltip_text: Optional[str] = None):
        self.tooltip_next = tooltip_text
        self.container = None

    def show_help(self) -> None:
        """
        Базовое поведение компонента заключается в том, чтобы показать всплывающую подсказку, если для неё задан текст.
        В обратном случае — перенаправить запрос своему контейнеру, если тот существует.
        """
        if self.tooltip_next:
            print('Показать подсказку')
        else:
            self.container.show_help()


# Контейнеры могут включать в себя как простые компоненты, так
# и другие контейнеры. Здесь формируются связи цепочки. Класс
# контейнера унаследует метод show_help от своего родителя —
# базового компонента.
class Container(Component):
    def __init__(self, tooltip_text: Optional[str] = None):
        super().__init__(tooltip_text)
        self.children: List[Component] = []

    def add_child(self, child) -> None:
        self.children.append(child)
        child.container = self


# Большинство примитивных компонентов устроит базовое поведение
# показа помощи через подсказку, которое они унаследуют из
# класса Component.
class Button(Component):
    def __init__(self, x, y, width, height, text, tooltip_text: Optional[str] = None):
        super().__init__(tooltip_text)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


# Но сложные компоненты могут переопределять метод показа
# помощи по-своему. Но и в этом случае они всегда могут
# вернуться к базовой реализации, вызвав метод родителя
class Panel(Container):
    def __init__(self, x: int, y: int, width: int, height: int, tooltip_text: Optional[str] = None,
                 modal_help_text: Optional[str] = None):
        super().__init__(tooltip_text)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.modal_help_text = modal_help_text

    def show_help(self) -> None:
        if self.modal_help_text:
            print(f"Модальная подсказка: {self.modal_help_text}")
        else:
            super().show_help()


class Dialog(Container):
    def __init__(self, title, tooltip_text: Optional[str] = None, wiki_page_url: Optional[str] = None):
        super().__init__(tooltip_text)
        self.title = title
        self.wiki_page_url = wiki_page_url

    def show_help(self) -> None:
        if self.wiki_page_url:
            print(f'Страница в википедии: {self.wiki_page_url}')
        else:
            super().show_help()


class Application:
    def __init__(self):
        self.dialog = None

    def create_ui(self) -> None:
        self.dialog = Dialog("Отчеты", wiki_page_url="http://...")
        panel = Panel(0, 0, 400, 800, modal_help_text="Эта панель предназначена для...")
        ok = Button(250, 760, 50, 20, "ОК", tooltip_text="Это кнопка OK, которая...")
        cancel = Button(320, 760, 50, 20, "Отмена")
        panel.add_child(ok)
        panel.add_child(cancel)
        self.dialog.add_child(panel)

    def on_press_f1_key(self, component: Component) -> None:
        component.show_help()

    def get_component_at_mouse_coords(self) -> Component:
        return self.dialog.children[0].children[0]


if __name__ == '__main__':
    app = Application()
    app.create_ui()
    component = app.get_component_at_mouse_coords()
    app.on_press_f1_key(component)
