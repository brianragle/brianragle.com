# Cross-posting pipeline — PLAN

Not implemented yet. This document describes the engine to build next.

## Goal

When Brian hands over a post for brianragle.com, that is automatic permission to publish it on the site AND cross-post it to all his socials + Substack, formatted per platform, with no per-post approval needed. (Standing authorization, 2026-09-26. Scope: the post he supplies — text, images, video links/blurbs. Never: DMs, replies, comments, follows, deletions, or anything beyond publishing that post. If a post looks like it was meant to stay private, check first.)

## Input

A post as defined in the main README (`posts/YYYY-MM-DD-slug.md` with frontmatter: title, date, type, excerpt, optional image / link_url / video_url). The pipeline runs after `build.py`, or as one `publish.py` command that builds, deploys, and cross-posts.

## Per-platform formatters

Each platform gets a formatter that takes the canonical post and returns platform-native content:

- **Bluesky** — short text + link. Use the Bluesky API (app password in secure storage). Link cards via the API's embed.
- **Mastodon** — short text + link, hashtags where natural. API is confirmed working (`@brianragle@mastodon.social`).
- **Threads** — short text + link. `threads-cli publish-post` works.
- **Facebook** — longer text + link and/or image. The facebook-cli is read-only for timelines, so this needs browser automation on his logged-in session (or his manual tap as fallback).
- **LinkedIn** — professional framing, link + image. Posting path TBD (browser automation likely).
- **Instagram** — image posts only: needs an image. When a post has an image, publish the image with a caption; when it doesn't, skip Instagram for that post (or pair with the site avatar only if Brian approves that pattern). Video posts go to Reels (see video flow).
- **Substack** — new posts publish to the "Brian Ragle" publication (`brianmragle.substack.com`) as newsletter posts/notes. Browser automation on the signed-in session, or the Substack API if a workable path is found.

Formatters handle: character limits (truncate with care, never mid-word; link always survives), image attach where supported, alt text carried through, and per-platform voice tweaks documented per formatter.

## Voice and formatting rules (standing, from Brian 2026-09-26)

- Distill, don't rewrite: the brianragle.com post as he wrote and approved it is the canonical text. Per-platform versions only condense for character/post limits — never rewrite, embellish, or add framing he didn't approve. Truncate with care, never mid-word; the link always survives.
- Minimal emojis. He is not a tween or millennial.
- His voice always: the Ragle voice rules apply to every platform version (`~/workspace/user/files/ragle-voice-prompt.md` — no em-dashes, no hedging, no rhetorical-question-plus-answer, dry and aimed at arguments).
- Abbreviate where necessary to fit constraints, but keep his wording wherever it fits.

## Video flow

Videos are posted directly to the video platforms; brianragle.com carries only a blurb + link, and that blurb is what cross-posts to the text platforms:

1. Video file lands in `posts/` (or a `media/` dir) alongside the blurb post.
2. Upload the file directly to **TikTok**, **Instagram Reels**, and **YouTube** (YouTube via API or browser; TikTok/Reels via browser automation on his sessions — both are bot-sensitive, expect manual fallback).
3. Collect the published URLs, write them into the post's frontmatter (`video_url`, plus per-platform URLs if useful), rebuild the site.
4. The blurb text + site link cross-posts to Bluesky/Mastodon/Threads/Facebook/LinkedIn/Substack as a normal text post.

## Friday digest job

Every Friday, a scheduled job:

1. Collects that week's posts from `posts/` (by date).
2. Drafts a roundup: one section per post (title, excerpt, link), grouped by type.
3. Publishes it to the "Brian Ragle" Substack publication as the weekly digest edition.
4. The homepage subscribe box (`https://brianmragle.substack.com/subscribe`) captures subscribers for it.

Digest goes out Fridays — confirmed with Brian 2026-09-26.

## Ordering and idempotency

- Publish order: site first (so every cross-post links a live URL), then Substack, then socials.
- Keep a `pipeline/state.json` log of what was posted where (post slug → platform → published URL / timestamp) so re-runs never double-post.
- Failures post partial results and report: which platforms succeeded, which need a retry or manual step. Never silently skip.

## Open questions for build time

- LinkedIn posting path (API vs browser).
- Substack post-creation path (API vs browser).
- Whether image-less posts should still hit Instagram (decision: skip unless Brian says otherwise).
- YouTube upload path for the video flow.
