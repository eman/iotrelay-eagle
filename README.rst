IoT Relay-Eagle
----------------------------------------------------
An Eagle™ Home Energy Gateway plugin for IoT Relay

Release v1.0.2

iotrelay-eagle is a data source plugin for IoT Relay. It polls an
Eagle™ Home Energy Gateway for power readings and forwards those
readings to data handlers connected to IoT Relay. This lets you pull
data from a smart meter and forward it for logging or analysis.

More information about IoT Relay may be found in its
`Documentation <http://iot-relay.readthedocs.org>`_.

iotrelay-eagle uses the `Meter Reader
<https://github.com/eman/meter_reader>`_ library to communicate with
the Eagle™ Home Energy Gateway.

iotrelay-eagle is available on PyPI and can be installed via pip.

.. code-block:: bash

    $ pip install iotrelay-eagle


Configuration

.. code-block:: ini

    ; ~/.iotrelay.cfg

    [iotrelay-eagle]
    series key = power
    address = 192.168.3.253
    timeout = 4
    poll frequency = 9

