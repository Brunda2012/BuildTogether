"""Smoke tests: matching rules and the full join-to-matches flow."""

from pathlib import Path

import pytest

from app import create_app
from sammen import ai, db
from sammen.matching import Profile, find_matches, suggest_meeting
from sammen.seed import seed


def make_profile(profile_id: int, role: str, looking_for: list[str], **overrides) -> Profile:
    defaults = dict(name=f"Person {profile_id}", city="Copenhagen", meeting_mode="either",
                    about="lab automation", verified=False)
    defaults.update(overrides)
    return Profile(id=profile_id, role=role, looking_for=looking_for, **defaults)


def test_match_requires_mutual_interest():
    job_seeker = make_profile(1, "job_seeker", ["company"])
    interested_company = make_profile(2, "company", ["job_seeker"])
    uninterested_company = make_profile(3, "company", ["investor"])

    matches = find_matches(job_seeker, [job_seeker, interested_company, uninterested_company])

    assert [match.profile.id for match in matches] == [2]


def test_meeting_format_respects_preferences():
    in_person_only = make_profile(1, "cofounder", ["cofounder"], meeting_mode="in_person")
    video_only = make_profile(2, "cofounder", ["cofounder"], meeting_mode="video")
    other_city = make_profile(3, "cofounder", ["cofounder"], city="Munich")

    assert suggest_meeting(in_person_only, video_only) is None
    assert suggest_meeting(in_person_only, other_city) is None
    assert suggest_meeting(video_only, other_city) == "Video coffee"


@pytest.fixture(autouse=True)
def no_real_api_calls(monkeypatch):
    monkeypatch.delenv("MISTRAL_API_KEY", raising=False)
    monkeypatch.setattr(ai, "load_env_file", lambda *args: None)
    ai.embed.cache_clear()
    ai.coffee_intro.cache_clear()


@pytest.fixture
def client(tmp_path: Path):
    database_path = tmp_path / "test.db"
    with db.connect(database_path) as connection:
        seed(connection)
    return create_app(database_path).test_client()


def test_join_flow_shows_matches(client):
    response = client.post("/join", data={
        "name": "Test Founder", "role": "cofounder", "looking_for": ["cofounder", "investor"],
        "city": "Copenhagen", "meeting_mode": "either",
        "about": "Biotech founder working on lab automation with python.",
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Mikkel Aagaard" in response.data
    assert b"Nordlys Ventures" in response.data


def test_invalid_form_and_bot_trap_are_rejected(client):
    assert client.post("/join", data={"name": ""}).status_code == 400
    assert client.post("/join", data={"name": "Bot", "website": "spam.example"}).status_code == 400


def test_meaning_based_score_beats_keywords():
    founder = make_profile(1, "cofounder", ["cofounder"], about="pipetting robots")
    close = make_profile(2, "cofounder", ["cofounder"], about="liquid handling machines")
    far = make_profile(3, "cofounder", ["cofounder"], about="fashion marketplace")
    fake_similarity = lambda first, second: 0.9 if "liquid" in second else 0.5

    matches = find_matches(founder, [close, far], similarity=fake_similarity)

    assert [match.profile.id for match in matches] == [2, 3]
    assert matches[0].score > matches[1].score


def test_ai_features_with_mocked_mistral(client, monkeypatch):
    def fake_post(path: str, payload: dict) -> dict:
        if path == "/moderations":
            flagged = "attack" in payload["input"][0]
            return {"results": [{"categories": {"violence_and_threats": flagged}}]}
        if path == "/embeddings":
            return {"data": [{"embedding": [1.0, 0.0]}]}
        return {"choices": [{"message": {"content": "You both build lab automation."}}]}

    monkeypatch.setattr(ai, "post", fake_post)
    form = {"name": "Test Founder", "role": "cofounder", "looking_for": ["cofounder"],
            "city": "Copenhagen", "meeting_mode": "either", "about": "Lab automation founder."}

    assert b"You both build lab automation." in client.post("/join", data=form, follow_redirects=True).data
    assert client.post("/join", data={**form, "about": "I will attack you"}).status_code == 400


def test_ai_failure_falls_back_to_rules(client, monkeypatch):
    monkeypatch.setattr(ai, "post", lambda path, payload: None)

    assert ai.similarity("first", "second") is None
    assert ai.is_text_safe("anything") is True
    assert ai.coffee_intro("A", "about a", "B", "about b") is None
