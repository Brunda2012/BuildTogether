# [App name] design system

Style guide for the mobile app. Follow it for every screen, component and state. Do not invent colors, fonts or spacing outside these tokens.

## 1. Audience and principles
Primary users: startup founders, entrepreneurs, individual contributors, project leads and investors.
- Nordic minimalism: quiet, uncluttered, honest materials. Every element earns its place.
- Warm, not cold: oat-toned neutrals, soft contrast, natural hues. Never stark white-and-blue "corporate".
- Clarity over decoration. Numbers, status and next actions come first.
- One primary action per screen.
- Scannable in under five seconds: founders and investors check on the go.
- Role-aware: ICs see tasks, leads see progress and risk, investors see metrics and trends. Same visual language for all.
- Generous whitespace. When in doubt, remove something.

## 2. Color (palette: Nordic Oat)
Default theme: light. Dark theme is fully supported and follows the system setting unless the user overrides it.

| Token | Light | Dark | Use |
|---|---|---|---|
| background | #F7F4EF | #1A1816 | Screen background (oat / warm charcoal) |
| surface | #FFFFFF | #242120 | Cards, sheets, inputs |
| surface-muted | #EFEAE2 | #2E2A27 | Chips, pressed states, tiles |
| border | #E6E0D6 | #38332E | Hairlines, dividers |
| text-primary | #26231F | #F2EEE8 | Headings, body |
| text-secondary | #7A736A | #A69E93 | Labels, metadata |
| primary | #3F5B73 | #A9C1D6 | Main buttons, active nav, links (fjord blue) |
| on-primary | #FFFFFF | #15191D | Text on primary |
| accent | #8A5A0B | #E0B25C | Due dates, highlights, charts (warm ochre) |
| success | #3F5B73 | #A9C1D6 | Done, positive change (shown with icon, never green) |
| warning | #8A5A0B | #E0B25C | At risk, due soon |
| danger | #B4442F | #E58B76 | Errors, negative change, destructive (brick) |

Rules:
- There is no green and no purple anywhere in the palette. Never use either for text, icons, chips or charts.
- Positive deltas: text-primary with an up-arrow icon. Negative deltas: danger color with a down-arrow icon. Done states use a check icon in the success (fjord) color.
- Due dates and deadlines use the ochre accent: ochre text on a 12% ochre tint chip. Overdue switches to danger.
- Primary is for one main action per screen. Use accent sparingly (under 10% of the screen).
- Never use color alone to convey status: pair it with an icon or label.
- Tinted backgrounds use the role color at 10% opacity (light) or 16% (dark).
- No gradients, no glows, no colored shadows.

## 3. Typography
Headings and body: Inter (system sans-serif fallback). Slightly tighter tracking on large sizes (-0.01em). Use tabular numbers for all metrics, currency and dates.

| Style | Size / line | Weight | Use |
|---|---|---|---|
| Display | 32 / 40 | 500 | Hero metric |
| Title | 24 / 32 | 500 | Screen title |
| Heading | 20 / 28 | 500 | Section title |
| Subheading | 17 / 24 | 500 | Card title |
| Body | 16 / 24 | 400 | Default text |
| Small | 14 / 20 | 400 | Secondary text |
| Caption | 12 / 16 | 400 | Metadata, chips |

Use only weights 400 and 500. Sentence case everywhere. Minimum size 12px.

## 4. Spacing and layout
- 4px base grid. Scale: 4, 8, 12, 16, 24, 32, 48, 64.
- Screen padding: 20px. Card padding: 16px. Gap between cards: 12px. Section spacing: 32px.
- List row minimum height: 56px. Touch targets at least 44 x 44px.
- One column. Left-aligned text. Avoid dense grids on mobile.
- Respect safe areas. Bottom nav height 64px plus safe-area inset.

## 5. Shape and elevation
- Buttons: 12px radius. Cards and sheets: 16px. Inputs: 12px. Chips: 8px. Avatars: circle.
- Flat by default: 0.5px border using the border token, no shadows on cards.
- Shadows only for floating layers (bottom sheets, menus): 0 8px 24px rgba(38,35,31,0.10).

## 6. Components
- Primary button: primary fill, on-primary text, 52px tall, full width on forms. One per screen.
- Secondary button: transparent, 1px border, text-primary.
- Ghost button: text only in primary color.
- Destructive: danger fill, always confirm.
- Card: surface fill, hairline border, 16px radius. Tappable cards darken to surface-muted when pressed.
- Metric card: caption label, Display number, delta as text-primary with arrow icon (danger color only when negative).
- Input: 52px tall, surface fill, border, 2px primary focus ring. Label above, helper or error below.
- Chip or badge: Caption text, surface-muted fill, text-secondary. Status chips use the role tint with role-colored text. Due date chip: ochre tint, ochre text, clock icon.
- List row: leading outline icon or avatar, title, secondary line, trailing chevron. Hairline separators, no card around each row.
- Bottom tab bar: 4 to 5 items. Plain outline icons, no tile or pill. Active icon and label use primary; inactive use text-secondary.
- Empty state: outline icon, one-line headline, one-line explanation, one action.
- Charts: primary first, ochre second, then neutrals (text-secondary, border). Direct labels over legends. Gridlines at 0.5px border color. No green or purple series.

## 7. Iconography
Outline icons, 1.5px stroke, rounded caps, 20px default (16 small, 24 large). Use one icon set (Lucide or Tabler). Icons are monochrome: text-secondary by default, primary when active.

## 8. Motion
- Duration: 150ms for taps and toggles, 250ms for sheets and transitions.
- Easing: ease-out for entering, ease-in for exiting.
- Animate opacity and transform only. Respect reduced-motion settings.
- Calm and subtle: no bounces or attention-seeking animation.

## 9. Voice and content
Direct, warm and understated. Verb-first buttons ("Create project", "Send update"). No exclamation marks in system copy. Errors say what happened and what to do next. Numbers use compact formats ($48.2k, 14.2 mo).

## 10. Accessibility
- Text contrast at least 4.5:1, large text and icons at least 3:1, in both themes.
- Visible focus states. Labels on every input and icon button.
- Support dynamic type up to 130% without clipping.

## 11. Design tokens (CSS variables)
```css
:root {
  --background: #F7F4EF;
  --surface: #FFFFFF;
  --surface-muted: #EFEAE2;
  --border: #E6E0D6;
  --text-primary: #26231F;
  --text-secondary: #7A736A;
  --primary: #3F5B73;
  --on-primary: #FFFFFF;
  --accent: #8A5A0B;
  --success: #3F5B73;
  --warning: #8A5A0B;
  --danger: #B4442F;
  --radius-button: 12px;
  --radius-card: 16px;
  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
}
.dark {
  --background: #1A1816;
  --surface: #242120;
  --surface-muted: #2E2A27;
  --border: #38332E;
  --text-primary: #F2EEE8;
  --text-secondary: #A69E93;
  --primary: #A9C1D6;
  --on-primary: #15191D;
  --accent: #E0B25C;
  --success: #A9C1D6;
  --warning: #E0B25C;
  --danger: #E58B76;
}
```

## 12. Instructions for the builder (Lovable)
- Read this file before generating or editing any UI. Map the tokens above into the Tailwind config and the shadcn theme variables.
- Never hard-code hex values in components. Use the semantic tokens.
- Never use green or purple (including Tailwind green-*, emerald-*, purple-*, violet-*, indigo-* classes) for any text, icon, chip or chart.
- Build mobile-first at 390px width, then scale up.
- Reuse the components in section 6 before creating new ones.
- When a request conflicts with this file, follow this file and say so.
