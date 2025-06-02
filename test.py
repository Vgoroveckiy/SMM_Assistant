import config as conf
from generators.image_gen import ImageGenerator
from generators.text_gen import PostGenerator
from social_publishers.vk_publisher import VKPublisher

post_gen = PostGenerator(
    conf.openai_key,
    "позитивный и веселый",
    "Аксессуары для чайных церемоний от компании ZeroTee",
)
content = post_gen.generate_post()
img_desc = post_gen.generate_post_image_description()

img_gen = ImageGenerator(conf.openai_key)
img_url = img_gen.generate_image(img_desc)

print(content)
print(img_url)

vk_pub = VKPublisher(conf.vk_api_key, conf.vk_group_id)
vk_pub.publish_post(content, img_url)
