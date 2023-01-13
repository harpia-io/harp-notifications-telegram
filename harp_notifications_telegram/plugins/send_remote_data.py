import json

import requests
from logger.logging import service_logger
import traceback

log = service_logger()


def send_data(url, content: dict):
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json"
	}

	try:
		req = requests.put(
			url=url,
			data=json.dumps(content),
			headers=headers,
			timeout=10
		)
		if req.status_code == 200:
			return req.json()
		else:
			return False
	except Exception as err:
		log.error(msg=f"Error: {err}, stack: {traceback.format_exc()}")
		return {'msg': None}
