import json
import requests

from homeassistant.helpers.event import track_point_in_time
from homeassistant.util import dt as dt_util

DOMAIN = 'gebeds_assistent'

#   config
street = "your street"  # fill in your streetname
housenumber = "your housenumer"  # fill in your housenumber
city = "your city"  # fill in your city
country = "your country"  # fill in your country
angle = "15.0,null,15.0"  # fill in angle

#   request 
location = street + " " + housenumber + "," + city + "," + country
url = "https://api.aladhan.com/timingsByAddress?address=" + location + "&method=99&methodSettings=" + angle + ".json"
headers = {'content-type': 'application/json'}


def setup(hass, config):
    def update(now=None):
        #   request
        r = requests.get(url, headers)
        response = r.content.decode("utf-8")
        jsonstring = json.loads(response)
        inner = jsonstring["data"]

        prayer = inner["timings"]

        fajr = prayer["Fajr"]
        sunrise = prayer["Sunrise"]
        dhuhr = prayer["Dhuhr"]
        asr = prayer["Asr"]
        maghrib = prayer["Maghrib"]
        isha = prayer["Isha"]

        hass.states.set('Gebedstijden.Fajr', fajr)
        hass.states.set('Gebedstijden.Sunrise', sunrise)
        hass.states.set('Gebedstijden.Dhuhr', dhuhr)
        hass.states.set('Gebedstijden.Asr', asr)
        hass.states.set('Gebedstijden.Maghrib', maghrib)
        hass.states.set('Gebedstijden.Isha', isha)

        # Run again at next (local) midnight.
        track_point_in_time(
            hass, update,
            dt_util.find_next_time_expression_time(dt_util.now(), [0], [0], [0]))

    update()
    return True
