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

"""Start the server and whatnot."""
import shudder.queue as queue


if __name__ == '__main__':
    conn, sqsq = queue.create_queue()
    sns_conn, sub = queue.subscribe_sns(sqsq)
    queue.death_row(sns_conn, sub, conn, sqsq)
