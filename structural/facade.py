"""
Фасад — это структурный паттерн проектирования, который предоставляет простой интерфейс к сложной системе классов,
библиотеке или фреймворку.
Фасад полезен, если вы используете какую-то сложную библиотеку со множеством подвижных частей, но вам нужна только часть её возможностей.
К примеру, программа, заливающая видео котиков в социальные сети, может использовать профессиональную библиотеку сжатия видео.
Но все, что нужно клиентскому коду этой программы — простой метод encode(filename, format). Создав класс с таким методом,
вы реализуете свой первый фасад.
Аналогия из жизни: Когда вы звоните в магазин и делаете заказ по телефону, сотрудник службы поддержки является вашим
фасадом ко всем службам и отделам магазина. Он предоставляет вам упрощённый интерфейс к системе создания заказа, платёжной
системе и отделу доставки.
"""

"""Классы сложного стороннего фреймворка конвертации видео. Мы не контролируем этот код, поэтому не можем его упростить"""


class VideoFile:
    def __init__(self, filename):
        self.filename = filename


class OggCompressionCodec:
    def __init__(self):
        self.codec_type = 'ogg'


class MPEG4CompressionCodec:
    def __init__(self):
        self.codec_type = 'mp4'


class CodecFactory:
    @staticmethod
    def extract(file):
        if file.filename.endswith('.mp4'):
            return 'mp4'
        else:
            return 'ogg'


class BitrateReader:
    @staticmethod
    def read(filename, source_code):
        return f"buffer from {filename} with codec {source_code}"

    @staticmethod
    def convert(buffer, destination_codec):
        return f"converted {buffer} to {destination_codec.codec_type}"


class AudioMixer:
    @staticmethod
    def fix(result):
        return f"fixed audio in {result}"


class File:
    def __init__(self, data):
        self.data = data

    def save(self):
        print(f"Saving file with data: {self.data}")


"""Вместо этого мы создаём Фасад — простой интерфейс для работы со сложным фреймворком. Фасад не имеет всей функциональности 
фреймворка, но зато скрывает его сложность от клиентов."""


class VideoConvertor:
    def convert(self, filename, file_format):
        file = VideoFile(filename)
        source_code = CodecFactory.extract(file)

        if file == 'mp4':
            destination_codec = MPEG4CompressionCodec()
        else:
            destination_codec = OggCompressionCodec()

        buffer = BitrateReader.read(filename, source_code)
        result = BitrateReader.convert(buffer, destination_codec)
        result = AudioMixer.fix(result)
        return File(result)


if __name__ == '__main__':
    converter = VideoConvertor()
    ogg = converter.convert('test.mp4', file_format='ogg')
    ogg.save()
