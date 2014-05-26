'''
Copyright (c) 2014, Emmanuel Levijarvi
All rights reserved.
License BSD
'''
import logging
import datetime
from iotrelay import Reading
from meter_reader import Gateway, GatewayError

logger = logging.getLogger(__name__)
__version__ = "1.0.1"


class Poll(object):
    def __init__(self, config):
        self.config = config
        self.series_key = config['series key']
        self.gateway = Gateway(config['address'])
        self.gateway.timeout = float(config['timeout'])
        # poll_frequency: seconds between readings
        poll_frequency = int(config['poll frequency'])
        self.delta = datetime.timedelta(seconds=poll_frequency)
        self.next_reading_time = datetime.datetime.now()
        self.last_timestamp = None

    def get_readings(self):
        if datetime.datetime.now() < self.next_reading_time:
            return
        try:
            timestamp, demand = self.gateway.get_instantaneous_demand()
        except GatewayError as e:
            logger.error(e)
            self.next_reading_time = datetime.datetime.now() + self.delta / 2
            return
        if self.last_timestamp is None or timestamp != self.last_timestamp:
            logger.info("{0!s}, {1!s}".format(timestamp, demand))
            self.last_timestamp = timestamp
            self.next_reading_time = datetime.datetime.now() + self.delta
            return Reading('power', demand, timestamp, self.series_key)
        else:
            logger.warning('duplicate reading')
            self.next_reading_time = datetime.datetime.now() + self.delta / 2
