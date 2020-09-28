#!/usr/bin/env python3
from datetime import datetime, date, timedelta
from .const.const import (
    _LOGGER,
    MIN_TIME_BETWEEN_UPDATES,
    PARALLEL_UPDATES,
    SENSOR_ICON,
    SENSOR_PREFIX,
    ATTR_LAST_UPDATE,
    ATTR_DAYS_UNTIL_COLLECTION_DATE,
    ATTR_YEAR_MONTH_DAY_DATE
)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle


class AfvalwijzerCustomSensor(Entity):
    def __init__(self, hass, fetch_afvalwijzer_data, waste_type, default_label):
        self.fetch_afvalwijzer_data = fetch_afvalwijzer_data
        self.waste_type = waste_type
        self.default_label = default_label
        self._last_update = None
        self._name = SENSOR_PREFIX + waste_type
        self._state = None
        self._icon = SENSOR_ICON
        self._year_month_day_date = None

    @property
    def name(self):
        return self._name

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        if self.waste_type == "first_next_date":
            return {ATTR_LAST_UPDATE: self._last_update, ATTR_YEAR_MONTH_DAY_DATE: self._year_month_day_date}
        else:
            return {ATTR_LAST_UPDATE: self._last_update}

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        await self.hass.async_add_executor_job(self.fetch_afvalwijzer_data.update)
        waste_data_custom = self.fetch_afvalwijzer_data.waste_data_custom
        _LOGGER.debug("Generating state via AfvalwijzerCustomSensor for = %s", waste_data_custom)

        self._last_update = datetime.today().strftime("%d-%m-%Y %H:%M")
        self._state = waste_data_custom[self.waste_type]

        if self.waste_type == "first_next_date":
            if waste_data_custom["first_next_date"] != self.default_label:

                # Add date in Dutch and US format
                collection_date_nl = waste_data_custom[self.waste_type]
                _LOGGER.debug("AfvalwijzerCustomSensorcollection_date_nl = %s", collection_date_nl)
                collection_date_convert_to_us = datetime.strptime(waste_data_custom[self.waste_type], "%d-%m-%Y").strftime("%Y-%m-%d")
                collection_date_us = datetime.strptime(collection_date_convert_to_us, "%Y-%m-%d").date()
                _LOGGER.debug("AfvalwijzerCustomSensorcollection_date_us = %s", collection_date_us)

                # Add attribute date in format "%Y-%m-%d"
                self._year_month_day_date = str(collection_date_us)
