from celery import Celery


def create_celery_app():
    app = Celery()
    app.conf.broker_url = 'amqp://guest:guest@localhost:5672//'
    app.conf.result_backend = 'rpc://'
    app.conf.update(task_track_started=True)
    app.conf.update(task_serializer='pickle')
    app.conf.update(result_serializer='pickle')
    app.conf.update(accept_content=['pickle', 'json'])
    app.conf.update(result_persistent=True)
    app.conf.update(worker_send_task_events=False)
    app.conf.update(worker_prefetch_multiplier=1)
    app.conf.update(task_track_started = True)
    app.conf.update( broker_transport_options={
        'confirm_publish': True,
        'publish_retry': True,
        'delivery_mode': 2,
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
        'acknowledgements_timeout': 3600000,  # Set the timeout to 1 hour in milliseconds
        'timeout': 3600,
            })


    return app
