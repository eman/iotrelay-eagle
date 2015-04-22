'''
Copyright (c) 2015, Emmanuel Levijarvi
All rights reserved.
License BSD
'''
import logging
import datetime
from iotrelay import Reading
from meter_reader import Gateway, GatewayError

logger = logging.getLogger(__name__)
__version__ = "1.0.1"

POLL_FREQUENCY = 9
SUMM_POLL_FREQUENCY = 600


class Poll(object):
    def __init__(self, config):
        self.config = config
        self.series_key = config['series key']
        self.gateway = Gateway(config['address'])
        self.gateway.timeout = float(config['timeout'])
        # poll_frequency: seconds between readings
        poll_frequency = int(config.get('poll frequency', POLL_FREQUENCY))
        summ_poll_frequency = int(config.get('summation poll frequency',
                                             SUMM_POLL_FREQUENCY))
        self.delta = datetime.timedelta(seconds=poll_frequency)
        self.next_reading_time = datetime.datetime.now()
        self.last_timestamp = None
        self.last_summation = None

    def get_readings(self):
        if datetime.datetime.now() < self.next_reading_time:
            return
        try:
            timestamp, demand = self.gateway.get_instantaneous_demand()
            summ = self.gateway.run_command(name='GET_SUMMATION_VALUES')[-1]
        except GatewayError as e:
            logger.error(e)
            self.next_reading_time = datetime.datetime.now() + self.delta / 2
            return
        if self.last_timestamp is None or timestamp != self.last_timestamp:
            logger.info("{0!s}, {1!s}".format(timestamp, demand))
            self.last_timestamp = timestamp
            self.next_reading_time = datetime.datetime.now() + self.delta
            power = Reading('power', demand, timestamp, self.series_key)
            if summ['TimeStamp'] == self.last_summation:
                return power
            self.last_summation = summ['TimeStamp']
            return [power,
                    Reading('power', summ['Value'], summ['TimeStamp'],
                            'summation')]
        else:
            logger.warning('duplicate reading')
            self.next_reading_time = datetime.datetime.now() + self.delta / 2

    def get_summation(self):
        summation = self.gateway.run_command(name='GET_SUMMATION_VALUES')
