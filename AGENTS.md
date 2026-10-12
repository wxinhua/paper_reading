# Paper library maintenance

- This repository is the portable, public source of the reading website.
- Update Markdown notes, figures and `library.json`; HTML and `dist/` are generated.
- Preserve original paper versions, captions, evidence boundaries and citations. Being-M0.7 uses only the October 8, 2026 arXiv v1.
- Wholebody papers have one primary subcategory; related directions do not duplicate counts. Keep ICL-VLA separate.
- Run `python3 tools/build_site.py` after source changes. Fix broken local links before committing.
- Keep credentials, local Zotero metadata and local PDF archives outside this repository.
- Preserve the existing repository remote. Publication is controlled by the Pages workflow.

