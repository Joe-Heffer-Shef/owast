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
        id=str(uuid.uuid4()),
        attributes=dict(
            drill_type='steel',
            speed=100,
        ),
        start_time=end_time - datetime.timedelta(minutes=30),
        end_time=end_time,

    )
    logger.info(experiment)
    experiment.save()

    logger.debug(experiment.id)
    logger.debug(experiment.start_time)
    logger.debug(dir(experiment))


if __name__ == '__main__':
    main()
