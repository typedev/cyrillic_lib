# Contributing

Thank you for your interest in improving the Cyrillic Languages knowledge base. This document explains what contributors can change, the format of the data files, the glyph-marker syntax, and the steps for submitting a Pull Request.

A Russian translation is available in [CONTRIBUTING-RU.md](CONTRIBUTING-RU.md).

## Who this is for

This guide is for anyone who wants to correct or extend information about a **Cyrillic-script language**: fix an alphabet, update a description, add a dialect form, correct alternative names, and so on.

A Latin-script tree exists elsewhere in the repository (`cyrillic-languages/library/latin/`) but is an internal work-in-progress and is **not open for external contributions**. Please do not open PRs against it.

## What you can edit

Contributors should only ever change files inside:

```
cyrillic-languages/library/cyrillic/base/
```

Every other directory — including `site/`, `static/`, `scripts/`, and the shared configuration files next to them — is maintained by the project operators and should not be touched in a contributor PR. See the **Repository map** in the root [README.md](README.md) for the full list.

The rule of thumb: if you are editing a single per-language JSON file, you are doing it right.

## Workflow

1. **Fork** this repository.
2. **Edit** one or more `.json` files under `cyrillic-languages/library/cyrillic/base/`.
3. **Open a Pull Request** against `master`.
4. A maintainer will review your change, possibly request adjustments, and — once the change is accepted — regenerate the site artifacts under `cyrillic-languages/site/` in a follow-up commit. You do not need to regenerate or commit anything under `site/` yourself.

Your PR title and description may be written in **English or Russian** — whichever is more natural for you. Please include a short explanation of *why* the change is being made and, where applicable, a reference to the source (dictionary, orthographic reference, academic paper, community consensus…) that supports it.

## The per-language JSON file

One file per language, named after the English name of the language, e.g. `Avar.json`. The filename must match the `name_eng` field inside.

### Required fields

