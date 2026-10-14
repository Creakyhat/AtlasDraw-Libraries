# The `.atlasdrawlib` format (version 1)

An AtlasDraw library is a UTF-8 JSON file with the extension `.atlasdrawlib` and the media type
`application/vnd.atlasdraw.library+json`.

```json
{
  "type": "atlasdrawlib",
  "version": 1,
  "id": "creakyhat.network-diagram",
  "name": "Network diagram",
  "description": "Routers, switches, access points…",
  "author": { "name": "Creakyhat", "url": "https://creakyhat.co.uk" },
  "licence": "CC-BY-4.0",
  "category": "Infrastructure",
  "tags": ["network", "router"],
  "items": [
    {
      "id": "creakyhat.network.router",
      "status": "published",
      "created": 1792022400000,
      "name": "Router",
      "category": "Optional sidebar category",
      "elements": [ … ],
      "files": { … }
    }
  ]
}
```

| Field | Required | Meaning |
|---|---|---|
| `type` | yes | Always `"atlasdrawlib"`. |
| `version` | yes | Format version. AtlasDraw refuses files newer than it understands. |
| `id` | in this repo | Stable id, `publisher.library-name`. |
| `name` | in this repo | Shown on the website, and the sidebar category for items that don't set their own. |
| `description` | in this repo | One or two sentences for the website. |
| `author` | in this repo | `name`, and optionally `url`. |
| `licence` | in this repo | SPDX id: `CC-BY-4.0`, `CC0-1.0` or `MIT`. |
| `category` | in this repo | The website category, which is also the folder the library lives in. |
| `tags` | no | Search words for the website. |
| `items` | yes | The shapes. |

Each item's `elements` are AtlasDraw elements, which use the Excalidraw element schema plus AtlasDraw extras
(effects, curved paths and Markdown) in `customData`. `files` holds any images the elements use, keyed by file id.
Item ids must be unique: AtlasDraw skips an item that's already in the user's library, so reinstalling a
library doesn't duplicate it.

The details (`id` to `tags`) are optional in the format itself, so a plain export from AtlasDraw is valid. They're
required for libraries published here.

AtlasDraw also imports Excalidraw's `.excalidrawlib` files, but never writes them, and this repo doesn't hold them.
