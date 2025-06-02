import datetime
import sys
from pathlib import Path

import requests

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


class VKStats:
    def __init__(self, vk_api_key, group_id):
        """
        Конструктор для VKStats

        :param vk_api_key: API ключ для VK
        :param group_id: ID группы VK
        :return: None
        """
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def get_stats(self, start_date, end_date):
        """
        Получает статистику группы с указанной начальной даты по указанную конечную дату.

        :param start_date: Начальная дата в формате "YYYY-MM-DD"
        :param end_date: Конечная дата в формате "YYYY-MM-DD"
        :return: Ответ от VK API
        :raises Exception: Если VK API возвращает ошибку
        """
        url = "https://api.vk.com/method/stats.get"
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        start_date = start_date.replace(tzinfo=datetime.timezone.utc)
        end_date = end_date.replace(tzinfo=datetime.timezone.utc)

        start_unix_time = start_date.timestamp()
        end_unix_time = end_date.timestamp()

        params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "group_id": self.group_id,
            "timestamp_from": start_unix_time,
            "timestamp_to": end_unix_time,
        }
        response = requests.get(url, params=params).json()
        if "error" in response:
            raise Exception(response["error"]["error_msg"])
        else:
            return response["response"][0]

    def get_followers(self):
        """
        Получает количество подписчиков группы.

        :return: Количество подписчиков
        :raises Exception: Если VK API возвращает ошибку
        """
        url = "https://api.vk.com/method/groups.getMembers"
        params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "group_id": self.group_id,
        }
        response = requests.get(url, params=params).json()
        if "error" in response:
            raise Exception(response["error"]["error_msg"])
        else:
            return response["response"]["count"]

    def get_likes_and_views(self, count=100):
        """
        Получает количество лайков и просмотров последних N постов.

        :param count: Количество постов для анализа (макс. 100)
        :return: Список словарей с лайками и просмотрами для каждого поста
        :raises Exception: Если VK API возвращает ошибку
        """
        url = "https://api.vk.com/method/wall.get"
        params = {
            "access_token": self.vk_api_key,
            "v": "5.236",
            "owner_id": f"-{self.group_id}",  # отрицательное значение для групп
            "count": count,
        }
        response = requests.get(url, params=params).json()
        if "error" in response:
            raise Exception(response["error"]["error_msg"])

        result = []
        for item in response["response"]["items"]:
            stats = {
                "post_id": item["id"],
                "likes": item["likes"]["count"],
                "views": item["views"]["count"] if "views" in item else 0,
                "date": datetime.datetime.fromtimestamp(item["date"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
            result.append(stats)
        return result
