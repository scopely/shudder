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


def poll_instance_metadata():
    """Check instance metadata for a scheduled termination"""
    r = requests.get("http://169.254.169.254/latest/meta-data/spot/termination-time")
    return r.status_code < 400

def get_instance_id():
    """Check instance metadata for an instance id"""
    r = requests.get("http://169.254.169.254/latest/meta-data/instance-id")
    return r.text

