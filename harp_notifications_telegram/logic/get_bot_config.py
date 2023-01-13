import requests
import harp_notifications_telegram.settings as settings
import traceback
from logger.logging import service_logger

log = service_logger()


def bot_config(bot_name):
    url = f"{settings.BOTS_SERVICE}/{bot_name}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    log.info(msg=f"Request {bot_name} config from bots service: {url}")
    try:
        req = requests.get(url=url, headers=headers, timeout=10, verify=False)
        if req.status_code == 200:
            log.info(msg=f"Receive {bot_name} response from bots service: {req.json()}")
            return req.json()['config']
        else:
            log.error(msg=f"Error during receiving bot config: {req.content}, stack: {traceback.format_exc()}")
    except Exception as err:
        log.error(msg=f"Error during receiving bot config: {err}, stack: {traceback.format_exc()}")
        return {'msg': None}
