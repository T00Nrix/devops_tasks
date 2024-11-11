import logging
import sys
import requests
from datetime import datetime
import pytz
import os

# logging
os.makedirs("../logs", exist_ok=True)
logging.basicConfig(level=logging.INFO, filename="../logs/lights_control.log", format='%(asctime)s; %(levelname)s; %(message)s')

def should_turn_lights_on(latitude, longitude, timezone_str='Europe/Amsterdam'):
    """
    Light turn
    :param latitude:
    :param longitude:
    :param timezone_str:
    :return:
    """
    try:
        timezone = pytz.timezone(timezone_str)
        current_date = datetime.utcnow().date()
        api_url = f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={current_date}&formatted=0'
        logging.info(f"[FETCHING] Sunrise and sunset time: {api_url}")

        response = requests.get(api_url)
        if response.status_code != 200:
            logging.error(f"[FAILED] API request with status code {response.status_code}")
            sys.exit(1)

        data = response.json()
        if data['status'] != 'OK':
            logging.error("[FAILED] Error fetching sunrise and sunset time.")
            sys.exit(1)

        sunrise_utc = datetime.fromisoformat(data['results']['sunrise'])
        sunset_utc = datetime.fromisoformat(data['results']['sunset'])
        sunrise_local = sunrise_utc.astimezone(timezone)
        sunset_local = sunset_utc.astimezone(timezone)
        now_local = datetime.now(timezone)

        if now_local < sunrise_local or now_local >= sunset_local:
            logging.info("[ON] Lights")
            return 'ON'
        else:
            logging.info("[OFF] Lights")
            return 'OFF'
    except Exception as e:
        logging.critical(f"[ERROR] {e}")
        sys.exit(1)

if __name__ == '__main__':
    latitude = 50.930581 # need also add config file in future
    longitude = 5.780691
    status = should_turn_lights_on(latitude, longitude)
    print(status)

# later can be used for setup vagrant
# need change the name