from abc import abstractmethod, ABC
from typing import List, Dict, Optional


class ThirdPartyYouTubeLib(ABC):
    """
    Интерфейс удалённого сервиса
    """

    @abstractmethod
    def list_videos(self) -> List[str]:
        pass

    @abstractmethod
    def get_video_info(self, video_id: str) -> str:
        pass

    @abstractmethod
    def download_video(self, video_id: str) -> str:
        pass


class ThirdPartyYouTubeClass(ThirdPartyYouTubeLib):
    """
    Конкретная реализация сервиса. Методы этого класса
    запрашивают у YouTube различную информацию. Скорость запроса
    зависит не только от качества интернет-канала пользователя,
    но и от состояния самого YouTube. Значит, чем больше будет
    вызовов к сервису, тем менее отзывчивой станет программа.
    """

    def list_videos(self) -> List[str]:
        # Получить список видеороликов с помощью API YouTube.
        print("Запрос списка видеороликов с YouTube.")
        return ['video1', 'video2', 'video3']

    def get_video_info(self, video_id: str) -> str:
        # Получить детальную информацию о каком-то видеоролике.
        print(f"Запрос информации о видео: {video_id}")
        return f"Информация о видео: {video_id}"

    def download_video(self, video_id: str) -> str:
        # Скачать видео с YouTube.
        print(f"Скачивание видео: {video_id}")
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

    def __init__(self, service: ThirdPartyYouTubeLib):
        self._service = service
        self._list_cache: Optional[List[str]] = None
        self._video_cache: Dict[str, str] = {}
        self._cache_valid: bool = True

    def list_videos(self) -> List[str]:
        if self._list_cache is None or not self._cache_valid:
            print("Кеш устарел или отсутствует. Обновление кеша списка видеороликов.")
            self._list_cache = self._service.list_videos()
            self._cache_valid = True
        else:
            print("Использование кеша для списка видеороликов.")
        return self._list_cache

    def get_video_info(self, video_id: str) -> str:
        if video_id not in self._video_cache or not self._cache_valid:
            print(f"Кеш устарел или отсутствует. Обновление кеша информации о видео: {video_id}")
            self._video_cache[video_id] = self._service.get_video_info(video_id)
            self._cache_valid = True
        else:
            print(f"Использование кеша для информации о видео: {video_id}")
        return self._video_cache[video_id]

    def download_video(self, video_id: str) -> str:
        print(f"Запрос на скачивание видео: {video_id}")
        return self._service.download_video(video_id)


class YouTubeManager:
    def __init__(self, service: ThirdPartyYouTubeLib):
        self.service = service

    def render_video_page(self, video_id: str) -> None:
        info = self.service.get_video_info(video_id)
        print(f"Rendering video page for {video_id}: {info}")
        # Логика отображения страницы видеоролика

    def render_list_panel(self) -> None:
        video_list = self.service.list_videos()
        print(f"Rendering list panel with videos: {video_list}")
        # Логика отображения списка превьюшек видеороликов

    def download_video(self, video_id: str) -> None:
        self.service.download_video(video_id)
        print(f"Downloading video: {video_id}")

    def react_on_user_input(self) -> None:
        self.render_video_page("video1")
        self.download_video("video1")
        self.render_list_panel()


if __name__ == "__main__":
    youtube_service = ThirdPartyYouTubeClass()
    youtube_proxy = CachedYouTubeClass(youtube_service)
    manager = YouTubeManager(youtube_proxy)
    manager.react_on_user_input()
