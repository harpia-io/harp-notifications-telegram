import requests
from logger.logging import service_logger
from harp_notifications_telegram.logic.get_bot_config import bot_config

log = service_logger()


class NotificationProcessor(object):
    def __init__(self, telegram_chat_id):
        self.telegram_chat_id = telegram_chat_id
        self.bot_config = self.get_bot_config()

    def get_bot_config(self):
        config = self.bot_config = bot_config(bot_name='telegram')

        return config

    @staticmethod
    def generate_message(title, text, button_url, facts):
        message_section = [f"<strong>{title}</strong>", " "]

        if text:
            message_section.append(text)
            message_section.append(" ")

        if facts:
            for key, value in facts.items():
                message_section.append(f"<strong>{key}</strong>: {value}")
        message_section.append(" ")

        if button_url:
            message_section.append(f'<a href="{button_url}" class="button">Open Alert Details</a>')
            message_section.append(" ")

        return '\n'.join(message_section)

    def send_image_url(self, image_url, config):
        keyboard = {
            'inline_keyboard': [
                [
                    {
                        'text': 'Open Image',
                        'url': image_url
                    }
                ]
            ]
        }

        response = requests.post(
            f"https://api.telegram.org/bot{config['BOT_API_TOKEN']}/sendPhoto",
            json={
                'chat_id': self.telegram_chat_id,
                'photo': image_url,
                'reply_markup': keyboard
            }
        )

        log.info(msg=f"Send Image by URL\nResponse: {response.json()}")

    def send_image_body(self, image_body, config):
        response = requests.post(
            f"https://api.telegram.org/bot{config['BOT_API_TOKEN']}/sendPhoto",
            json={
                'chat_id': self.telegram_chat_id,
                'image_caption': ''
            },
            files={"photo": image_body}
        )

        log.info(msg=f"Send Image by Body\nResponse: {response.json()}")

    def send_notification(self, title, text, button_url, facts, image_url, image_body):
        config = bot_config(bot_name='telegram')
        api_url_message = f"https://api.telegram.org/bot{config['BOT_API_TOKEN']}/sendMessage"

        message_content = self.generate_message(
            title=title, text=text, button_url=button_url, facts=facts
        )

        try:
            response = requests.post(api_url_message, json={
                'chat_id': self.telegram_chat_id,
                'text': message_content,
                'parse_mode': 'html',
                'disable_web_page_preview': True
            })

            log.info(msg=response.json())

        except Exception as e:
            log.error(e)

        if image_url:
            self.send_image_url(image_url=image_url, config=config)

        if image_body:
            self.send_image_body(image_body=image_body, config=config)
