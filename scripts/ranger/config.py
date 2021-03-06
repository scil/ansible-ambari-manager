#!/usr/bin/env python

'''
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import ConfigParser
import logging
import os

class Config:
  def __init__(self):
    self.config = ConfigParser.RawConfigParser()
    current_file_dir = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(current_file_dir, 'config.ini')
    self.config.read(config_file)

  def get(self, section, option, default=None):
    if default is not None and not self.config.has_option(section, option):
      return default
    return self.config.get(section, option)

  def has_section(self, section):
    return self.config.has_section(section)

  def has_option(self, section, option):
    return self.config.has_option(section, option)
