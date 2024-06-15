"""
Заместитель — это структурный паттерн проектирования, который позволяет подставлять вместо реальных объектов специальные объекты-заменители.
Эти объекты перехватывают вызовы к оригинальному объекту, позволяя сделать что-то до или после передачи вызова оригиналу.

Проблема:
У вас есть внешний ресурсоёмкий объект, который нужен не все время, а изредка.
Мы могли бы создавать этот объект не в самом начале программы, а только тогда, когда он кому-то реально понадобится.
Каждый клиент объекта получил бы некий код отложенной инициализации. Но, вероятно, это привело бы к множественному дублированию кода.
В идеале, этот код хотелось бы поместить прямо в служебный класс, но это не всегда возможно. Например, код класса может
находиться в закрытой сторонней библиотеке.

Решение:
Паттерн Заместитель предлагает создать новый класс-дублёр, имеющий тот же интерфейс, что и оригинальный служебный объект.
При получении запроса от клиента объект-заместитель сам бы создавал экземпляр служебного объекта и переадресовывал бы ему всю реальную работу.
"""
from abc import abstractmethod, ABC


class ThirdPartyYouTubeLib(ABC):
    """
    Интерфейс удалённого сервиса
    """

    @abstractmethod
    def list_videos(self) -> None:
        pass

    @abstractmethod
    def get_video_info(self, video_id) -> None:
        pass

    @abstractmethod
    def download_video(self, video_id) -> None:
        pass


class ThirdPartyYouTubeClass(ThirdPartyYouTubeLib):
    """
    Конкретная реализация сервиса. Методы этого класса
    запрашивают у YouTube различную информацию. Скорость запроса
    зависит не только от качества интернет-канала пользователя,
    но и от состояния самого YouTube. Значит, чем больше будет
    вызовов к сервису, тем менее отзывчивой станет программа.
    """

    def list_videos(self) -> None:
        # Получить список видеороликов с помощью API YouTube.
        return ['video1', 'video2', 'video3']

    def get_video_info(self, video_id) -> None:
        # Получить детальную информацию о каком-то видеоролике.
        return f"Информация о видео: {video_id}"

    def download_video(self, video_id) -> None:
        #  Скачать видео с YouTube.
        return f"Скачивание видео: {video_id}"


class CachedYouTubeClass(ThirdPartyYouTubeLib):
    """
    С другой стороны, можно кешировать запросы к YouTube и не
    повторять их какое-то время, пока кеш не устареет. Но внести
    этот код напрямую в сервисный класс нельзя, так как он
    находится в сторонней библиотеке. Поэтому мы поместим логику
    кеширования в отдельный класс-обёртку. Он будет делегировать
    запросы к сервисному объекту, только если нужно
    непосредственно выслать запрос.
    """

    def __init__(self, service):
        self._service = service
        self._list_cache = None
        self._video_cache = {}
        self.need_reset = False

    def list_videos(self):
        if self._list_cache is None or self.need_reset:
            self._list_cache = self._service.list_videos()
            self.need_reset = False
        return self._list_cache

    def get_video_info(self, video_id):
        if video_id not in self._video_cache or self.need_reset:
            self._video_cache[video_id] = self._service.get_video_info(video_id)
            self.need_reset = False
        return self._video_cache[video_id]

    def download_video(self, video_id):
        return self._service.download_video(video_id)


class YouTubeManager:
    def __init__(self, service: ThirdPartyYouTubeLib):
        self.service = service

    def render_video_page(self, video_id):
        info = self.service.get_video_info(video_id)
        print(f"Rendering video page for {video_id}: {info}")
        # Логика отображения страницы видеоролика

    def render_list_panel(self):
        video_list = self.service.list_videos()
        print(f"Rendering list panel with videos: {video_list}")
        # Логика отображения списка превьюшек видеороликов

    def react_on_user_input(self):
        self.render_video_page("video1")
        self.render_list_panel()


if __name__ == "__main__":
    youtube_service = ThirdPartyYouTubeClass()
    youtube_proxy = CachedYouTubeClass(youtube_service)
    manager = YouTubeManager(youtube_proxy)
    manager.react_on_user_input()
