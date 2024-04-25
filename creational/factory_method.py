"""
Фабричный метод — это порождающий паттерн проектирования, который определяет общий интерфейс для создания объектов в суперклассе,
позволяя подклассам изменять тип создаваемых объектов.

Пример:
Вы создаете программу управления грузоперевозками и рассчитываете, что грузы будут перевозить автомобили, поэтому ваш код работает с объектами класса Грузовик.
Со временем вы расширяетесь и решаете перевозить грузы на морских судах. Вам понадобится перелопатить всю программу.

Паттерн Фабричный метод предлагает создавать объекты не напрямую, используя оператор new, а через вызов особого фабричного метода.
Не пугайтесь, объекты всё равно будут создаваться при помощи new, но делать это будет фабричный метод.
"""
from abc import abstractmethod, ABC


# Абстрактный класс логгера
class Logger(ABC):
    @abstractmethod
    def log(self, text: str):
        pass


# Класс для логирования в консоль
class FileLogger(Logger):
    def log(self, text: str) -> None:
        with open('log.txt', 'w') as f:
            f.write(text)


# Класс для логирования в терминал
class TerminalLoger(Logger):
    def log(self, text: str) -> None:
        print(text)


# Абстрактная фабрика для создания логгеров
class LoggerFactory(ABC):
    @abstractmethod
    def create_loggeer(self):
        pass


# Фабрика для создания логгеров для записи в файл
class FileLoggerFactory(LoggerFactory):
    def create_loggeer(self):
        return FileLogger()


# Фабрика для создания логгеров для записи в терминал
class TerminalLoggerFactory(LoggerFactory):
    def create_loggeer(self):
        return TerminalLoger()


if __name__ == '__main__':
    file_logger_factory = FileLoggerFactory()
    file_logger = file_logger_factory.create_loggeer()
    file_logger.log('Лог записываемый в файл')

    terminal_logger_factory = TerminalLoggerFactory()
    terminal_logger = terminal_logger_factory.create_loggeer()
    terminal_logger.log('Лог записываемый в терминал')
