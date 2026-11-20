# Tea Menu

A small static site for guests to browse the house tea collection, filter it, and pick a cup. Guests tell the host their choice in person.

Hosted with GitHub Pages: https://amberdoctor.github.io/tea/

- `index.html`: the whole site (no build step)
- `teas.json`: the public tea list. It holds only teas marked to share that are in stock, and only guest-facing fields.
- `tools/build_teas.py`: regenerates `teas.json` from the full (private) tea list CSV

To update: `python tools/build_teas.py path/to/tea-collection.csv`, then commit `teas.json`.
The full CSV lives in a private repo and should never be committed here.
