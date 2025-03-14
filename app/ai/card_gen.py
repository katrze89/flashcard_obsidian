import logging
import os
from pathlib import Path
from typing import Any

import dotenv
from openai import OpenAI

from app.tools.open_file import open_file

logger = logging.getLogger(__name__)


class CardGen:
    system_prompt_path: Path = Path(__file__).parent.resolve() / "prompts"

    def __new__(cls, *args: Any, **kwargs: Any) -> "CardGen":
        dotenv.load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env", ".env-chatgpt"))
        if os.getenv("OPENAI_API_KEY", None) is None:
            raise EnvironmentError("OPENAI_API_KEY is not set")

        return super().__new__(cls)

    def __init__(self, model: str = "gpt-3.5-turbo-16k", response_format: dict[str, str] | None = None):
        self.client = OpenAI()
        self.model = model
        self.response_format = response_format if response_format is not None else {"type": "json_object"}

    def create_flashcard_json(self, user_prompt: str) -> Any:
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": open_file(type(self).system_prompt_path / "system_prompt.txt")},
            {"role": "user", "content": user_prompt},
        ]

        logger.info(f"Creating flashcard json for user: {len(user_prompt.split())}")

        return self.client.chat.completions.create(
            model=self.model,
            # response_format=self.response_format,
            messages=messages,  # type: ignore
        )
