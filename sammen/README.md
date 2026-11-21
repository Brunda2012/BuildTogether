# Sammen

**Meet the right person. Over a coffee.**

Sammen (Danish for "together") matches job seekers, companies, people looking for a co-founder, and investors. Matched people meet for a coffee, in person or on video.

Built at Women Build AI, Copenhagen, 21–22 November 2026.

## Team

| Who | GitHub | Owns |
| --- | --- | --- |
| Steffi | @steffiAI | to be agreed |
|  | @brunda2012 | to be agreed |
|  | @ForiBor | to be agreed |

One owner per area: **product and build**, **design and demo flow**, **pitch and validation**.

## Timeline

Venue: Djøf, Gothersgade 133. We leave the venue by 22:00 on both days.

| When | What |
| --- | --- |
| Sat, time TBC | **Team lock-in** on [z2d-base.lovable.app](https://z2d-base.lovable.app) |
| Sat 20:00 | Pitch & Dine: show Day 1 progress (about 20% of pre-selection) |
| Sun 09:00 | Doors open |
| Sun, time TBC | **Final submission** on [z2d-base.lovable.app](https://z2d-base.lovable.app) |
| Sun 13:30 | **Pre-selection pitch and demo** (about 70% of pre-selection) |
| Sun 15:00 | Finalists announced |
| Sun 16:00 | Live demos and judging: 3 minutes, no deck, then jury Q&A |
| Sun 18:00 | Winners announced |

Exact lock-in and submission times come through the organisers' WhatsApp group.

## What the jury scores

| Criterion | Our answer |
| --- | --- |
| Product | The deployed app: join, get matched, see why, meet for a coffee |
| Problem | Who struggles to meet the right person, and why today's networks fail them |
| Validation | Real conversations and sign-ups this weekend (LinkedIn post, people on site) |
| Speed & demo | A live demo that works, rehearsed to three minutes |

Saturday: the problem and a first working version. Sunday: proof that people want it, the demo and the pitch.

## Run it

```bash
git clone https://github.com/steffiAI/sammen.git
cd sammen
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash; on macOS/Linux: source venv/bin/activate
pip install uv
uv pip install -r requirements.txt
python -m sammen.seed             # invented demo profiles
python app.py                     # http://127.0.0.1:5000
python -m pytest                  # must pass before every push
```

### Turn on the AI (Mistral, European)

1. Redeem the hackathon credits and create an API key in [Mistral Studio](https://console.mistral.ai/) (code and steps are in the Mistral slides).
2. Copy `.env.example` to `.env` and paste the key after `MISTRAL_API_KEY=`. Never commit `.env`.
3. Restart the app.

| With a key | Model | Without a key |
| --- | --- | --- |
| Matching by meaning, not just shared words | Mistral Embed | Shared keywords |
| One sentence on why you two should meet | Mistral Small | Reasons list only |
| Safety check on profile text | Mistral Moderation | Skipped |

## How we work this weekend

1. **The demo path comes first.** Landing page → join → matches. Anything that is not on this path waits.
2. **`main` always runs.** Pull before you start, run the tests before you push. If `main` breaks, fixing it is everyone's top priority.
3. **Small steps, pushed often.** One issue, one short branch (`feat/short-name`), merged within the hour. No long-lived branches.
4. **The board is the plan.** Take an issue, assign yourself, move it to Done. If it is not on the board, it is not happening.
5. **Stop adding features two hours before code freeze.** After that: only fixes, demo rehearsal and the pitch.
6. **Deployed, with a safety net.** The jury wants a deployed MVP, not a repo. The app still runs locally on rule-based matching if the Wi-Fi or the API fails.
7. **Hackathon rules.** Only our team and the official mentors work on this. Everything in this repo was started after Saturday's kick-off.

Commit messages: `feat: add match page`, `fix: empty city crashed form`, `docs: update pitch`.

## Our principles

| Principle | What it means in this repo |
| --- | --- |
| Secure | No secrets in the repo (`.env` is ignored). Inputs are validated. We store only what a match needs. |
| European | No US-hosted services for user data. System fonts, no external scripts or trackers. AI runs on Mistral (France). |
| Real people | Verified badge, mutual interest required before two people see each other, bot trap on the join form. |
| Fictional demo data | Every profile in `sammen/seed.py` is invented. No real people's data in the repo. |

## Where things are

```
app.py                 web app (routes, form validation)
sammen/matching.py     who matches whom, and why
sammen/ai.py           Mistral: meaning-based matching, intros, safety check
sammen/db.py           SQLite storage (local file in data/)
sammen/seed.py         invented demo profiles
templates/, static/    pages and the one stylesheet
tests/                 smoke tests for matching and the join flow
docs/demo-checklist.md what must be ready before the demo
```

## Design

Copenhagen minimal: warm white, ink, one muted green, lots of space. All colours are variables at the top of `static/style.css`.
