"""Module for setting up an sqs queue subscribed to
an sns topic polling for messages pertaining to our
impending doom.

"""
import json
import time
import requests
from boto.utils import get_instance_metadata
import boto.sns as sns
import boto.sqs as sqs
from shudder.config import CONFIG


INSTANCE_ID = get_instance_metadata()['instance-id']
QUEUE_NAME = "{prefix}-{id}".format(prefix=CONFIG['sqs_prefix'],
                                    id=INSTANCE_ID)


def create_queue():
    """Creates the sqs queue and returns the connection/queue"""
    conn = sqs.connect_to_region(CONFIG['region'])
    queue = conn.create_queue(QUEUE_NAME)
    queue.set_timeout(60 * 60)  # one hour
    return conn, queue


def subscribe_sns(queue):
    """Subscribes the SNS topic to the queue."""
    conn = sns.connect_to_region(CONFIG['region'])
    subscription = conn.subscribe_sqs_queue(CONFIG['sns_topic'], queue)
    return conn, subscription


def should_terminate(msg):
    """Check if the termination message is about our instance"""
    first_box = json.loads(msg.get_body())
    body = json.loads(first_box['Message'])
    termination_msg = 'autoscaling:EC2_INSTANCE_TERMINATING'
    return body.get('LifecycleTransition') == termination_msg \
        and INSTANCE_ID == body['EC2InstanceId']


def death_row(sns_conn, conn, queue):
    """Poll sqs until we get a termination message."""
    while True:
        message = queue.read()
        if message:
            conn.delete_message(queue, message)
            if should_terminate(message):
                queue.delete()
                sns_conn.unsubscribe(CONFIG['sns_topic'])
                return requests.get(CONFIG['endpoint'])
        time.sleep(3)
