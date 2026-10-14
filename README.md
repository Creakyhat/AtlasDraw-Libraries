# AtlasDraw Libraries

Ready-made shape libraries for [AtlasDraw](https://atlasdraw.com), made by Creakyhat or contributed by others.
Each one is an `.atlasdrawlib` file: open it, or drag it onto AtlasDraw, and its shapes are added to the library
sidebar.

## Layout

```
libraries/
  <category>/                   e.g. infrastructure/
    <library>/                  e.g. network-diagram/
      <library>.atlasdrawlib
      preview.png               shown on the website
libraries.json                  generated index the website reads; don't edit by hand
scripts/validate.py             checks every library and regenerates libraries.json
FORMAT.md                       the .atlasdrawlib format
```

## Adding a library

1. Build the shapes in AtlasDraw, give each a name, then use **Export category…** or **Export whole library…**
   in the library sidebar.
2. Put the file at `libraries/<category>/<library>/<library>.atlasdrawlib`. Folder names are lower-case and
   hyphenated, and the category folder must match the library's `category`.
3. Add the details at the top of the file: `id`, `name`, `description`, `author`, `licence`, `category` and
   `tags` (see [FORMAT.md](FORMAT.md)). Exports from AtlasDraw don't include these yet.
4. Add a `preview.png` of the shapes (about 900 px wide).
5. Run `python scripts/validate.py` and commit the updated `libraries.json` with the library.

GitHub runs the same check on every push and pull request.

### Rules

- Only `.atlasdrawlib` files. Excalidraw libraries aren't accepted: people who want those can get them from
  Excalidraw and import them in AtlasDraw.
- Every library names its author and licence (`CC-BY-4.0`, `CC0-1.0` or `MIT`). Only submit work you made or
  have the right to share under that licence.
- Item ids must be unique across the repo; prefix them with the library's publisher and name, e.g.
  `creakyhat.network.router`.

## Licence

Each library's licence is in its file and shown on the website. Libraries by Creakyhat are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The scripts in this repo are © Creakyhat.
