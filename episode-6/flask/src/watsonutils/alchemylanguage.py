# -*- coding: utf-8 -*-
# Copyright 2016 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

from watson_developer_cloud import AlchemyLanguageV1 as AlchemyLanguageService
from watson_developer_cloud import WatsonException

from .baseservice import BaseService


class AlchemyLanguageUtils(BaseService):
  def __init__(self, app):
    self.app = app
    super(AlchemyLanguageUtils, self).__init__("alchemy_api")
    self.service = AlchemyLanguageService(api_key=self.getAPIKey()) 

  def getAlchemyService(self):
    return self.service  

  def identifyKeyworkdsAndEntities(self, data):
    self.app.logger.info('Preparing to invoke AlchemyAPI Language service')
    txt = data.encode("utf-8", "replace")
    alchemy_language = self.getAlchemyService()

    alchemyResults = alchemy_language.combined(text=txt, show_source_text=True,
                                   extract=['entity', 'keyword'])
    self.app.logger.info(json.dumps(alchemyResults, indent=2))

    primeEntity = None
    primeKeyword = None

    entities = alchemyResults.get('entities')
    if entities: 
      primeEntity = entities[0].get('text', None)  

    keywords = alchemyResults.get('keywords')
    if keywords: 
      primeKeyword = keywords[0].get('text', None)

    return { "prime_entity": primeEntity,
             "prime_keyword": primeKeyword }


