# Copyright 2014 Scopely, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for setting up an sqs queue subscribed to
an sns topic polling for messages pertaining to our
impending doom.

"""
import json

from boto.utils import get_instance_metadata
import boto.sns as sns
import boto.sqs as sqs

from shudder.config import CONFIG


INSTANCE_ID = get_instance_metadata()['instance-id']
QUEUE_NAME = "{prefix}-{id}".format(prefix=CONFIG['sqs_prefix'],
                                    id=INSTANCE_ID)


def create_queue():
    """Creates the SQS queue and returns the connection/queue"""
    conn = sqs.connect_to_region(CONFIG['region'])
    queue = conn.create_queue(QUEUE_NAME)
    queue.set_timeout(60 * 60)  # one hour
    return conn, queue


def subscribe_sns(queue):
    """Subscribes the SNS topic to the queue."""
    conn = sns.connect_to_region(CONFIG['region'])
    sub = conn.subscribe_sqs_queue(CONFIG['sns_topic'], queue)
    sns_arn = sub['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    return conn, sns_arn


def should_terminate(msg):
    """Check if the termination message is about our instance"""
    first_box = json.loads(msg.get_body())
    body = json.loads(first_box['Message'])
    termination_msg = 'autoscaling:EC2_INSTANCE_TERMINATING'
    return body.get('LifecycleTransition') == termination_msg \
        and INSTANCE_ID == body['EC2InstanceId']


def clean_up_sns(sns_conn, sns_arn, queue):
    """Clean up SNS subscription and SQS queue"""
    queue.delete()
    sns_conn.unsubscribe(sns_arn)


def poll_queue(conn, queue):
    """Poll SQS until we get a termination message."""
    message = queue.read()
    if message:
        conn.delete_message(queue, message)
        return should_terminate(message)
    return False