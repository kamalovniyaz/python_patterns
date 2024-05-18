"""
Адаптер — это структурный паттерн проектирования, который позволяет объектам с несовместимыми интерфейсами работать вместе.
Представьте, что вы делаете приложение для торговли на бирже. Ваше приложение скачивает биржевые котировки из нескольких источников в XML,
а затем рисует красивые графики.
В какой-то момент вы решили улучшить приложение и использовать стороннюю библиотеку, но библиотека поддерживает только формат JSON.
Вы можете создать адаптер. Это объект-переводчик, который трансформирует интерфейс или данные одного объекта в такой вид, чтобы он стал понятен другому объекту.
"""
import math


class RoundPeg:
    def __init__(self, radius: int) -> None:
        self.radius = radius

    def get_radius(self) -> int:
        """Вернуть радиус круглого колышка"""
        return int(self.radius)


class RoundHole:
    def __init__(self, radius: int) -> None:
        self.radius = radius

    def get_radius(self) -> int:
        """Вернуть радиус отверстия"""
        return int(self.radius)

    def fits(self, peg: RoundPeg) -> bool:
        return self.get_radius() >= peg.get_radius()


class SquarePeg:
    def __init__(self, width: int) -> None:
        self.width = width

    def get_width(self) -> int:
        """Вернуть ширину квадратного колышка"""
        return int(self.width)


class SquarePegAdapter(RoundPeg):
    """Адаптер позволяет использовать квадратные колышки и круглые отверстия вместе"""

    def __init__(self, peg: SquarePeg) -> None:
        self.peg = peg

    def get_radius(self) -> int:
        """Вычислить половину диагонали квадратного колышка по теореме Пифагора"""
        return int(self.peg.get_width() * math.sqrt((2) / 2))


if __name__ == '__main__':
    hole = RoundHole(5)
    rpeg = RoundPeg(5)
    print(hole.fits(rpeg))

    small_sqpeg = SquarePeg(5)
    large_sqpeg = SquarePeg(10)

    small_sqpeg_adapter = SquarePegAdapter(small_sqpeg)
    large_sqpeg_adapter = SquarePegAdapter(large_sqpeg)
    print(hole.fits(small_sqpeg_adapter))
    print(hole.fits(large_sqpeg_adapter))
