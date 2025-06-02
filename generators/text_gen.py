from openai import OpenAI


class PostGenerator:

    def __init__(self, openai_key: str, tone: str, topic: str):
        """
        Аргументы:
            openai_key (str): API-ключ для OpenAI.
            tone (str): Пожелаемый тон для генерируемого текста.
            topic (str): Тема для генерируемого текста.
        """
        self.client = OpenAI(api_key=openai_key)
        self.tone = tone
        self.topic = topic

    def generate_post(self):
        """
        Генерирует текст для поста в социальной сети на основе заданной темы и тона.

        Функция использует модель GPT-4o-mini для создания текста, который будет
        соответствовать указанной теме и настроению. Взаимодействие с моделью
        происходит через симуляцию диалога, где система выступает в роли SMM
        специалиста, а пользователь задает тему и тон.

        Возвращает:
            str: Сгенерированный текст для поста.
        """

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты высококвалифицированный SMM специалист, который будет помогать в генерации текста для постов с заданной тебе тематикой и заданным тоном.",
                },
                {
                    "role": "user",
                    "content": f"Сгенерировать текст для соцсети с темой: {self.topic} и тоном: {self.tone}.",
                },
            ],
        )

        return response.choices[0].message.content

    def generate_post_image_description(self):
        """
        Генерирует текст-описание для изображения, которое будет сгенерировано
        на основе заданной темы.

        Функция использует модель GPT-4o-mini для создания текста, который будет
        соответствовать указанной теме. Взаимодействие с моделью
        происходит через симуляцию диалога, где система выступает в роли
        ассистента, а пользователь задает тему.

        Возвращает:
            str: Сгенерированный текст-описание для изображения.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Ты ассистент, который составит промт для нейронной сети, которая будет генерировать изображения. Ты должен составить промт на заданную тему.",
                },
                {
                    "role": "user",
                    "content": f"Сгенерируй изображение для соцсети с темой: {self.topic}",
                },
            ],
        )

        return response.choices[0].message.content
