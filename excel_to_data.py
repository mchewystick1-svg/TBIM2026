#!/usr/bin/env python3
"""Convert TBIM_Interactive_Map_Database_Template.xlsx -> data.js

Usage:  python3 excel_to_data.py
No extra packages needed (uses only the Python standard library).
"""
import json, posixpath, re, zipfile, xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
XLSX = HERE / "TBIM_Interactive_Map_Database_Template.xlsx"
OUT = HERE / "data.js"
LOGOS = HERE / "assets" / "logos"          # put your own logo files here as <BoothID>.png/.jpg/.svg/.webp
LOGOS_FROM_EXCEL = LOGOS / "excel"          # pictures pasted in the Excel LogoFile column are exported here
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "rel": "http://schemas.openxmlformats.org/package/2006/relationships"}

EVENT = {"name": "BIM Bootcamp 2026", "date": "9 October 2026",
         "venue": "Sripatum University (SPU)", "floor": "1F",
         "floorplan": "assets/floorplan_clean.png"}  # hotspot X/Y/W/H % are measured on this image


def read_sheets(path):
    """Return {sheet name: list of row dicts keyed by the header row}."""
    z = zipfile.ZipFile(path)
    shared = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
    rels = {r.get("Id"): r.get("Target") for r in
            ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall("rel:Relationship", NS)}
    sheets = {}
    for s in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", NS):
        target = rels[s.get(f"{{{NS['r']}}}id")].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        grid, rownums = [], []
        for row in ET.fromstring(z.read(target)).iter(f"{{{NS['m']}}}row"):
            rownums.append(int(row.get("r")))
            cells = {}
            for c in row.findall("m:c", NS):
                col = col_index(c.get("r"))
                t, v = c.get("t"), c.find("m:v", NS)
                if t == "s":
                    val = shared[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(f"{{{NS['m']}}}t"))
                elif t == "b":
                    val = v.text == "1"
                elif v is None:
                    val = None
                elif t == "str":
                    val = v.text
                else:
                    f = float(v.text)
                    val = int(f) if f.is_integer() else f
                cells[col] = val
            grid.append([cells.get(i) for i in range(max(cells, default=-1) + 1)])
        if grid:
            header = [str(h).strip() if h is not None else "" for h in grid[0]]
            rows = []
            for r, num_ in zip(grid[1:], rownums[1:]):
                d = {h: (r[i] if i < len(r) else None) for i, h in enumerate(header) if h}
                if any(v not in (None, "") for v in d.values()):
                    d["_row"] = num_
                    rows.append(d)
            sheets[s.get("name")] = rows
    return sheets


IMAGE_TYPES = {b"\x89PNG": ".png", b"\xff\xd8\xff": ".jpg", b"GIF8": ".gif", b"RIFF": ".webp"}


def read_pictures(path, sheet_name):
    """Return {Excel row number: (bytes, ext)} for valid pictures placed on a sheet."""
    z = zipfile.ZipFile(path)

    def rels_of(part):
        folder, name = posixpath.split(part)
        rp = f"{folder}/_rels/{name}.rels"
        if rp not in z.namelist():
            return {}
        return {r.get("Id"): posixpath.normpath(posixpath.join(folder, r.get("Target")))
                for r in ET.fromstring(z.read(rp)).findall("rel:Relationship", NS)}

    wb_rels = rels_of("xl/workbook.xml")
    sheet_part = next(wb_rels[s.get(f"{{{NS['r']}}}id")]
                      for s in ET.fromstring(z.read("xl/workbook.xml")).find("m:sheets", NS)
                      if s.get("name") == sheet_name)
    pics = {}
    for drawing in (t for t in rels_of(sheet_part).values() if "/drawings/" in t):
        media = rels_of(drawing)
        xml = z.read(drawing).decode("utf-8")
        for anchor in re.findall(r"<xdr:(?:oneCell|twoCell)Anchor.*?</xdr:(?:oneCell|twoCell)Anchor>", xml, re.S):
            row = re.search(r"<xdr:from>.*?<xdr:row>(\d+)</xdr:row>", anchor, re.S)
            emb = re.search(r'r:embed="([^"]+)"', anchor)
            if not (row and emb and emb.group(1) in media):
                continue
            data = z.read(media[emb.group(1)])
            ext = next((e for sig, e in IMAGE_TYPES.items() if data.startswith(sig)), None)
            if ext:  # skip broken / placeholder pictures
                pics[int(row.group(1)) + 1] = (data, ext)
    return pics


