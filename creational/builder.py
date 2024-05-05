"""
Строитель — это порождающий паттерн проектирования, который позволяет создавать сложные объекты пошагово.
Строитель даёт возможность использовать один и тот же код строительства для получения разных представлений объектов.

Например:
Cоздать объект Дом.
Чтобы построить стандартный дом, нужно поставить 4 стены, установить двери, вставить пару окон и положить крышу.
Но что, если вы хотите дом побольше да посветлее, имеющий сад, бассейн и прочее добро?

Решение:
Чтобы не плодить подклассы, вы можете подойти к решению с другой стороны.
Вы можете создать гигантский конструктор Дома, принимающий уйму параметров для контроля над создаваемым продуктом.
Действительно, это избавит вас от подклассов, но приведёт к другой проблеме - большая часть этих параметров будет простаивать.

Паттерн Строитель предлагает вынести конструирование объекта за пределы его собственного класса, поручив это дело отдельным объектам, которые следует называть строителями.
Паттерн предлагает разбить процесс конструирования объекта на отдельные шаги (например, построитьСтены, вставитьДвери и другие).
Чтобы создать объект, вам нужно поочерёдно вызывать методы строителя.
Причём не нужно запускать все шаги, а только те, что нужны для производства объекта определённой конфигурации.
"""
from abc import ABC, abstractmethod


class Car:
    pass


class Manual:
    pass


class Builder(ABC):
    @abstractmethod
    def set_tires(self, tires_model: str) -> None:
        pass

    @abstractmethod
    def set_engine(self, engine_name: str) -> None:
        pass

    @abstractmethod
    def set_seats(self, seats_count: int) -> None:
        pass

    @abstractmethod
    def set_car_radio(self, set_radio) -> bool:
        pass


class CarBuilder(Builder):
    def __init__(self):
        self.car = Car()

    def set_tires(self, tires_model: str) -> None:
        print(f'Установить колеса {tires_model}')

    def set_engine(self, engine_name: str) -> None:
        print(f'Установить двигатель {engine_name}')

    def set_seats(self, seats_count: int) -> None:
        print(f'Установить {seats_count} сидения')

    def set_car_radio(self, set_radio: bool) -> None:
        if set_radio:
            print("Установить радио в машину")
        else:
            print("Не устанавливать радио в машину")

    def get_result(self) -> Car:
        return self.car


class CarManualBuilder(Builder):
    def __init__(self):
        self.manual = Manual()

    def set_tires(self, tires_model: str) -> None:
        print(f'Добавить в руководство информацию о колесах {tires_model}')

    def set_engine(self, engine_model: str) -> None:
        print(f'Добавить в руководство информацию о двигателе {engine_model}')

    def set_seats(self, seats_model: int) -> None:
        print(f'Добавить в руководство информацию о {seats_model} сидениях ')

    def set_car_radio(self, set_radio: bool) -> None:
        if set_radio:
            print("Добавить в руководство информацию о радио")
        else:
            print("Не добавлять в руководство информацию о радио")

    def get_result(self) -> Manual:
        return self.manual


class Director:
    def create_sport_car(self, builder: Builder):
        builder.set_tires('MICHELIN Pilot Sport 5 245/40/R18 97Y')
        builder.set_engine('2JZ-GE')
        builder.set_seats(2)
        builder.set_car_radio(False)

    def create_family_car(self, builder: Builder):
        builder.set_tires('Kumho Ecsta HS52 185/65/R15 88H')
        builder.set_engine('G4LC')
        builder.set_seats(4)
        builder.set_car_radio(True)


class Application:
    @staticmethod
    def make_car():
        director = Director()

        print('__________Выпустить семейную машину__________')
        builder = CarBuilder()
        director.create_family_car(builder)
        builder.get_result()

        builder = CarManualBuilder()
        director.create_family_car(builder)
        builder.get_result()

        print('__________Выпустить спортивную машину__________')
        builder = CarBuilder()
        director.create_sport_car(builder)
        builder.get_result()

        builder = CarManualBuilder()
        director.create_sport_car(builder)
        builder.get_result()


if __name__ == '__main__':
    builder = Application()
    builder.make_car()
