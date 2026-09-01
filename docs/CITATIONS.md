<!-- This document is mirrored from the root [CITATIONS.md](../CITATIONS.md). -->
<!-- The canonical version lives in the repository root. -->

# Citations

## How to Cite Fed-Dup

If you use Fed-Dup in academic research, a blog post, a talk, or any other
context where attribution is appropriate, we appreciate a citation. Below are
suggested citation formats.

---

## BibTeX

```bibtex
@software{feddup,
  title        = {Fed-Dup: Federated Repository Duplication Engine},
  author       = {{Fed-Dup Contributors}},
  year         = {2025},
  version      = {1.0.0},
  url          = {https://github.com/feddup/fed-dup},
  license      = {MIT}
}
```

### With a specific version tag

```bibtex
@software{feddup_v1_0_0,
  title        = {Fed-Dup: Federated Repository Duplication Engine},
  author       = {{Fed-Dup Contributors}},
  year         = {2025},
  month        = sep,
  version      = {1.0.0},
  url          = {https://github.com/feddup/fed-dup/releases/tag/v1.0.0},
  license      = {MIT}
}
```

---

## APA (7th Edition)

> Fed-Dup Contributors. (2025). *Fed-Dup: Federated repository duplication
> engine* (Version 1.0.0) [Computer software]. MIT License.
> <https://github.com/feddup/fed-dup>

---

## Chicago (Author-Date)

> Fed-Dup Contributors. 2025. *Fed-Dup: Federated Repository Duplication
> Engine.* Version 1.0.0. <https://github.com/feddup/fed-dup>.

---

## IEEE

> Fed-Dup Contributors, "Fed-Dup: Federated Repository Duplication Engine,"
> version 1.0.0, 2025. [Online]. Available:
> <https://github.com/feddup/fed-dup>

---

## Plain Text / Markdown

> Fed-Dup — Federated Repository Duplication Engine. Fed-Dup Contributors,
> 2025. Version 1.0.0. MIT License. <https://github.com/feddup/fed-dup>

---

## RST (reStructuredText)

```rst
Fed-Dup Contributors. *Fed-Dup: Federated Repository Duplication Engine*.
Version 1.0.0. 2025. MIT License.
https://github.com/feddup/fed-dup
```

---

## Citation Principles

- **Version matters:** Always cite the specific version you used (e.g.,
  `v1.0.0`), as behavior may change between releases. Find your version with
  `python -c "import feddup; print(feddup.__version__)"`.
- **URL:** Cite the GitHub repository URL or the specific release URL.
- **License:** Include the license (MIT) in software citations per best
  practice ([Software Citation Principles](https://force11.org/info/software-citation-principles/),
  FORCE11).
- **Authors:** Use "Fed-Dup Contributors" as the collective author. If you
  need to cite a specific individual, see [AUTHORS.md](AUTHORS.md) and use
  their name with a note that they are a Fed-Dup contributor.

---

## Zenodo DOI

If a Zenodo DOI is registered for Fed-Dup (via GitHub's Zenodo integration),
each release receives a unique DOI. Cite the DOI for the specific version you
used:

```bibtex
@software{feddup_zenodo,
  title        = {Fed-Dup: Federated Repository Duplication Engine},
  author       = {{Fed-Dup Contributors}},
  year         = {2025},
  version      = {1.0.0},
  doi          = {10.5281/zenodo.XXXXXXX},
  url          = {https://doi.org/10.5281/zenodo.XXXXXXX},
  license      = {MIT}
}
```

> Replace `XXXXXXX` with the actual Zenodo DOI once registered. Check the
> repository README or Zenodo record for the current DOI.

---

## Related Work

If your work builds on or relates to Fed-Dup's approach (database-free Git
mirroring, token-safe sync, etc.), consider also citing:

- The [Git documentation](https://git-scm.com/doc) for the `--mirror` clone
  and push semantics.
- The [Streamlit](https://streamlit.io/) framework for the web UI approach.
- The [FORCE11 Software Citation Principles](https://force11.org/info/software-citation-principles/)
  for software citation methodology.

---

## Contact

Questions about citing Fed-Dup? Open a
[GitHub Discussion](https://github.com/feddup/fed-dup/discussions).
