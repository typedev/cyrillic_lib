# Maintaining the Cyrillic Languages project

This document is for **maintainers and operators** — the people who review contributor Pull Requests, run the compilation pipeline, regenerate the site artifacts, and keep the supporting configuration in order. It is not written for external contributors; the contributor-facing guide is [CONTRIBUTING.md](../CONTRIBUTING.md) / [CONTRIBUTING-RU.md](../CONTRIBUTING-RU.md).

The document covers the Cyrillic build as the primary workflow, and includes a dedicated section on the Latin-script tree, which is an internal work-in-progress kept in the same repository but not open for external contributions.

## Contents

1. [Prerequisites](#prerequisites)
2. [Running the pipeline](#running-the-pipeline)
3. [Reviewing and merging a contributor PR](#reviewing-and-merging-a-contributor-pr)
4. [Repository layout — operator view](#repository-layout--operator-view)
5. [The language registry (`cyrillic_library.json`)](#the-language-registry-cyrillic_libraryjson)
6. [Glyph categories (`glyphs_list_categories.json`)](#glyph-categories-glyphs_list_categoriesjson)
7. [Pipeline config (`languages.json`)](#pipeline-config-languagesjson)
8. [The sort order table (`sortorder_cyrillic.txt`)](#the-sort-order-table-sortorder_cyrillictxt)
9. [Unicode description tables](#unicode-description-tables)
10. [Locales](#locales)
11. [Utility scripts](#utility-scripts)
12. [Dump / reload round-trip for language descriptions](#dump--reload-round-trip-for-language-descriptions)
13. [The legacy folder](#the-legacy-folder)
14. [Latin script (experimental, WIP)](#latin-script-experimental-wip)
15. [Known limitations and TODOs](#known-limitations-and-todos)
16. [Contact](#contact)

---

## Prerequisites

The main pipeline (`compile_languages.py`) uses **only the Python 3 standard library** — no third-party dependencies. Any reasonably recent Python 3 interpreter works. Verify:

```bash
python3 --version
```

A couple of the utility scripts (see [Utility scripts](#utility-scripts)) have additional requirements or hardcoded paths; those are noted per-script.

## Running the pipeline

All scripts run from `cyrillic-languages/scripts/`. The primary entry point is `compile_languages.py`. It reads `../languages.json` to discover which scripts (cyrillic, latin) to build and which per-script configuration to use.

### Full rebuild

```bash
cd cyrillic-languages/scripts
python3 compile_languages.py
```

This regenerates everything: per-language JSON files under `../site/cyrillic/base/` and `../site/latin/base/`, and the pan-script summary files `../site/cyrillic/cyrillic_characters_lib.json` and `../site/latin/latin_characters_lib.json`.

### Rebuild a single script

```bash
python3 compile_languages.py -s cyrillic
python3 compile_languages.py -s latin
```

### Rebuild only specific languages

```bash
python3 compile_languages.py -s cyrillic -n Avar Azeri
```

Names must match the `name_eng` field of the source file. The `-n` list is passed straight through; when a name contains spaces or parentheses, quote it:

```bash
python3 compile_languages.py -s cyrillic -n "Altaic (Oirot)" "Eskimo (Yupik)"
```

Note: `-n` only controls *per-language regeneration*. The pan-script summary (`cyrillic_characters_lib.json`) is always rebuilt from **every enabled** language, so running `-n Avar` is enough to refresh Avar's per-language file but the pan-script summary will still include all languages.

### Output indentation

Near the top of `compile_languages.py`:

```python
DEVELOPMENT = True
```

When `True`, JSON files are written with `indent=4` (pretty). When `False`, output is minified. Leave it at `True` for development; consider flipping it off only if you're explicitly optimizing artifact size for production deployment.

### Outputs to inspect after a rebuild

- `cyrillic-languages/site/cyrillic/base/<Language>.json` — per-language result
- `cyrillic-languages/site/cyrillic/cyrillic_characters_lib.json` — pan-Cyrillic summary
- Same under `site/latin/` for the Latin tree
- Console messages — the pipeline prints warnings such as `*** Unicode not in SortOrder, added to the end of the list …` (see [The sort order table](#the-sort-order-table-sortorder_cyrillictxt)) and `*** Extended glyph: …` for certain multi-unicode tokens

Skim the console output after every run. Warnings are informative but often flag a missing sort-order entry or a malformed token that should be fixed at the source.

## Reviewing and merging a contributor PR

Contributor PRs should only modify files under `cyrillic-languages/library/cyrillic/base/`. The operator workflow after approving a contributor's change:

1. **Read the PR diff.** Verify nothing is touched outside the contributor-editable paths listed in the root [README.md](../README.md#repository-map).
2. **Sanity-check the source JSON.** Required fields present, `name_eng` matches the filename, `local` is a valid value, glyph tokens use only live markers (see [CONTRIBUTING.md — Glyph markers](../CONTRIBUTING.md#glyph-markers--live-reference) and [Known limitations](#known-limitations-and-todos) for dead/trap markers).
3. **If a new character was added**, verify its codepoint is present in `cyrillic-languages/library/cyrillic/sortorder_cyrillic.txt`. If not, add an entry before regenerating (see [The sort order table](#the-sort-order-table-sortorder_cyrillictxt)).
4. **Merge** the contributor's PR.
5. **Regenerate** on `master`:
   ```bash
   cd cyrillic-languages/scripts
   python3 compile_languages.py -s cyrillic
   ```
6. **Review the regenerated site files** under `cyrillic-languages/site/cyrillic/` with `git diff`. Check that the diff matches the intent of the contributor's change (no surprise mass-edits; no dropped glyphs).
7. **Commit** the regenerated artifacts in a follow-up commit on `master` with a message that references the contributor PR (e.g. `regenerate site for #<PR number>`).

There is currently no pre-merge CI validator (see [Known limitations](#known-limitations-and-todos)); these checks are done by eye.

## Repository layout — operator view

Everything lives under `cyrillic-languages/`. The subtrees, grouped by role:

**Data sources (edited by contributors)**

- `library/cyrillic/base/<Language>.json` — per-language hand-edited sources. This is the only tree contributors ever touch.

**Data configuration (operator-only)**

- `library/cyrillic/cyrillic_library.json` — registry of languages, with `enable` flag and internal `code_pt` values.
- `library/cyrillic/sortorder_cyrillic.txt` — pan-Cyrillic sort order.
- `languages.json` — top-level pipeline config: which scripts to build, and the per-script config file names.
- `locales.json` — mapping of OT-locale tags to human-readable language names. (See [Locales](#locales) for the caveat.)
- `glyphs_list_categories.json` — block-type titles and `show_unicodes` flags.

**Reference tables (operator-only)**

- `unicode14.txt` — upstream Unicode character descriptions. Bundled copy of the Unicode Character Database name list.
- `PT_PUA_unicodes.txt`, `PT_PUA_unicodes-descritions.txt` — descriptions for the Private Use Area codepoints that the Paratype fonts map to specific glyphs.

**Pipeline**

- `scripts/compile_languages.py` — the only script that must work correctly at any time. See [Running the pipeline](#running-the-pipeline).
- `scripts/<other .py>` — helper and one-shot scripts in various states of decay. See [Utility scripts](#utility-scripts).

**Generated artifacts (operator commits, never hand-edit)**

- `site/cyrillic/base/<Language>.json` — generated from the source files
- `site/cyrillic/cyrillic_characters_lib.json` — pan-script summary

**Site engine (operator-only; separate concern)**

- `static/`, `fonts/`, `index.html`, `asset-manifest.json`, `favicon.ico`, `robots.txt` — the compiled React site bundle that is served at <https://paratype.github.io/cyrillic-languages/>. The site fetches JSON from the `site/` tree above via `raw.githubusercontent.com` URLs; those URLs are baked into the compiled bundle and will need updating if this repository ever moves.

**Legacy**

- `library/cyrillic/_legacy/` — archived Russian historical-alphabet files; see [The legacy folder](#the-legacy-folder).

**Latin tree (experimental)**

- `library/latin/`, `site/latin/` — mirror structure for Latin-script languages. See [Latin script](#latin-script-experimental-wip).

## The language registry (`cyrillic_library.json`)

Shape:

```json
[
    {
        "name_eng": "Abazin",
        "name_rus": "Абазинский",
        "code_pt": "1",
        "enable": true
    },
    ...
]
```

### Fields

- `name_eng` — must match the filename of the source JSON (minus `.json`) and the `name_eng` field inside it.
- `name_rus` — Russian display name. Used by the site UI.
- `code_pt` — an internal Paratype identifier. Most Latin-tree entries and new Cyrillic entries carry a placeholder `"1"`; assign a real value when one is provided by Paratype.
- `enable` — boolean. When `false`, the pipeline silently skips this language; its source file is kept but not processed and no output is emitted. All entries currently are `true`; `false` is useful for temporarily parking a language pending revision.

### Registering a new language

1. Place the source file at `library/cyrillic/base/<Language>.json`.
2. Append a new entry to `cyrillic_library.json` with `enable: true` and a real `code_pt` (or `"1"` placeholder pending assignment).
3. Run the pipeline and commit the results.

### Invariants

- One registry entry per source file, and one source file per registry entry. Orphans on either side are a mistake (except for the contents of `_legacy/`, which is intentional — see [The legacy folder](#the-legacy-folder)).

## Glyph categories (`glyphs_list_categories.json`)

Defines the `type` values that may appear on a `glyphs_list[*].type` and attaches display metadata:

```json
{
    "type": "extended",
    "show_unicodes": false,
    "title": "Extended Orphographic Notation"
}
```

`show_unicodes` controls whether the site UI shows codepoint numbers next to glyphs in that section. `charset` (the pan-script flat view) is the only block type whose `show_unicodes` is true.

Adding a new category: append a new entry here, then use its `type` value in one or more source files. The pipeline reads this file by `type` name.

Current inventory (April 2026): `alphabet`, `charset`, `dialect`, `historic`, `extended`, `digraph`, `consideration`, `foreign`. Of those, `charset` is synthesized by the pipeline and must not appear in source files; `digraph` is defined but currently unused in any source — digraphs are instead marked inline with the `:` marker.

## Pipeline config (`languages.json`)

Root-level config that drives `compile_languages.py`:

```json
[
    {
        "script": "cyrillic",
        "name_eng": "Cyrillic",
        "name_rus": "Кириллица",
        "enable": true,
        "local_default": "ru",
        "list_of_languages": "cyrillic_library.json",
        "sort_order": "sortorder_cyrillic.txt",
        "glyphs_library": "cyrillic_characters_lib.json"
    },
    { "script": "latin", ... }
]
```

- `script` — subdirectory name under `library/` and `site/`.
- `enable` — whether the pipeline builds this script at all. Set to `false` to skip the whole latin tree during a cyrillic-only build iteration, for example.
- `local_default` — the locale tag used as fallback for glyphs without an explicit `local` override.
- `list_of_languages`, `sort_order`, `glyphs_library` — filenames that the pipeline resolves under `library/{script}/`.

## The sort order table (`sortorder_cyrillic.txt`)

A plain text file that defines the canonical glyph order for the pan-Cyrillic character set. Each non-comment line has the form:

```
<UpperCh>=<UpperCP>/<LowerCh>=<LowerCP>
```

— where `UpperCh`/`LowerCh` are the characters (used for human reading only; the pipeline ignores them and sorts by codepoint) and `UpperCP`/`LowerCP` are the hex Unicode codepoints. Either half can be omitted if the character has no case pair. Comments start with `#`.

Example:

```
А=0410/а=0430
Ӕ=04D4/ӕ=04D5
Б=0411/б=0431
```

### Locale duplication

The pipeline internally expands each codepoint with a set of locale suffixes (`''`, `.ru`, `.ba`, `.bg`, `.cv`, `.sr`, `.en`). This is how localized forms land at the same sort position as their unlocalized parents. **The locale list is hardcoded in the Python source** (see [Locales](#locales) for the caveat).

### Missing-codepoint behavior

When `compile_languages.py` encounters a codepoint in a source file that is not present in `sortorder_cyrillic.txt`, it prints:

```
*** Unicode not in SortOrder, added to the end of the list  <codepoint>
```

…and appends the glyph at the end of the sorted list. The pipeline does not fail. This is the main reason to re-read console output after every run: orphan codepoints at the end of the pan-script table almost always indicate a missing sort-order entry.

### Adding a new entry

Find the right alphabetical position, add a single line. The pipeline picks it up on the next run.

## Unicode description tables

Descriptions shown in the generated per-language JSONs come from two files, both loaded by `CharacherDescription.loadUnicodeDescriptionsFile()`:

- `unicode14.txt` — a dump of the Unicode 14 character database name list. First tab-separated field is the codepoint, second is the name. Updating this file means dropping in a refreshed export from the Unicode Consortium.
- `PT_PUA_unicodes-descritions.txt` — descriptions for Private Use Area codepoints that the Paratype fonts map to specific glyphs. Same format as `unicode14.txt`. This file is Paratype-curated — when a new PUA codepoint is assigned in the fonts, its description should be added here.

The supplementary `PT_PUA_unicodes.txt` is not read by `compile_languages.py` and appears to be kept for reference.

When both files define the same codepoint, the pipeline prints `Unicodes overlap:` and keeps the first entry it saw. If you see this on a run, it means `PT_PUA_unicodes-descritions.txt` has drifted into an official Unicode range or vice versa — investigate rather than ignoring.

Description handling trims tabs and converts double quotes to single quotes (`CharacherDescription.dangersymbols`) and title-cases the result.

## Locales

### Current values

Cyrillic locales in use: `ru` (default), `ba` (Bashkir), `bg` (Bulgarian), `cv` (Chuvash), `sr` (Serbian). Latin: `en`.

`locales.json` is a tiny lookup table of locale-tag → human-readable name, consumed mainly by the React site for UI labeling.

### Known limitation — hardcoded locale list

The pipeline itself does not read `locales.json` when expanding the sort-order table; instead, it uses a hardcoded list in `compile_languages.py`:

```python
locales = ['', '.ru', '.ba', '.bg', '.cv', '.sr', '.en']
```

This is a legacy shortcut that was never tidied up. Adding a new locale today therefore requires editing three files in lockstep:

1. Add the locale tag and label to `locales.json`.
2. Add the `.<tag>` suffix to the `locales` list in `laguagesOrderSorter.__init__` inside `compile_languages.py`.
3. Add the new `local` value to the set of acceptable values that contributors may use (reflected in `CONTRIBUTING.md`).

**TODO:** make `compile_languages.py` derive its locale list from `locales.json`, and drop the hardcoded list. Tracked in [Known limitations](#known-limitations-and-todos).

## Utility scripts

Everything below `scripts/` other than `compile_languages.py`. Ordered by "relevant now" → "semi-archived".

### `compile_languages.py`

The main pipeline. See [Running the pipeline](#running-the-pipeline).

### `dumpLangDescriptions.py`

Dumps every language's textual metadata (`name_eng`, `name_rus`, `language_group_rus`, `alt_names_eng`, `description_eng`, `description_rus`) into a single markdown-ish text file. Intended as an intermediate format when you want to edit descriptions in bulk in a text editor.

**Hardcoded paths.** The current file has absolute paths to `/Users/alexander/WORKS/PythonWorks/...`. Before running it on a different machine, rewrite the `workpath` and `codeslangfile` constants to use paths relative to the script (see `reloadDescriptions.py` and `makeLatinLib.py` for the pattern). As currently written it targets the **Latin** base; to dump Cyrillic descriptions, change the path.

### `reloadDescriptions.py`

The inverse of `dumpLangDescriptions.py`: reads the markdown-ish text file and writes each language's `language_group_rus`, `alt_names_eng`, `description_eng`, and `description_rus` back into the corresponding `library/latin/base/<name>.json`. Operates on the Latin tree by default; set `applyChanges = False` to dry-run.

### `makeLatinLib.py`

Bootstraps the entire Latin tree from `latin_languages.txt`: creates one `library/latin/base/<Name>.json` per language and rewrites `library/latin/latin_library.json`. Run only when rebuilding the Latin library from scratch.

### `recode_basejson.py`, `recode_cyrlib.py`, `recode_mainlibfile.py`

One-shot migrations from earlier schema generations. Kept as reference for how the data reached its current shape; they are not part of any recurring workflow.

- `recode_basejson.py` — split the old `uppercase_alphabet_adds` / `lowercase_alphabet_adds` blobs into separate `uppercase_dialect`, `uppercase_historic`, `uppercase_lexic` keys.
- `recode_cyrlib.py` — migrated those flat keys into the modern `glyphs_list` structure. The two files still in `library/cyrillic/_legacy/` pre-date even this step and were never migrated.
- `recode_mainlibfile.py` — set `enable: true` on every entry in `cyrillic_library.json`. Paths are hardcoded to `/Users/alexander/GitHub/PythonWorks/...`.

If you need to run one of these, re-read it first — paths and assumptions rarely match the current layout.

### `checkLanguageUFO.py`

Cross-checks the glyph sets declared in the Cyrillic sources against actual UFO font files. Requires the `fontParts` third-party package (not installed by default). Outside the recurring pipeline; useful when validating a new font release against the language data.

### `testPanCharSet.py`, `testSorting.py`

Small diagnostic dumps — `testPanCharSet.py` lists all glyph types encountered across the generated site files; `testSorting.py` is a throwaway script that compares Python's default sort of a Dagestan-language alphabet against an expected order.

### `make_charlib.py` — obsolete, do not run

Early sketch that imports `CyrillicOrderSorter` from `PTLangLib`. That class is fully commented out in the current `PTLangLib.py`, so the import will fail. Kept for historical reference only.

### `PTLangLib.py`

A helper module. Most of it is commented out. The surviving `CharacherDescription` class is nearly identical to the one inlined in `compile_languages.py`; don't rely on this module for new code.

## Dump / reload round-trip for language descriptions

When you need to edit descriptions for many languages at once, the workflow is:

1. Adjust the hardcoded paths in `dumpLangDescriptions.py` so it points at the right tree (cyrillic or latin) and the right input file.
2. Run it:
   ```bash
   cd cyrillic-languages/scripts
   python3 dumpLangDescriptions.py > /dev/null
   ```
   This produces `output.txt` next to `cyrillic_library.json` (or the latin variant, depending on your path edits).
3. Edit `output.txt` in a text editor. The format uses markers:
   - `#### <name_eng>` — starts a language block
   - `### Языковые группы` / `### Language groups` — delimit the two language-group lists
   - `## Латинские названия` — starts the `alt_names_eng` list
   - `# description english` / `# description russian` — start the two description fields, terminated by a blank line
4. Adjust the `descriptionsfile` constant at the top of `reloadDescriptions.py` to point at your edited file, and make sure `applyChanges = True`.
5. Run it:
   ```bash
   python3 reloadDescriptions.py
   ```

`reloadDescriptions.py` is currently hardwired for the Latin tree. For the Cyrillic tree, either rewrite the `libraryPath` construction to use `library/cyrillic/base` instead of `library/latin/base`, or (safer) copy the script into a new `reloadDescriptions_cyrillic.py` with the correct paths and run that.

Either way, the round-trip preserves `name_eng`, `name_rus`, `local`, `language_group_rus`, `alt_names_eng`, `description_eng`, `description_rus`, and the `glyphs_list`. It does not preserve anything outside those fields.

## The legacy folder

Path: `cyrillic-languages/library/cyrillic/_legacy/`.

Contents: three Russian historical-alphabet files that are not referenced by `cyrillic_library.json` and therefore not processed by the pipeline:

- `Russian Ancient (XVIII).json` — legacy schema (flat `uppercase_alphabet` / `lowercase_alphabet` / `uppercase_dialect` / … keys; no `glyphs_list`). Would need migration through something like `recode_cyrlib.py` before it could be re-enabled.
- `Russian Church (X-XVII).json` — same legacy schema.
- `Russian Old (XIX).json` — modern schema (has `glyphs_list`), simply not registered in the index.

See the folder's own `README.md` for the explanation visible to casual readers.

Options, should you decide to act on them:

- **Retire** — delete the folder if these historical alphabets are permanently out of scope.
- **Migrate and re-enable** — convert the two legacy-schema files to the modern format (reference: the structure of `Russian Old (XIX).json`), register all three in `cyrillic_library.json`, verify output, and move them back into `../base/`. Expect to add several codepoints (`Ѣ`, `Ѳ`, `Ѵ`, etc.) to `sortorder_cyrillic.txt` in the process.

## Latin script (experimental, WIP)

The Latin tree under `cyrillic-languages/library/latin/` mirrors the structure of the Cyrillic tree but is considered internal work-in-progress and is **not open for external contributions**. Contributor-facing docs should direct any Latin-related requests to an issue rather than a PR.

Key differences from the Cyrillic workflow:

- **Marker distribution is different.** In the Latin tree, the `=` marker (equivalent with its own Unicode) is dominant — used in roughly half the files to mark accented variants. The `+` marker is rare. Other markers (`&`, `:`, `.ita`, `.str`) are unused.
- **All Latin files use `local: en`.** No locale-specific OpenType alternatives are wired up.
- **Descriptions are more often empty** in the Latin tree than in the Cyrillic tree.
- **Source of truth** for the Latin tree is historically `latin_languages.txt`; the bootstrap script `makeLatinLib.py` re-creates `library/latin/base/` and `library/latin/latin_library.json` from it.

Before opening the Latin tree to contributors, the schema and conventions would need to be audited and formalized the same way the Cyrillic tree has been.

## Known limitations and TODOs

A running list of things that are known-imperfect and should be addressed when someone has the time.

1. **Hardcoded locale list in `compile_languages.py`.** `locales = ['', '.ru', '.ba', '.bg', '.cv', '.sr', '.en']` should be read from `locales.json` instead. See [Locales](#locales). Until this is fixed, adding a locale requires coordinated edits in three places.

2. **Dead marker code in `compile_languages.py`.** The `marks` list contains `*`, `$`, `#`, `@`, `(`, `)`, `[`, `]`, `<`, `.alt` — none of which are used in any current source file:
   - `*`, `$`, `#`, `@`, `<` → their function was migrated to the `type` field in `glyphs_list`.
   - `(`, `)`, `[`, `]` → listed in `marks` but missing from `signtypes`; will raise `KeyError` if a contributor types one.
   - `.alt` → listed in `marks` but its `signtypes` entry is commented out; same crash.

   Cleanup would mean trimming both tables and the `getCharInfo` loop. Done carefully, this would turn the footguns into explicit "unknown marker" errors.

3. **Utility scripts with absolute user paths.** `dumpLangDescriptions.py` and `recode_mainlibfile.py` contain macOS-style absolute paths from an earlier developer setup. Any run starts with a mandatory path edit.

4. **No pre-merge validator.** PRs are reviewed by eye. A small validator script (`scripts/validate.py`) that checks schema completeness, filename/name_eng match, locale validity, and absence of dead/trap markers would remove most of the routine review work. **This is deferred pending scope agreement**; see project history for the outstanding decision.

5. **Legacy files not migrated.** See [The legacy folder](#the-legacy-folder).

6. **Stale contact email in the compiled site bundle.** The React bundle at `cyrillic-languages/static/js/main.9d864c58.js` still contains `fonts@paratype.com` in the "About the project" panel. The new canonical contact is `info@paratype.net`. This requires a site-engine rebuild, which is out of scope for routine data maintenance.

7. **Production split.** This repository currently holds both the data and the site engine. Long-term, splitting into a data-only repository and a site-engine repository (with the site fetching JSON via `raw.githubusercontent.com` URLs, as it already does) would cleanly separate the contributor surface from the site surface. Until that split happens, the contributor/operator boundary is enforced only by the `README.md` map and `CONTRIBUTING.md` — there are no mechanical guards.

8. **`glyphs_list_categories.json` includes `digraph` and `foreign`**, both currently unused in source data (`digraph` is handled inline via the `:` marker). Either remove them from the categories file, or adopt them in data, or document why they are reserved.

## Contact

`info@paratype.net` for anything that needs a human on the Paratype side.
