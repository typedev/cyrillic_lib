<!-- Thank you for contributing! Please fill in the sections below.
     A full contributor guide is available in CONTRIBUTING.md / CONTRIBUTING-RU.md. -->

## What changed

<!-- Which language file(s) did you edit, and what specifically did you change?
     Added / removed / corrected a glyph? Fixed a description? Updated a name? -->

## Language(s) affected

<!-- e.g. Avar, Belarusian -->

## Source for the change

<!-- Dictionary, orthographic reference, academic publication, community consensus, etc.
     A URL or book citation is ideal. -->

## Checklist

- [ ] I only edited files under `cyrillic-languages/library/cyrillic/base/`.
- [ ] I did **not** touch anything under `cyrillic-languages/site/`, `static/`, `scripts/`, `fonts/`, or any shared configuration file.
- [ ] The filename matches the `name_eng` field exactly.
- [ ] All required fields are present (`name_eng`, `name_rus`, `local`, `language_group_rus`, `alt_names_eng`, `description_rus`, `glyphs_list`).
- [ ] `local` is one of `ru`, `ba`, `bg`, `cv`, `sr`.
- [ ] Glyph tokens only use live markers (`+`, `=`, `&`, `:`, `!XXXX`, `.ita`, `.str`). No `*`, `$`, `#`, `@`, `<`, `.alt`, `(`, `)`, `[`, `]`.
- [ ] I did not introduce new Private Use Area codepoints (`!FXXX`). If I needed one, I opened an issue instead.
- [ ] If I added a character whose Unicode is not yet in `sortorder_cyrillic.txt`, I mentioned it in the description above.
