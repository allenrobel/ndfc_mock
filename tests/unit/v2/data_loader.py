# Copyright (c) 2024 Cisco and/or its affiliates.
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

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import os
import sys

data_path = os.path.join(os.path.dirname(__file__), "data")


def load_data(filename):
    """
    # Summary

    Load test data from a JSON file.

    ## Parameters

    - filename

    The file from which to load the data.
    The file is assumed to be in ./data/{filename}

    ## Example

    fabric.json

    Would load the following file:

    ./data/fabric.json

    ## Returns

    A dictionary containing the data from the file.
    """
    path = os.path.join(data_path, f"{filename}")

    try:
        with open(path, encoding="utf-8") as file_handle:
            data_dict = file_handle.read()
    except IOError as exception:
        msg = f"Exception opening test input file {filename} : "
        msg += f"Exception detail: {exception}"
        print(msg)
        sys.exit(1)

    try:
        data_json = json.loads(data_dict)
    except json.JSONDecodeError as exception:
        msg = "Exception reading JSON contents in "
        msg += f"test input file {filename} : "
        msg += f"Exception detail: {exception}"
        print(msg)
        sys.exit(1)

    return data_json
