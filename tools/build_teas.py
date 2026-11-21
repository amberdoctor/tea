"""Build teas.json for the public site from the full tea list.

Usage:  python tools/build_teas.py path/to/tea-collection.csv
Keeps only teas with Share? = Yes that are in stock, and only guest-facing
columns. Never commit the full CSV to this public repo.
"""
import csv, json, sys, pathlib

PUBLIC = ["Tea","Source","Type","Subtype","Style","Format","Origin","Caffeine (brand rating)","Caffeine scale",
          "Tasting summary","Provided Tasting Notes & Descriptions","Ingredients","Allergens","Preparation",
          "Water temp","Steep time","Leaf amount","Infusions","Hot / iced","Milk?","Organic"]
KEYS = {"Tea":"name","Source":"brand","Type":"type","Subtype":"subtype","Style":"style","Format":"format",
        "Origin":"origin","Caffeine (brand rating)":"caffeine","Caffeine scale":"caffeineScale",
        "Tasting summary":"summary","Provided Tasting Notes & Descriptions":"description","Ingredients":"ingredients",
        "Allergens":"allergens","Preparation":"preparation","Water temp":"waterTemp","Steep time":"steepTime",
        "Leaf amount":"leafAmount","Infusions":"infusions","Hot / iced":"hotIced","Milk?":"milk","Organic":"organic"}
IN_STOCK = {"in stock","limited"}

def main(src):
    out = []
    with open(src, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("Share?","").strip().lower() != "yes": continue
            if row.get("Stock","").strip().lower() not in IN_STOCK: continue
            tea = {KEYS[c]: row.get(c,"").strip() for c in PUBLIC}
            if "of ?" in tea["caffeineScale"]: tea["caffeineScale"] = ""
            tea["description"] = tea["description"].replace(" (my summary of the brand's text)", "")
            if row.get("Stock","").strip().lower() == "limited": tea["limited"] = True
            out.append({k: v for k, v in tea.items() if v})  # drop empty fields
    out.sort(key=lambda t: (t["type"], t["name"].lower()))
    dest = pathlib.Path(__file__).resolve().parent.parent / "teas.json"
    # one tea per line keeps the file small and git diffs readable
    lines = ",\n".join(json.dumps(t, ensure_ascii=False) for t in out)
    dest.write_text("[\n" + lines + "\n]\n", encoding="utf-8")
    print(f"Wrote {len(out)} teas to {dest}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "tea-collection.csv")
