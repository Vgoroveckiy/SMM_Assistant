import requests


class VKPublisher:
    def __init__(self, vk_api_key, group_id):
        """
        Конструктор для VKPublisher

        :param vk_api_key: Ключ доступа к VK API
        :param group_id: ID группы VK
        :return: None
        """
        self.vk_api_key = vk_api_key
        self.group_id = group_id

    def upload_photo(self, image_url):
        """
        Загружает фотографию на VK и возвращает строку для вложения.

        Данная функция обрабатывает процесс загрузки фотографии на VK, сначала получая
        URL сервера загрузки на стену, затем загружая изображение на этот URL, и
        потом сохраняя его на сервере VK. Она возвращает строку, которая может быть
        использована в качестве вложения для поста VK.

        :param image_url: URL изображения, которое будет загружено.
        :return: Строка в формате 'photo{owner_id}_{photo_id}' для вложения фотографии к посту.
        :raises Exception: Если происходит ошибка при получении URL загрузки или на любом шаге процесса загрузки.
        """
        upload_url_response = requests.get(
            url="https://api.vk.com/method/photos.getWallUploadServer",
            params={
                "access_token": self.vk_api_key,
                "v": "5.236",
                "group_id": self.group_id,
            },
        ).json()

        if "error" in upload_url_response:
            raise Exception(upload_url_response["error"]["error_msg"])
        else:
            upload_url = upload_url_response["response"]["upload_url"]

            image_data = requests.get(image_url).content

            upload_response = requests.post(
                upload_url, files={"photo": ("image.jpg", image_data)}
            ).json()

            save_response = requests.get(
                url="https://api.vk.com/method/photos.saveWallPhoto",
                params={
                    "access_token": self.vk_api_key,
                    "v": "5.236",
                    "group_id": self.group_id,
                    "photo": upload_response["photo"],
                    "server": upload_response["server"],
                    "hash": upload_response["hash"],
                },
            ).json()

            photo_id = save_response["response"][0]["id"]
            owner_id = save_response["response"][0]["owner_id"]

            return f"photo{owner_id}_{photo_id}"

    def publish_post(self, content, image_url=None):
        """
        Метод для публикации поста в VK.

        :param content: текст поста
        :param image_url: URL изображения, которое будет добавлено к посту
        :return: ответ от VK API в виде JSON-объекта
        :raises Exception: если происходит ошибка при загрузке изображения или на любом шаге процесса публикации.
        """
        params = {
            "access_token": self.vk_api_key,
            "from_group": 1,
            "v": "5.236",
            "owner_id": f"-{self.group_id}",
            "message": content,
        }
        if image_url:
            attachment = self.upload_photo(image_url)
            params["attachments"] = attachment

        response = requests.post(
            "https://api.vk.com/method/wall.post", params=params
        ).json()

        return response
