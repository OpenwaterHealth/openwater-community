# Community Garden Chronicle — Content Source

This folder is the source of truth for each weekly Community Garden Chronicle issue.

## Simple weekly workflow

1. Copy `_template.md`.
2. Rename it using `YYYY-MM-DD-issue-NNN.md`.
3. Fill in the front matter at the top.
4. Write only the sections that have meaningful updates.
5. Open a pull request for review.
6. After approval, merge to `main`.

A later build step will turn these Markdown files into:
- the Chronicle website/archive under `/chronicle/`
- the RSS feed used by HubSpot

## File naming

Example:

`2026-08-28-issue-001.md`

Use a three-digit issue number so files sort cleanly.

## Required front matter

- `issue`
- `date`
- `title`
- `subject`
- `summary`
- `status`
- `hero_image`

Use `status: draft` while editing. Change it to `published` only when the issue is ready to appear on the public site and RSS feed.

## Editorial rule

Public by default. Do not put confidential, regulatory-sensitive, customer-sensitive, unreleased commercial, or internal personnel information in Chronicle files.

Internal-only material belongs outside this public repository.
