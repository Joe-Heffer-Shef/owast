import logging
import os
import uuid
import datetime

import pymodm.connection

import meta.models.activity

CONNECTION_STRING = os.environ['MONGO_URI']

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.DEBUG)

    pymodm.connection.connect(CONNECTION_STRING)

    end_time = datetime.datetime.utcnow()

    experiment = meta.models.activity.Activity(
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
