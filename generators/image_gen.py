from openai import OpenAI


class ImageGenerator:
    def __init__(self, openai_key):
        """
        Создает экземпляр класса ImageGenerator.

        Аргументы:
            openai_key (str): API ключ для DALL-E API от OpenAI.

        Возвращает:
            None
        """
        self.client = OpenAI(api_key=openai_key)

    # def generate_image(self, prompt):
    #     response = self.client.images.generate(
    #         model="dall-e-3",
    #         prompt=prompt,
    #         size="1024x1024",  # единственный размер
    #         quality="standard",
    #         n=1,
    #     )

    #     if response.data is not None:
    #         return response.data[0].url
    #     else:
    #         return None

    # Для тестов беру дешевле модель. По качеству и пониманию промтов отстой полный.
    # Очень некачественно и плохо понимает промт, но в 4 раза дешевле при тех же параметрах. Промт в два раза дешевле получается.
    # Размеры есть 256x256, 512x512, 1024x1024
    def generate_image(self, prompt):
        """
        Генерирует изображение на основе заданного текстового приглашения с использованием модели DALL-E 2.

        Аргументы:
            prompt (str): Текстовое приглашение для генерации изображения.

        Возвращает:
            str: URL сгенерированного изображения или None, если генерация не удалась.
        """
        response = self.client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            size="256x256",
            n=1,
        )

        if response.data is not None:
            return response.data[0].url
        else:
            return None
