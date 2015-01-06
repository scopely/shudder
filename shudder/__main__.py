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

"""Start polling of SQS and metadata."""
import shudder.queue as queue
import shudder.metadata as metadata
from shudder.config import CONFIG

import time
import requests


if __name__ == '__main__':
    sqs_connection, sqs_queue = queue.create_queue()
    sns_connection, subscription_arn = queue.subscribe_sns(sqs_queue)
    while True:
        if queue.poll_queue(sns_connection, sqs_queue) \
                or metadata.poll_instance_metadata():
            queue.clean_up_sns(sns_connection, subscription_arn, sqs_queue)
            requests.get(CONFIG["endpoint"])
            break
        time.sleep(5)