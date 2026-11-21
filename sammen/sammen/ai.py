"""Mistral AI (European provider): meaning-based matching, intros, safety check.

Every function returns None (or a safe default) without an API key or when
the call fails, so the app keeps working on the rule-based matching alone.
"""

from __future__ import annotations

import json
import logging
import math
import os
import urllib.error
import urllib.request
from functools import lru_cache
from pathlib import Path

API_URL = "https://api.mistral.ai/v1"
CHAT_MODEL = "mistral-small-latest"
EMBED_MODEL = "mistral-embed"
MODERATION_MODEL = "mistral-moderation-latest"
TIMEOUT_SECONDS = 8

logger = logging.getLogger(__name__)


def load_env_file(env_path: Path = Path(__file__).resolve().parent.parent / ".env") -> None:
    """Read KEY=value lines from .env into the environment (existing values win)."""
    try:
        lines = env_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return
    for line in lines:
        if "=" in line and not line.strip().startswith("#"):
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


def is_enabled() -> bool:
    """Return True if a Mistral API key is configured."""
    return bool(os.environ.get("MISTRAL_API_KEY"))


def post(path: str, payload: dict) -> dict | None:
    """
    Send one request to the Mistral API.

    Parameters
    ----------
    path : str
        Endpoint path, for example "/embeddings"
    payload : dict
        JSON body

    Returns
    -------
    dict or None
        Parsed response, or None without a key or on any failure
    """
    if not is_enabled():
        return None
    request = urllib.request.Request(
        API_URL + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {os.environ['MISTRAL_API_KEY']}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        logger.warning("Mistral call to %s failed: %s", path, error)
        return None


@lru_cache(maxsize=512)
def embed(text: str) -> tuple[float, ...] | None:
    """Return the embedding of a text, or None if unavailable."""
    response = post("/embeddings", {"model": EMBED_MODEL, "input": [text]})
    try:
        return tuple(response["data"][0]["embedding"])
    except (TypeError, KeyError, IndexError):
        return None


def similarity(first_text: str, second_text: str) -> float | None:
    """
    Compare two texts by meaning.

    Returns
    -------
    float or None
        Cosine similarity (higher means closer), or None if unavailable
    """
    first, second = embed(first_text), embed(second_text)
    if first is None or second is None:
        return None
    dot_product = sum(a * b for a, b in zip(first, second))
    norms = math.sqrt(sum(a * a for a in first)) * math.sqrt(sum(b * b for b in second))
    return dot_product / norms if norms else None


def is_text_safe(text: str) -> bool:
    """
    Check profile text with Mistral's moderation model.

    Returns
    -------
    bool
        False only if the model flags the text. Without a key or on a
        failed call the text is accepted, so sign-up never blocks.
    """
    response = post("/moderations", {"model": MODERATION_MODEL, "input": [text]})
    try:
        return not any(response["results"][0]["categories"].values())
    except (TypeError, KeyError, IndexError, AttributeError):
        return True


@lru_cache(maxsize=512)
def coffee_intro(person_name: str, person_about: str, candidate_name: str, candidate_about: str) -> str | None:
    """
    Write one sentence on why two people should meet for a coffee.

    Returns
    -------
    str or None
        The sentence, or None if unavailable
    """
    prompt = (
        "Two people were matched for a coffee. In one warm, concrete sentence (max 30 words), "
        f"tell {person_name} why meeting {candidate_name} is worth it. Use only the facts below. "
        "No greeting, no emojis.\n\n"
        f"{person_name}: {person_about}\n{candidate_name}: {candidate_about}"
    )
    response = post("/chat/completions", {
        "model": CHAT_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
        "max_tokens": 80,
    })
    try:
        return response["choices"][0]["message"]["content"].strip()
    except (TypeError, KeyError, IndexError, AttributeError):
        return None
