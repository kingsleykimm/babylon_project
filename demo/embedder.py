import os
from typing import Optional


class OpenAIEmbedder():
    def __init__(self, config):
        if not config.model:
            self.model = "text-embedding-ada-002"
        else:
            self.model = config.model
            