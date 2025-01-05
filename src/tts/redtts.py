import datetime
import os
import zipfile
import re
from io import BytesIO
from pathlib import Path

from manim import logger
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService

import requests

host = os.environ.get("REDTTS_SERVICE_HOST", "localhost")
port = os.environ.get("REDTTS_SERVICE_PORT", "8000")

URL = f"http://{host}:{port}/generate_voice"


def generate_voice(text, output_path):
    body = {
        "text": text,
    }

    try:
        response = requests.post(URL, json=body)
        response.raise_for_status()
        with open(output_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")


class RedTTSService(SpeechService):

    def generate_from_text(
        self, text: str, cache_dir: str = None, path: str = None, **kwargs
    ) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_text = remove_bookmarks(text)
        input_data = {"input_text": text, "service": "redtts"}
        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = path

        output_path = str(Path(cache_dir) / audio_path)

        generate_voice(text, output_path)

        json_dict = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
            # "word_boundaries": word_boundaries,
        }

        return json_dict
