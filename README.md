# brianragle.com

The hub site for Brian Ragle — local reporter covering Tennessee's Upper Cumberland. The site is the clearinghouse: posts publish here first, then cross-post out to every social platform and Substack (see `pipeline/`).

Static site. No frameworks, no JavaScript frameworks, no trackers, no external requests at runtime. Fonts and images are self-hosted under `assets/`.

## Layout

```
brianragle.com/
├── build.py            # static site generator (Jinja2 + Markdown)
├── posts/              # Markdown posts with YAML frontmatter
├── templates/          # base, home, post, archive, about
├── assets/
│   ├── css/style.css   # hand-written, brand palette
│   ├── img/            # wordmarks, hero, avatar (from the brand kit)
│   └── fonts/          # Inter Tight + Newsreader, self-hosted
├── pipeline/           # cross-posting engine (plan only for now)
└── dist/               # built site (generated, not committed)
```

## Adding a post

Create a Markdown file in `posts/` named `YYYY-MM-DD-slug.md`:

```markdown
---
title: "Post title"
date: 2026-09-26
type: blurb        # article | blurb | link | video
excerpt: "One or two sentences shown on the homepage and archive."
image: "assets/img/some-photo.jpg"   # optional
link_url: "https://..."              # for type: link
video_url: "https://..."             # for type: video
---

Body text in Markdown.
```

Post types:

- **article** — a short article, full body on its own page.
- **blurb** — a few sentences, an observation, a note from the field.
- **link** — points at something elsewhere (a new Medium article, an interesting story). `link_url` gets its own card.
- **video** — a blurb that points at a video. The video file goes directly to TikTok / Instagram Reels / YouTube; the post links to it via `video_url`, and the blurb text is what cross-posts to text platforms.

## Building

```bash
python3 build.py
```

Reads `posts/*.md`, renders templates into `dist/`. Requires `jinja2`, `pyyaml`, and `markdown` (`pip install jinja2 pyyaml markdown`).

## Deploy

`dist/` is deployed to IONOS hosting (Deploy Now from this repo's `main` branch builds and publishes `dist/`).

## Brand

Palette and typography follow the brand guide (`BRAND-GUIDE.md` in the Brian Ragle Website workspace on Brian's Mac): Coal `#14110B` page ground, Iron `#221D14` cards, Bone `#EAE2D0` text, Stone `#8A8172` secondary, Ember `#C47B34` accents and links only (never backgrounds), Paper `#F3EDE0` for light applications only. Inter Tight leads on the hub; Newsreader is reserved for pull quotes and the Ragle Reports imprint. No gradients, no icon sets, no stock tech imagery.
