# Copyright 2015 Scopely, Inc.
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

"""Module to set up polling of instance metadata for the termination of a spot instance

"""
import requests
import logging
from shudder.config import CONFIG, LOG_FILE


logging.basicConfig(filename=LOG_FILE,format='%(asctime)s %(levelname)s:%(message)s',level=logging.INFO)
termination_time = "http://169.254.169.254/latest/meta-data/spot/termination-time"
instance_id = "http://169.254.169.254/latest/meta-data/instance-id"

def poll_instance_metadata():
    """Check instance metadata for a scheduled termination"""
    try:
      r = requests.get(termination_time)
      return r.status_code < 400
    except:
      logging.exception('Request to ' + termination_time + ' failed.')

def get_instance_id():
    """Check instance metadata for an instance id"""
    try:
      r = requests.get(instance_id)
      return r.text
    except:
      logging.exception('Request to ' + instance_id + ' failed.')
