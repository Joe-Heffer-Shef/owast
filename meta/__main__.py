import logging
import os
import datetime

import pymodm.connection

from meta.models.prov.activity import Activity

CONNECTION_STRING = os.environ['MONGO_URI']

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    pymodm.connection.connect(CONNECTION_STRING)

    end_time = datetime.datetime.utcnow()

    experiment = Activity(
        attributes=dict(
            drill_type='steel',
            speed=100,
        ),
        start_time=end_time - datetime.timedelta(minutes=30),
        end_time=end_time,
    )
    experiment.save()

    logger.info(repr(experiment))
    print(experiment.id)


if __name__ == '__main__':
    main()
