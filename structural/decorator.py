"""
Декоратор — это структурный паттерн проектирования, который позволяет динамически добавлять объектам новую функциональность,
оборачивая их в полезные «обёртки».
Основой библиотеки является класс Notifier с методом send, который принимает на вход строку-сообщение и высылает её всем
администраторам по электронной почте. Сторонняя программа должна создать и настроить этот объект, указав кому отправлять
оповещения, а затем использовать его каждый раз, когда что-то случается.
В какой-то момент стало понятно, что одних email-оповещений пользователям мало. А также пользователя захотели получать
сообщения сразу на несколько ресурсов.
Вы попытались реализовать все возможные комбинации подклассов оповещений. Но после того как вы добавили первый десяток классов,
стало ясно, что такой подход невероятно раздувает код программы.

Декоратор имеет альтернативное название — обёртка. Оно более точно описывает суть паттерна: вы помещаете целевой объект в
другой объект-обёртку, который запускает базовое поведение объекта, а затем добавляет к результату что-то своё.

Оба объекта имеют общий интерфейс, поэтому для пользователя нет никакой разницы, с каким объектом работать — чистым или обёрнутым.
Вы можете использовать несколько разных обёрток одновременно — результат будет иметь объединённое поведение всех обёрток сразу.

В примере с оповещениями мы оставим в базовом классе простую отправку по электронной почте, а расширенные способы отправки
сделаем декораторами.
"""


class DataSource:
    """
    Общий интерфейс компонентов
    """

    def __init__(self, data: str):
        self.data = data

    def write_date(self, data: str) -> None:
        pass

    def read_date(self) -> None:
        pass


class FileDataSource(DataSource):
    """
     Один из конкретных компонентов реализует базовую функциональность
    """

    def write_date(self, data: str) -> None:
        print('записать данные в файл')

    def read_date(self) -> None:
        print('прочитать данные из файла')


class DataSourceDecorator(DataSource):
    """
    Родитель всех декораторов содержит код обёртывания
    """
    wrapper: DataSource

    def __init__(self, source: DataSource):
        self.wrapper = source

    def write_date(self, data: str) -> None:
        self.wrapper.write_date(data)

    def read_date(self) -> None:
        return self.wrapper.read_date()


class EncryptedDataSource(DataSourceDecorator):
    """
    Конкретные декораторы добавляют что-то своё к базовому поведению обёрнутого компонента.
    """

    def write_date(self, data: str) -> None:
        print(f"1. Зашифровать поданные данные."
              f"2. Передать зашифрованные данные в метод writeData обёрнутого объекта (wrappee)")

    def read_date(self) -> None:
        print(f"1. Получить данные из метода readData обёрнутого объекта (wrappee)."
              f"2. Расшифровать их, если они зашифрованы."
              f"3. Вернуть результат.")


class CompressionDecorator(DataSourceDecorator):
    """
    Декорировать можно не только базовые компоненты, но и уже обёрнутые объекты.
    """

    def write_date(self, data: str) -> None:
        print(f"1. Запаковать поданные данные."
              f"2. Передать запакованные данные в метод writeData обёрнутого объекта (wrappee)")

    def read_date(self) -> None:
        print(f"1. Получить данные из метода readData обёрнутого объекта (wrappee)."
              f"2. Распаковать их, если они запакованы."
              f"3. Вернуть результат.")

if __name__ == '__main__':
    file_data_source = FileDataSource('example.txt')

    encrypted_data_source = EncryptedDataSource(file_data_source)

    compressed_and_encrypted_data_source = CompressionDecorator(encrypted_data_source)

    print("Используем FileDataSource:")
    file_data_source.write_date("Hello, World!")
    file_data_source.read_date()

    print("Используем EncryptedDataSource:")
    encrypted_data_source.write_date("Hello, World!")
    encrypted_data_source.read_date()

    print("Используем CompressionDecorator поверх EncryptedDataSource:")
    compressed_and_encrypted_data_source.write_date("Hello, World!")
    compressed_and_encrypted_data_source.read_date()