def logo_for(booth_id, excel_pic):
    """A file you put in assets/logos/ wins; otherwise use the picture from Excel."""
    for ext in (".svg", ".png", ".webp", ".jpg", ".jpeg"):
        f = LOGOS / f"{booth_id}{ext}"
        if f.exists():
            return f.relative_to(HERE).as_posix()
    if excel_pic:
        data, ext = excel_pic
        LOGOS_FROM_EXCEL.mkdir(parents=True, exist_ok=True)
        f = LOGOS_FROM_EXCEL / f"{booth_id}{ext}"
        f.write_bytes(data)
        return f.relative_to(HERE).as_posix()
    return ""


def col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group():
        n = n * 26 + ord(ch) - 64
    return n - 1


def txt(v):
    return "" if v is None else str(v).strip()


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def hhmm(v):
    """Excel stores times as a fraction of a day."""
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        mins = round(v * 24 * 60)
        return f"{mins // 60:02d}:{mins % 60:02d}"
    return txt(v)


def shape(v):
    """ "x,y x,y ..." (percent of the floor plan) -> [[x, y], ...] for a non-rectangular hotspot."""
    pts = [p.split(",") for p in txt(v).split()]
    return [[float(x), float(y)] for x, y in pts] if pts else None


def main():
    sh = read_sheets(XLSX)

    pictures = read_pictures(XLSX, "02_Booths")
    booths = []
    for b in sh["02_Booths"]:
        if b.get("Visible") is False or txt(b.get("DataStatus")) == "Hidden":
            continue
        booths.append({
            "id": txt(b["BoothID"]), "name": txt(b["Company"]), "category": txt(b["Category"]),
            "x": num(b.get("X_pct")), "y": num(b.get("Y_pct")),
            "w": num(b.get("W_pct")), "h": num(b.get("H_pct")), "rot": num(b.get("Rot_deg")) or 0,
            "poly": shape(b.get("Shape_pts")),
            "description": txt(b.get("ShortDescription")), "products": txt(b.get("ProductsServices")),
            "contact": txt(b.get("ContactPerson")), "phone": txt(b.get("ContactPhone")),
            "website": txt(b.get("Website")), "qr": txt(b.get("QR_Link")),
            "logo": logo_for(txt(b["BoothID"]), pictures.get(b["_row"])), "note": txt(b.get("Notes")),
        })

    rooms = [{
        "id": txt(r["RoomID"]), "name": txt(r["RoomName"]), "pathway": txt(r.get("Pathway")),
        "floor": txt(r.get("Floor")),
        "x": num(r.get("X_pct")), "y": num(r.get("Y_pct")),
        "w": num(r.get("W_pct")), "h": num(r.get("H_pct")),
    } for r in sh["03_Rooms"]]

    # RoomID in 04_Classes is a slot code like "TR1-01" -> room "TR1"
    classes = [{
        "id": txt(c["ClassID"]), "room": txt(c["RoomID"]).split("-")[0],
        "start": hhmm(c.get("StartTime")), "end": hhmm(c.get("EndTime")),
        "topic": txt(c.get("Topic")), "speaker": txt(c.get("SpeakerDisplay")),
        "org": txt(c.get("Organisation")), "takeaway": txt(c.get("KeyTakeaway")),
    } for c in sh["04_Classes"]]
    classes.sort(key=lambda c: (c["room"], c["start"]))

    data = {"event": EVENT, "booths": booths, "rooms": rooms, "classes": classes}
    OUT.write_text(
        "// AUTO-GENERATED from TBIM_Interactive_Map_Database_Template.xlsx by excel_to_data.py\n"
        "// Edit the Excel file, then run:  python3 excel_to_data.py\n"
        "window.TBIM_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n",
        encoding="utf-8")
    print(f"Wrote {OUT.name}: {len(booths)} booths, {len(rooms)} rooms, {len(classes)} classes")
    missing = [b["id"] for b in booths if not b["logo"]]
    print(f"Logos: {len(booths) - len(missing)} found" + (f", missing: {', '.join(missing)}" if missing else ""))


if __name__ == "__main__":
    main()
