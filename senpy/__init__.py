#!/usr/bin/python
# -*- coding: utf-8 -*-
#    Copyright 2014 J. Fernando Sánchez Rada - Grupo de Sistemas Inteligentes
#                                                       DIT, UPM
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""
Sentiment analysis server in Python
"""
from __future__ import print_function
from .version import __version__

try:
    import semver
    __version_info__ = semver.parse_version_info(__version__)

    if __version_info__.prerelease:
        import logging
        logger = logging.getLogger(__name__)
        msg = 'WARNING: You are using a pre-release version of {} ({})'.format(
            __name__, __version__)
        if len(logging.root.handlers) > 0:
            logger.info(msg)
        else:
            import sys
            print(msg, file=sys.stderr)
except ImportError:
    print('semver not installed. Not doing version checking')

__all__ = ['api', 'blueprints', 'cli', 'extensions', 'models', 'plugins']
