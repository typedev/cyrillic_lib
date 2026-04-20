# Legacy language files

This folder holds historical Russian-script language files that **are not part of the current build pipeline**. They are kept under version control so they are not lost, but they are not referenced by `cyrillic_library.json`, `compile_languages.py` ignores them, and no generated output is produced for them.

## Why they're here

These files pre-date the current JSON schema and have been parked until someone decides whether to migrate them to the modern format or retire them altogether.

## Files and their schema

| File | Schema |
|---|---|
| `Russian Ancient (XVIII).json` | **Legacy** — glyphs split across flat keys: `uppercase_alphabet` / `lowercase_alphabet`, `uppercase_dialect` / `lowercase_dialect`, `uppercase_historic` / `lowercase_historic`, `uppercase_lexic` / `lowercase_lexic`. No `glyphs_list`. |
| `Russian Church (X-XVII).json` | **Legacy** — same flat-keys schema as above. |
| `Russian Old (XIX).json` | **Modern** — uses `glyphs_list`. Simply not registered in `cyrillic_library.json`, so the pipeline does not process it. |

## What to do with them

Two options, to be decided by maintainers:

1. **Migrate.** Convert the two legacy-schema files to the modern `glyphs_list` format, register all three in `cyrillic_library.json`, verify output, and move them back into `../base/`.
2. **Retire.** Delete the folder if these historical alphabets are permanently out of scope.

Contributors: please don't edit anything in this folder. Open an issue instead.
