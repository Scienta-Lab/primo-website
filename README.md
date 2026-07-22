# PRIMO website

Public website for **PRIMO**, an open benchmark initiative evaluating whether omics AI helps develop drugs—from target discovery to the clinic.

## Local preview

No build step is required.

```bash
python3 -m http.server 4173
```

Open <http://localhost:4173>.

## Validation

```bash
python3 tests/check_site.py
```

The check validates required files, internal asset references, document landmarks, link safety, and placeholder behavior.

## Deployment

Pushes to `main` deploy automatically to GitHub Pages through `.github/workflows/pages.yml`.

Temporary project URL: <https://scienta-lab.github.io/primo-website/>

## Resources

- [PRIMO ICLR 2026 LMRL publication](https://openreview.net/forum?id=v2SA8gHwqo)
- GitHub benchmark repository: coming soon
- Hugging Face benchmark and leaderboard: coming soon

## Content and licensing

Copyright © Scienta Lab and PRIMO contributors. Licensing for website content, brand assets, and source code will be finalized with the PRIMO governance and repository transfer. No license is granted by default.
