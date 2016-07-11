'''
Copyright (c) 2016, Emmanuel Levijarvi
All rights reserved.
License BSD 2-Clause
'''
import logging
import datetime
from iotrelay import Reading
from meter_reader import Gateway, GatewayError

logger = logging.getLogger(__name__)
__version__ = "1.0.2"

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
        self.summ_delta = datetime.timedelta(seconds=summ_poll_frequency)
        self.delta = datetime.timedelta(seconds=poll_frequency)
        self.next_reading_time = datetime.datetime.now()
        self.summ_next_reading_time = datetime.datetime.now()
        self.last_timestamp = None
        self.last_summation = None

    def get_readings(self):
        summation = self.get_summation()
        power = self.get_power()
        if summation is None:
            return power
        summation.append(power)
        return summation

    def get_power(self):
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

    def get_summation(self):
        if datetime.datetime.now() < self.summ_next_reading_time:
            return
        try:
            summations = self.gateway.run_command(name='get_summation_values')
        except GatewayError as e:
            logger.error(e)
        self.sum_next_reading_time = datetime.datetime.now() + self.summ_delta
        return [Reading('power', s['Value'], s['TimeStamp'], 'summation')
                for s in summations]
