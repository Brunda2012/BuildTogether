"""Rule-based matching. Works offline, so the demo never depends on an API."""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass

ROLES: dict[str, str] = {
    "job_seeker": "Job seeker",
    "company": "Company",
    "cofounder": "Looking for a co-founder",
    "investor": "Investor / VC",
}

ROLE_PLURALS: dict[str, str] = {
    "job_seeker": "job seekers",
    "company": "companies",
    "cofounder": "co-founders",
    "investor": "investors",
}

MEETING_MODES: dict[str, str] = {
    "in_person": "In person",
    "video": "Video",
    "either": "Either",
}

STOP_WORDS = {
    "and", "the", "for", "with", "that", "this", "are", "but", "not", "you",
    "our", "from", "who", "want", "looking", "into", "have", "has", "can",
    "building", "build", "need", "start", "role", "experience", "focused",
}


@dataclass
class Profile:
    """One person or organisation on Sammen."""

    id: int
    name: str
    role: str
    looking_for: list[str]
    city: str
    meeting_mode: str
    about: str
    verified: bool = False


@dataclass
class Match:
    """A suggested coffee between two profiles."""

    profile: Profile
    score: int
    reasons: list[str]
    meeting: str
    intro: str | None = None


def extract_keywords(text: str) -> set[str]:
    """
    Reduce free text to lowercase keywords for overlap scoring.

    Parameters
    ----------
    text : str
        Free text from the "about" field

    Returns
    -------
    set of str
        Words with three or more letters, without stop words
    """
    words = re.findall(r"[a-zA-ZäöüæøåÄÖÜÆØÅß]{3,}", text.lower())
    return {word for word in words if word not in STOP_WORDS}


def suggest_meeting(first: Profile, second: Profile) -> str | None:
    """
    Decide how two people can meet.

    Returns
    -------
    str or None
        "Coffee in <city>", "Video coffee", or None if their preferences
        cannot be combined
    """
    same_city = first.city.strip().lower() == second.city.strip().lower()
    both_accept_in_person = "video" not in (first.meeting_mode, second.meeting_mode)
    both_accept_video = "in_person" not in (first.meeting_mode, second.meeting_mode)

    if same_city and both_accept_in_person:
        return f"Coffee in {first.city.strip()}"
    if both_accept_video:
        return "Video coffee"
    return None


# Cosine similarity range of the embedding model that maps to 0..40 points.
SIMILARITY_FLOOR = 0.6
SIMILARITY_CEILING = 0.9


def score_pair(
    person: Profile,
    candidate: Profile,
    similarity: Callable[[str, str], float | None] | None = None,
) -> Match | None:
    """
    Score one candidate for one person.

    Parameters
    ----------
    person : Profile
        The profile we are finding matches for
    candidate : Profile
        A possible match
    similarity : callable, optional
        Compares two "about" texts by meaning (see sammen.ai.similarity).
        If missing or unavailable, shared keywords are counted instead.

    Returns
    -------
    Match or None
        None unless both sides are looking for each other's role and a
        meeting format exists

    Notes
    -----
    Mutual interest is a hard requirement: nobody is shown to people they
    did not ask to meet.
    """
    if person.id == candidate.id:
        return None
    if candidate.role not in person.looking_for or person.role not in candidate.looking_for:
        return None

    meeting = suggest_meeting(person, candidate)
    if meeting is None:
        return None

    score = 50
    reasons = [
        f"You want to meet {ROLE_PLURALS[candidate.role]}, "
        f"and they want to meet {ROLE_PLURALS[person.role]}"
    ]

    shared_keywords = extract_keywords(person.about) & extract_keywords(candidate.about)
    meaning_score = similarity(person.about, candidate.about) if similarity else None
    if meaning_score is not None:
        closeness = (meaning_score - SIMILARITY_FLOOR) / (SIMILARITY_CEILING - SIMILARITY_FLOOR)
        score += round(max(0.0, min(closeness, 1.0)) * 40)
        if closeness >= 0.5:
            reasons.append("What you are looking for fits what they offer")
    else:
        score += min(len(shared_keywords), 4) * 10
    if shared_keywords:
        reasons.append("You both mention: " + ", ".join(sorted(shared_keywords)[:4]))

    if meeting.startswith("Coffee in"):
        score += 10
        reasons.append("You are in the same city")

    if candidate.verified:
        score += 5
        reasons.append("Verified profile")

    return Match(profile=candidate, score=min(score, 100), reasons=reasons, meeting=meeting)


def find_matches(
    person: Profile,
    candidates: list[Profile],
    limit: int = 5,
    similarity: Callable[[str, str], float | None] | None = None,
) -> list[Match]:
    """
    Rank the best coffee matches for one person.

    Parameters
    ----------
    person : Profile
        The profile we are finding matches for
    candidates : list of Profile
        Everyone else on the platform
    limit : int, default=5
        Maximum number of matches to return
    similarity : callable, optional
        Passed on to score_pair

    Returns
    -------
    list of Match
        Best matches first
    """
    matches = [score_pair(person, candidate, similarity) for candidate in candidates]
    ranked = sorted(
        (match for match in matches if match is not None),
        key=lambda match: match.score,
        reverse=True,
    )
    return ranked[:limit]