| Field | Type | Description |
|---|---|---|
| `name_eng` | string | English name of the language. Must match the filename (without `.json`). |
| `name_rus` | string | Russian name of the language. |
| `local` | string | OpenType locale tag used to switch on localized glyph forms for this language. Allowed values today: `ru` (default), `ba` (Bashkir), `bg` (Bulgarian), `cv` (Chuvash), `sr` (Serbian). If your language needs a new locale, open an issue — adding one requires code changes. |
| `language_group_rus` | array of strings | Language-family classification in Russian, from broadest to narrowest. Example: `["Индоевропейские языки", "Славянские языки"]`. |
| `alt_names_eng` | array of strings | English alternative / historical names of the language. Always a list, even if there is only one name. |
| `description_rus` | string | Plain-text description of the language and its alphabet, in Russian. |
| `glyphs_list` | array | The alphabet and related character sets. See [Glyph blocks](#glyph-blocks) below. |

### Recommended fields

| Field | Type | Description |
|---|---|---|
| `description_eng` | string | Plain-text description in English. About two-fifths of the existing files are still missing this — new contributions should fill it in. |
| `language_group_eng` | array of strings | English counterpart of `language_group_rus`. |

### Text formatting

`description_*`, `name_*`, `language_group_*`, and `alt_names_eng` are **plain text** — no Markdown, no HTML. Inside `description_*` you may use `\n` to separate paragraphs. A trailing `\n` is not required. Typical descriptions are a paragraph or two (up to ~500 characters).

### Internal/ignored fields

You may see the following in some files; contributors should not add or modify them:

- `code_pt` (in `cyrillic_library.json`, not inside the per-language file) — an internal Paratype identifier. Curators assign the real value.

## Glyph blocks

The `glyphs_list` field is an array of blocks. Each block represents one view of the language's glyph inventory, for example the alphabet proper, or historical forms, or dialect-only glyphs.

A block looks like this:

```json
{
    "type": "alphabet",
    "uppercase": "А Б В Г ...",
    "lowercase": "а б в г ..."
}
```

### Block types

| `type` | Meaning |
|---|---|
| `alphabet` | The current official alphabet of the language. Every file has exactly one `alphabet` block. |
| `extended` | Extended orthographic notation — signs used alongside the alphabet (e.g. Private Use Area codepoints rendered by the Paratype fonts, extra letters used only in certain contexts). |
| `historic` | Historical forms no longer part of the modern alphabet, still useful in historical texts or references. |
| `dialect` | Glyph forms used in dialects of the language, not part of the standard alphabet. |
| `consideration` | Signs for which there is currently **no consensus within the language community itself** — for example, characters whose use is under active debate among speakers or scholars. Use this sparingly; the value judgement belongs to people who know the language, not to the pipeline. |

A block may be omitted if there is nothing to put in it; not every language has `historic` or `dialect` entries.

### The `uppercase` and `lowercase` strings

Both strings are space-separated lists of **glyph tokens**. A token is normally one glyph — a single Unicode character — but it may also be:

- A **multi-character digraph** (`Дж`, `Дз` in Belarusian).
- A **Unicode escape** like `!F86F` for a character that cannot be typed on a normal keyboard — typically a Private Use Area codepoint rendered by the Paratype fonts.
- One of the above with **one or more markers** prepended or appended to attach semantics; see the next section.

The two strings must be parallel: every glyph on the uppercase side should have a matching lowercase counterpart in the same position, and vice versa.

## Glyph markers — live reference

Markers are single characters or suffixes attached to a token, with **no space between the marker and the token**. They are interpreted by the compilation pipeline. Multiple markers may combine on the same token; the order in which they are written does not matter.

### `+` — Alternate with its own Unicode

Groups the token under the **previous** main glyph as an alternate form. The alternate has its own valid Unicode codepoint.

Example — excerpt from the alphabet block of [Bashkir.json](cyrillic-languages/library/cyrillic/base/Bashkir.json):

```
А Б В Г &!F53C +Ғ Д &!F50A +Ҙ Е Ё ... С &!F53E +Ҫ Т У Ү Ф Х Һ ...
```

Each `+<letter>` attaches to the token immediately before it. In `&!F53C +Ғ`, the primary glyph is a codepoint in the Private Use Area (see the `!XXXX` section below), rendered via the OpenType `locl` feature (marker `&`), and `Ғ` is an alternate form that has its own standard Unicode codepoint.

### `&` — Localized form

Marks the token as a glyph that should render via the OpenType `locl` feature for the language's `local` value. Typically used together with `+` or `!XXXX`. Same excerpt from [Bashkir.json](cyrillic-languages/library/cyrillic/base/Bashkir.json) illustrates it — `&!F53C`, `&!F50A`, `&!F53E` are all Private Use Area codepoints (see the note on the PUA in the `!XXXX` section below) that the Paratype fonts substitute in when the `locl` feature is active for Bashkir (`"local": "ba"`).

### `:` — Digraph

Groups the token under the previous glyph as a digraph — a sequence of two characters treated as a single letter of the alphabet.

Example — excerpt from the alphabet block of [Belarusian.json](cyrillic-languages/library/cyrillic/base/Belarusian.json):

```
А Б В Г Ґ Д :Дж :Дз Е Ё Ж З І Й К Л М Н О П Р С Т У Ў Ф Х Ц Ч Ш Ы Ь Э Ю Я ʼ
```

`Дж` and `Дз` are Belarusian digraphs attached to `Д`.

### `!XXXX` — Unicode escape

A literal Unicode codepoint given by its hex code. Used when the character cannot easily be typed on the keyboard — in practice, almost always a codepoint in the Unicode Private Use Area (PUA, `E000`–`F8FF`).

Example — excerpt from the `extended` block of [Avar.json](cyrillic-languages/library/cyrillic/base/Avar.json):

```
!F86F !F872 !F875 !F878 !F87B !F87E
```

You can chain: `!F86F!F870` produces a two-character sequence.

#### About the Private Use Area

The PUA is a range of codepoints that the Unicode Consortium deliberately leaves unassigned — a blank canvas that any font or application may use for whatever it needs. **No one owns these codepoints.** Paratype historically uses part of this range (roughly `F000` and above) inside its own fonts to encode glyphs that have no official Unicode assignment — for example, historical or dialectal Cyrillic letters. That mapping is meaningful **only** when the text is rendered in a Paratype font that actually contains those glyphs — PT Sans Expert / PT Serif Expert, which this project ships; see the root [README](README.md).

**In a font from a different foundry, the same `!FXXX` hex code will usually display a completely different glyph — or nothing at all (an empty box).** Read `!FXXX` in this repository as *"the glyph at this codepoint in the Paratype Expert fonts,"* not as a universal character reference.

**Do not introduce new `!FXXX` codepoints in a contributor PR.** Even though the PUA itself is unowned, a useful entry here requires the codepoint to actually be assigned to a glyph inside the Paratype fonts — which is a coordinated change on the font side. If you believe a glyph that has no official Unicode codepoint needs to be added, please open an issue instead.

### `.ita` / `.str` — Style-specific glyphs

Suffixes. `.ita` marks a glyph that should appear only in italic style; `.str` (short for "straight", i.e. upright) marks a glyph that should appear only in the upright style. Used when the same nominal letter has two distinct designs that are selected by style rather than by locale. Currently used only in **Bulgarian** and **Serbian**.

Example — excerpt from the lowercase alphabet of [Bulgarian.json](cyrillic-languages/library/cyrillic/base/Bulgarian.json):

```
... &в +в &г.str +г.ita &д +д е &ж +ж &з +з &и.str +и.ita ...
```

Here `&г.str` is the localized Bulgarian form of `г` used in the upright style, and `+г.ita` is an alternate representation used in italic.

### Combining markers

Markers can stack on one token. Order does not affect parsing. For example `&!F53C` and `!F53C&` would both be read as "a PUA codepoint that is a localized form".

## Deprecated markers — do not use

Earlier versions of the pipeline used a different scheme. The following markers still appear in the parser code but are **no longer used anywhere in the data**, and you should not introduce them:

- `*` (replacement), `$` (extended / lexicographic), `#` (historic), `@` (dialect), `<` (alphabet) — their function has been replaced by the `type` field on the `glyphs_list` block.
- `.alt` — listed in the parser but never active; **using it will crash the compiler.**
- `(`, `)`, `[`, `]` — listed in the parser's marker table but missing from its handler; **using them will crash the compiler.**

If you see one of these markers in an existing file, it is almost certainly an old leftover; flag it in your PR rather than copying the pattern.

## Editing an existing language

The usual case: you want to add, remove, or correct a glyph in an existing alphabet, or update a description.

1. Open `cyrillic-languages/library/cyrillic/base/<Language>.json`.
2. Locate the relevant field — usually a glyph block inside `glyphs_list`, or one of the description fields.
3. Make the minimal change needed. Keep the `uppercase` and `lowercase` strings in lock-step: every uppercase glyph should have its lowercase counterpart at the same position, and vice versa.
4. Save, commit, open a PR.

**If you are adding a glyph whose Unicode codepoint is not already present in the sort order table** (`cyrillic-languages/library/cyrillic/sortorder_cyrillic.txt`), call this out explicitly in your PR description. The sort order table is operator-only, but your PR will prompt the maintainer to add the missing entry.

## Adding a new language

This is a bigger change because it touches more than one file and may require new entries in the shared sort-order table. Before doing the work, please **open an issue first** describing the language you want to add — this helps the maintainers plan the sort-order and `code_pt` assignment.

Once that is discussed, a new-language PR will usually include:

- A new file `cyrillic-languages/library/cyrillic/base/<Language>.json` filled out according to this document.
- (Via the maintainer) a corresponding entry in `cyrillic-languages/library/cyrillic/cyrillic_library.json` with `enable: true` and a `code_pt` value assigned by the maintainer; leave `"code_pt": "1"` as a placeholder if you include it in the PR.

Contributors do not need to (and should not) edit `sortorder_cyrillic.txt` themselves.

## Pre-flight checklist

Before opening a PR, please verify:

- [ ] You edited only files under `cyrillic-languages/library/cyrillic/base/`.
- [ ] You did **not** modify anything under `site/`, `static/`, `scripts/`, `fonts/`, or any shared configuration file.
- [ ] The filename matches the `name_eng` field exactly.
- [ ] All required fields are present and non-empty.
- [ ] `local` is one of the allowed values (`ru`, `ba`, `bg`, `cv`, `sr`).
- [ ] Glyph tokens use only the live markers documented above. No `*`, `$`, `#`, `@`, `<`, `.alt`, `(`, `)`, `[`, `]`.
- [ ] You did not introduce new Private Use Area codepoints (`!FXXX`). If you needed one, you opened an issue instead — adding a PUA entry requires a coordinated change in the Paratype fonts.
- [ ] If you added a character whose Unicode is not yet in `sortorder_cyrillic.txt`, you mentioned it in the PR description.
- [ ] The PR description explains what changed and links to a source where applicable.

## Getting help

If something in this document is unclear, or you are not sure whether a change belongs in a contributor PR or needs maintainer action, please open an issue. Better to ask than to guess.

Contact for off-repository questions: **info@paratype.net**.
