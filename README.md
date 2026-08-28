# Battery Emulator translations

User-interface translations for the Battery Emulator web UI, served to browsers over GitHub Pages.

The device itself never downloads these. Its web UI ships English inline and asks the browser to
fetch a language pack only when someone picks one; the pack is then cached in that browser's
`localStorage`. A device with no internet connection stays fully usable in English, and a browser
that has already cached a pack keeps working offline.

## Layout

| Path | Purpose |
|---|---|
| `index.json` | The list of available languages. The UI fetches this first. |
| `packs/<code>.json` | One language pack. |
| `template/en.json` | English source text. Translate from this; never edit it by hand. |

`index.json` is generated — run `python3 tools/build_index.py` after changing any pack:

```json
{
  "revision": "67d6407a9148",
  "languages": [
    { "code": "sv", "name": "Svenska", "path": "packs/sv.json" }
  ]
}
```

`revision` is a hash of every pack's bytes. Clients store it and re-pull all packs
only when it changes, so editing a translation is enough to push it out — nobody
has to remember to bump a version.

- `code` is the language tag the UI stores as the reader's choice.
- `name` is the language's own name for itself — `Deutsch`, not `German`. It is what the picker
  shows, and it is never translated.
- `path` resolves relative to `index.json`.

A pack is a flat object of `key: string`, with exactly the keys used in `template/en.json`.

## Status of the packs here

**Every pack in this repository is an unreviewed demonstration translation and is not fit for
production use.** They were machine-authored to exercise the download mechanism, and nobody who
speaks the language has checked them.

They cover the whole interface — navigation, buttons, card titles, row labels, settings field
labels, live control labels, help text and apply errors. **The 137 event and fault messages are
deliberately left in English** and fall back to it, because that is where a mistranslation stops
being cosmetic and starts misreporting the state of a battery.

Each pack needs a named human owner before it should be trusted.

## Adding a language

1. Copy `template/en.json` to `packs/<code>.json`.
2. Translate the values. Leave the keys alone.
3. Add the language's endonym to `NAMES` in `tools/build_index.py`.
4. Run `python3 tools/build_index.py`.
5. Open a pull request.

Keys you leave out fall back to English, so a partial translation is usable and safe to submit.

## Before you translate

**Do not machine-translate this file.** 137 of the strings are fault and status messages, and some
of them are safety-critical — `THERMAL RUNAWAY! POTENTIAL FIRE OR EXPLOSION IMMINENT!` is one of
them. A mistranslated fault message misreports a hazard to somebody standing in front of a live
battery pack, which is worse than showing them English. Every pack needs a human who speaks the
language and understands what the device does.

Some things are deliberately absent and must stay absent:

- Battery, inverter, charger and shunt product names are proper nouns and are never translated.
- Unit symbols (V, A, W, kWh, °C) are SI and are never translated.
- The advanced diagnostics page stays English; its readers are working from manufacturer
  documentation that is itself in English.

`{}` in a string is a placeholder the UI fills in. Keep it, and put it where the sentence needs it.

## Keeping a pack current

`template/en.json` changes whenever the firmware gains a driver or a screen, so packs drift. A key
that disappears from the template is dead weight; a key that appears is untranslated and falls back
to English until someone fills it in.

## Licence

GPL v3, matching the Battery Emulator firmware these strings are extracted from.
