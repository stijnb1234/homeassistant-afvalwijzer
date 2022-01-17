from datetime import datetime, timedelta
import logging

API = "api"
NAME = "afvalwijzer"
VERSION = "2021.12.02"
ISSUE_URL = "https://github.com/xirixiz/homeassistant-afvalwijzer/issues"

_LOGGER = logging.getLogger(__name__)

SENSOR_COLLECTOR_TO_URL = {
    "afvalwijzer_data_default": [
        "https://api.{0}.nl/webservices/appsinput/?apikey=5ef443e778f41c4f75c69459eea6e6ae0c2d92de729aa0fc61653815fbd6a8ca&method=postcodecheck&postcode={1}&street=&huisnummer={2}&toevoeging={3}&app_name=afvalwijzer&platform=phone&afvaldata={4}&langs=nl&"
    ],
    "afvalstoffendienstkalender": [
        "https://{0}.afvalstoffendienstkalender.nl/nl/{1}/{2}/"
    ],
    "afvalstoffendienstkalender-s-hertogenbosch": [
        "https://afvalstoffendienstkalender.nl/nl/{0}/{1}/"
    ],
    "ximmio01": [
        "https://wasteapi.ximmio.com/api/FetchAdress",
        "https://wasteapi.ximmio.com/api/GetCalendar",
    ],
    "ximmio02": [
        "https://wasteprod2api.ximmio.com/api/FetchAdress",
        "https://wasteprod2api.ximmio.com/api/GetCalendar",
    ],
}

SENSOR_COLLECTOR_TO_COMPANY_CODE = {
    "acv": "f8e2844a-095e-48f9-9f98-71fceb51d2c3",
    "almere": "53d8db94-7945-42fd-9742-9bbc71dbe4c1",
    "areareiniging": "adc418da-d19b-11e5-ab30-625662870761",
    "avalex": "f7a74ad1-fdbf-4a43-9f91-44644f4d4222",
    "avri": "78cd4156-394b-413d-8936-d407e334559a",
    "bar": "bb58e633-de14-4b2a-9941-5bc419f1c4b0",
    "hellendoorn": "24434f5b-7244-412b-9306-3a2bd1e22bc1",
    "meerlanden": "800bf8d7-6dd1-4490-ba9d-b419d6dc8a45",
    "meppel": "b7a594c7-2490-4413-88f9-94749a3ec62a",
    "rad": "13a2cad9-36d0-4b01-b877-efcb421a864d",
    "twentemilieu": "8d97bb56-5afd-4cbc-a651-b4f7314264b4",
    "waardlanden": "942abcf6-3775-400d-ae5d-7380d728b23c",
    "westland": "6fc75608-126a-4a50-9241-a002ce8c8a6c",
    "ximmio": "800bf8d7-6dd1-4490-ba9d-b419d6dc8a45",
    "reinis": "9dc25c8a-175a-4a41-b7a1-83f237a80b77",
}

# XIMMIO_URLS = {
#     "avalex": "https://wasteprod2api.ximmio.com",
#     "meerlanden": ["https://wasteprod2api.ximmio.com/api/FetchAdress", "https://wasteprod2api.ximmio.com/api/GetCalendar"]
#     "rad": "https://wasteprod2api.ximmio.com",
#     "westland": "https://wasteprod2api.ximmio.com",
# }


# XIMMIO_COLLECTOR_IDS = {
#     "acv": "f8e2844a-095e-48f9-9f98-71fceb51d2c3",
#     "almere": "53d8db94-7945-42fd-9742-9bbc71dbe4c1",
#     "areareiniging": "adc418da-d19b-11e5-ab30-625662870761",
#     "avalex": "f7a74ad1-fdbf-4a43-9f91-44644f4d4222",
#     "avri": "78cd4156-394b-413d-8936-d407e334559a",
#     "bar": "bb58e633-de14-4b2a-9941-5bc419f1c4b0",
#     "hellendoorn": "24434f5b-7244-412b-9306-3a2bd1e22bc1",
#     "meerlanden": "800bf8d7-6dd1-4490-ba9d-b419d6dc8a45",
#     "meppel": "b7a594c7-2490-4413-88f9-94749a3ec62a",
#     "rad": "13a2cad9-36d0-4b01-b877-efcb421a864d",
#     "twentemilieu": "8d97bb56-5afd-4cbc-a651-b4f7314264b4",
#     "waardlanden": "942abcf6-3775-400d-ae5d-7380d728b23c",
#     "westland": "6fc75608-126a-4a50-9241-a002ce8c8a6c",
#     "ximmio": "800bf8d7-6dd1-4490-ba9d-b419d6dc8a45",
#     "reinis": "9dc25c8a-175a-4a41-b7a1-83f237a80b77",
# }

CONF_COLLECTOR = "provider"
CONF_API_TOKEN = "api_token"
CONF_POSTAL_CODE = "postal_code"
CONF_STREET_NUMBER = "street_number"
CONF_SUFFIX = "suffix"
CONF_DATE_FORMAT = "date_format"
CONF_INCLUDE_DATE_TODAY = "include_date_today"
CONF_DEFAULT_LABEL = "default_label"
CONF_ID = "id"
CONF_EXCLUDE_LIST = "exclude_list"

SENSOR_PREFIX = "afvalwijzer "
SENSOR_ICON = "mdi:recycle"

ATTR_LAST_UPDATE = "last_update"
ATTR_IS_COLLECTION_DATE_TODAY = "is_collection_date_today"
ATTR_IS_COLLECTION_DATE_TOMORROW = "is_collection_date_tomorrow"
ATTR_IS_COLLECTION_DATE_DAY_AFTER_TOMORROW = "is_collection_date_day_after_tomorrow"
ATTR_DAYS_UNTIL_COLLECTION_DATE = "days_until_collection_date"
ATTR_YEAR_MONTH_DAY_DATE = "year_month_day_date"

MIN_TIME_BETWEEN_UPDATES = timedelta(hours=1)
PARALLEL_UPDATES = 1
SCAN_INTERVAL = timedelta(seconds=30)

TODAY = datetime.today().strftime("%d-%m-%Y")
DATE_TODAY = datetime.strptime(TODAY, "%d-%m-%Y")
DATE_TOMORROW = datetime.strptime(TODAY, "%d-%m-%Y") + timedelta(days=1)
DATE_DOT = datetime.strptime(TODAY, "%d-%m-%Y") + timedelta(days=2)
DATE_TODAY_NEXT_YEAR = (DATE_TODAY.date() + timedelta(days=365)).strftime("%Y-%m-%d")

DOMAIN = "afvalwijzer"
DOMAIN_DATA = "afvalwijzer_data"

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------,
Afvalwijzer - {VERSION},
This is a custom integration!,
If you have any issues with this you need to open an issue here:,
https://github.com/xirixiz/homeassistant-afvalwijzer/issues,
-------------------------------------------------------------------,
"""
