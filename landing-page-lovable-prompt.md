# Sammen landing page: Lovable prompt

Replaces the earlier BuildTogether landing page prompt (22 Nov 2026).

**How to use it**

1. Open the Lovable project.
2. Attach three images in the Lovable chat, in this order: the pony drawing, the first Opera drawing, the sextant.
3. Paste the whole prompt below.
4. After it builds, submit one test sign-up on a phone, check it arrives in the `waitlist` table, then delete it.

**Open points for the team**

- Name: the page says Sammen. Change it in the prompt if we stay with BuildTogether.
- The cream, navy and orange look applies to the landing page only. The app screens keep their current design.
- No pricing and no "verified" or "stored in the EU" claims yet. Add them only if the app really does this.
- The "Why now" section uses the Basel and Germany points without names. Names go in only after the people agreed to be quoted.

## Prompt

```text
Build a public landing page at "/" for Sammen. Keep the existing app and its routes unchanged; move the current start screen to "/app" if it sits at "/".

GOAL
Two audiences sign up for early access: investors and founders-to-be. Every section must help one of them decide to sign up. Investors come first.

LOOK (Danish editorial, calm, lots of empty space)
- Background cream #F6F1E7. Text and lines navy #1B2A4A. One accent only: orange #E8762B (darker #B5541A for small orange text). Secondary text #5B6577.
- Font: Inter. Headlines weight 300, large, letter-spacing -0.02em. Body 400. Small labels 500, uppercase, letter-spacing 0.25em.
- Thin navy hairlines (20% opacity) to separate rows. No cards, no boxes, no shadows, no gradients, no rounded pills, no emojis, no icons.
- Orange appears only on: the primary button, one key phrase per section, and the active form option.
- Images: use only the three attached drawings. Do not generate, draw or add any other image, illustration or stock photo. If an image is missing, leave the space empty.
- Mobile first. Buttons at least 48px high. Fast: no animation libraries, only a gentle fade-in on scroll.

SECTION 1: HERO
Label: SAMMEN
Headline: "Meet the next unicorn founder before they found."
Sub-line: "Sammen spots founders-to-be by early signals and brings them to the right investor at the right moment. Over a coffee."
Two buttons side by side: "I invest" (orange, filled) and "I'm building" (navy outline). Each scrolls to the sign-up form with that role preselected.
Small line below: "Starting with robotics, defence and dual-use, AI and biotech. Built in Europe."
Right side (below on mobile): attached image 1, the pony drawing, blending into the cream background.

SECTION 2: THE PROBLEM
Label: THE PROBLEM
Headline: "Investors meet the best founders two weeks too late."
Three rows with hairlines, left a short term, right one sentence:
- Before | No company yet, so there is nothing to find.
- The window (this row in orange) | Someone leaves a job, a PhD or a contract.
- Two weeks later | Five other investors have had the coffee.

SECTION 3: THE SIGNALS
Label: THE INSIGHT
Headline: "Founders-to-be can be spotted before they found."
Four rows with hairlines:
- Has built before | Side projects, GitHub, hackathon wins
- Deep expertise | Years of work, often in research
- Non-linear path | Changed country, field or track
- Just became available | Left a job, a PhD or a contract
Beside the rows: attached image 3, the sextant.

SECTION 4: WHY NOW
Label: WHY NOW
Headline: "The talent is available. The buildings are waiting."
Three rows with hairlines, left a short term, right one sentence:
- Basel | Pharma is cutting hundreds of jobs. Experienced people are learning to build companies.
- Germany | Few natural resources. Big, beautiful buildings with room for many more founders.
- Sammen (this row in orange) | We bring the people and the capital together, at the right moment.
Below the rows, one large light line: "Sammen means together. Let's fill these buildings with life."

SECTION 5: HOW IT WORKS
Label: THE PRODUCT
Headline: "Spot. Invite. Meet."
Three columns separated by hairlines, numbered 1 to 3 in orange:
1. Spot | We read early signals in the fields you choose.
2. Invite | You both say yes before anyone is introduced.
3. Meet | A 20-minute coffee, in person or on video.
Full-width below: attached image 2, the Opera drawing, with the caption "Different boats, same water."

SECTION 6: TWO SIDES
Two columns separated by one vertical hairline (stacked on mobile).
Left, label FOR INVESTORS, headline "See them first.":
- Founders-to-be in your sectors, before a company exists
- A clear reason for every match
- No cold inbound, only mutual interest
Button: "Get early access" (role Investor preselected)
Right, label FOR FOUNDERS-TO-BE, headline "Be seen at the right moment.":
- No pitch deck needed, your path is the signal
- Investors who back your field
- You decide who gets to meet you
Button: "Join as a founder" (role Founder-to-be preselected)

SECTION 7: SECTORS
Label: WHERE WE START
One line of large light text, separated by thin dots: "Robotics and physical AI · Defence and dual-use · AI · Biotech and deep tech"
Sub-line: "Tell us your field when you sign up. We open sector by sector."

SECTION 8: SIGN-UP (id "join")
Headline: "Be among the first."
A short form, one column:
1. "I am..." tappable options: Investor / Founder-to-be / Something else
2. "My fields" multi-select, tappable: Robotics and physical AI / Defence and dual-use / AI / Biotech and deep tech / Climate / Other
3. Email (required)
4. City (optional)
Button: "Request early access" (orange)
Line under the button: "No spam. Used only to invite you."
After submit, replace the form with: "Thank you. We will be in touch personally."
Store in a new table "waitlist" (role, fields, email, city, created_at). Row-level security: visitors can only insert, nobody can read publicly. Validate email on the server, limit input lengths, add a hidden honeypot field.

SECTION 9: CLOSING AND FOOTER
Large light headline: "The next unicorn is already out there." Second line in orange: "Let's find it. Together."
Footer, small: "Sammen. Build together. By Steffi, Brunda and Bori at Women Build AI, Copenhagen, November 2026." Links: Privacy, Imprint.

RULES
No testimonials, no logos of other companies, no user counters, no invented numbers or quotes. No tracking scripts, no external embeds. Page title: "Sammen: meet founders before they found". Meta description: "Sammen spots founders-to-be by early signals and brings them to the right investor at the right moment."
```
