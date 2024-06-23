"""
Команда — это поведенческий паттерн проектирования, который превращает запросы в объекты, позволяя передавать их как аргументы
при вызове методов, ставить запросы в очередь, логировать их, а также поддерживать отмену операций.
Проблема:
Вы создали класс красивых Кнопок и хотите использовать его для всех кнопок приложения, начиная от панели управления, заканчивая простыми кнопками в диалогах.
Все эти кнопки, хоть и выглядят схоже, но делают разные вещи. Поэтому возникает вопрос: куда поместить код обработчиков кликов
по этим кнопкам? Самым простым решением было бы создать подклассы для каждой кнопки и переопределить в них метод действия под разные задачи.
Но скоро станет понятно, что мы так раздуваем код и получилось слишком много подклассов.
Также код становится зависимым от классов бизнес-логики, которая часто меняется.
"""