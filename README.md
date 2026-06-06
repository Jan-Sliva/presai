# presai

Automated presentation generator, originally built for Geography and History homework. The LLM drafts structured slide content from a topic and focus description, then exports Markdown and PowerPoint.

Development started in a Jupyter notebook; the current direction is a **PyQt5 desktop app** with pluggable generation strategies.

## How it works

The **outline-first** pipeline (implemented in the notebook and partially ported to the GUI):

1. **Outline** — Ask Bing Chat for several JSON outlines (slide titles only), each with at least *N* slides. The user picks one.
2. **Slides** — Generate each slide separately as Markdown (`##` title + bullet points). Later slides receive the outline plus a rolling window of recently created slides so the model avoids repetition while staying within context limits.
3. **Post-process** — Strip Bing citation markers (`[^1^]`, `[link]`), optionally translate via DeepL, write `.md`.
4. **Export** — Fill a PowerPoint template with `python-pptx`, preserving bullet hierarchy (top-level vs. indented subpoints).
5. **Sources** — Collect Bing web-search URLs per slide into a companion `sources.txt`.

```
Topic + focus + parameters
        │
        ▼
  ┌─────────────┐     multiple attempts
  │   Outline   │ ──► JSON list of slide titles
  └─────────────┘
        │ user picks one
        ▼
  ┌─────────────┐     one Bing Chat call per slide
  │   Slides    │ ──► Markdown (## title, bullets)
  └─────────────┘
        │
        ├─► DeepL translation (optional, e.g. Czech)
        ├─► .md + .pptx + sources.txt
        └─► saved to output folder
```

## Key files

| What | Path |
|------|------|
| **Original development notebook** | [`notebooks/presai.ipynb`](notebooks/presai.ipynb) |
| **Notebook prompt templates** | [`notebooks/prompts.json`](notebooks/prompts.json) |
| **GUI strategy prompts** | [`src/strategies/outlineFirst/prompts/`](src/strategies/outlineFirst/prompts/) — [`outline.txt`](src/strategies/outlineFirst/prompts/outline.txt), [`firstSlide.txt`](src/strategies/outlineFirst/prompts/firstSlide.txt), [`otherSlide.txt`](src/strategies/outlineFirst/prompts/otherSlide.txt) |
| **Example output (Seven Years' War, Czech)** | [`notebooks/result/Sedmiletá válka IV.md`](notebooks/result/Sedmiletá%20válka%20IV.md) · [`notebooks/result/Sedmiletá válka IV.pptx`](notebooks/result/Sedmiletá%20válka%20IV.pptx) · [`notebooks/result/Sedmiletá válka IV sources.txt`](notebooks/result/Sedmiletá%20válka%20IV%20sources.txt) |

The example presentation covers the Seven Years' War across all major theatres (North America, Europe, India, Caribbean, Africa, Asia, South America) plus the Paris and Hubertusburg peace treaties — 10 slides, generated with the outline-first workflow.

## Technical details

### LLM backend: Bing Chat via EdgeGPT

Both the notebook and `src/BingChatAccess.py` talk to **Microsoft Bing Chat** through the [EdgeGPT](https://github.com/acheong08/EdgeGPT) library (`ConversationStyle.creative`). Each slide typically starts a **fresh conversation** (`newConv=True`) to avoid hitting the per-chat message cap (~10 turns).

The notebook layer adds **token budgeting** with `tiktoken`: before each request it estimates conversation size against a GPT-4 4 096-token window and reserves headroom for the expected response (`presaiUtils.num_tokens_from_messages`).

Failed requests are retried (default 5 attempts with 1 s backoff). Outline generation often needs several tries — Bing sometimes refuses structured JSON output on the first attempt.

### Prompt design

Prompts are plain text templates with Python `str.format` placeholders (`{top}`, `{foc}`, `{adj}`, `{len}`, `{pointsMin}`, `{pointsMax}`, …).

- **Outline prompt** — demands raw JSON only, no preamble: `{"slides": ["title 1", …]}`.
- **First slide prompt** — receives the full outline; asks for Markdown with `{pointsMin}–{pointsMax}` concise bullets.
- **Other slide prompt** — adds `{createdSlides}` (recent slides) and explicitly forbids repeating earlier content.

The notebook keeps all prompts in one JSON file; the GUI strategy splits them into separate `.txt` files under `src/strategies/outlineFirst/prompts/`.

### Translation and export

Non-English output uses the **DeepL API** (`deepl` Python package). A token file (`.DeepLtoken`, gitignored) is read at runtime. Slide titles and body text are translated after Markdown cleanup.

PowerPoint assembly uses **`python-pptx`** against a local `template.pptx` (title slide layout 0, content slides layout 1). Bullet nesting is mapped to paragraph levels; language IDs are set via `MSO_LANGUAGE_ID`.

### GUI architecture (work in progress)

```
src/main.py          → PyQt5 entry point
src/mainWindow.py    → strategy picker + parameter forms
src/selectionLayout.py → declarative form builder (text/number/selection inputs)
src/strategies/*/    → one folder per generation strategy
  strategy.py        → strategy class with begin() workflow
  info.json          → name + description shown in the picker
  prompts/           → prompt templates
```

Strategies are loaded dynamically with `importlib` — adding a new folder under `src/strategies/` with `info.json` + `strategy.py` registers it automatically.

The GUI currently implements the parameter screen and live prompt preview for the outline-first strategy; outline fetching and slide generation (`predictOutlines`) are still stubs.

### Notebook vs. `src/`

| | Notebook | GUI (`src/`) |
|---|----------|--------------|
| Bing access | `notebooks/BingChatAccess.py` (extends `ChatGPTlike`, token-aware) | `src/BingChatAccess.py` (async, implements `LLMChatAccess` ABC) |
| Prompts | `prompts.json` | per-strategy `.txt` files |
| Interface | Jupyter cells | PyQt5 forms |

## Running

**Notebook** (full pipeline):

```bash
cd notebooks
jupyter notebook presai.ipynb
```

Requires: `EdgeGPT`, `python-pptx`, `deepl`, `tiktoken`, and a `template.pptx` in the notebooks directory. For Czech output, create `.DeepLtoken` with your DeepL API key.

**GUI** (parameter selection only, for now):

```bash
cd src
python main.py
```

Requires: `PyQt5`.

## Project status

- Notebook pipeline: **working** — produces `.md`, `.pptx`, and `sources.txt` (see example in `notebooks/result/`).
- GUI: **early stage** — strategy selection and outline prompt preview; generation not yet wired up.
- Bing Chat / EdgeGPT: upstream APIs change frequently; the EdgeGPT project is archived — expect breakage over time.
