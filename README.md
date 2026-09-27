# TBIM BIM Bootcamp 2026 – Interactive Event Map Prototype

## Included
1. **System architecture** – data-driven interactive floor plan; booths/classes/speakers are separate from the UI.
2. **Database template** – use `TBIM_Interactive_Map_Database_Template.xlsx` to maintain booth, room, class and speaker data.
3. **HTML prototype** – `index.html` supports clickable hotspots, popup details, search/filter and room schedules.

## Run the prototype
Open `index.html` in a modern browser. It works offline.

## Edit the content
- The prototype reads `data.js`.
- Map background: `assets/floorplan_clean.png` (1536 × 1024) — the original `floorplan.png` with the Job Fair Booth List table removed. `floorplan.png` (original) and `floorplan.webp` (rejected render) are kept but not used.
- Coordinates are percentages of `floorplan_clean.png`: `X_pct, Y_pct, W_pct, H_pct` in Excel. `Rot_deg` rotates a box (Registration = -18). If you change the background image, the coordinates must be re-measured.
- **Logos** (shown in the booth popup), in priority order:
  1. A file in `assets/logos/` named by BoothID, e.g. `assets/logos/P5.png` (`.svg`, `.png`, `.webp`, `.jpg`).
  2. A picture pasted into the booth's `LogoFile` cell in Excel — exported automatically to `assets/logos/excel/`.
  3. Otherwise the popup shows the company name.
  - Booth logos are shown **inside** the booth box on the map (hover to enlarge) and in the popup; the booth ID tag sits just outside the box (above the top Job Fair row, below the others, left of BSI — rule `TAG_POS` in `index.html`). Facilities (Registration etc.) keep the plan visible and show their logo only in the popup.
- Booth popups for REG and BRK have a "Show route" button (`BOOTH_ROUTE` in `index.html`).
- YBIM = Young BIM Club (logo: Sripatum University, cut from the event poster — replace `assets/logos/YBIM.png` with the official file when available). ADV = Hardware Zone (ADVICE), logo shown on the curved desk zone.
- Unused since the full-1F view was removed: Excel rows TR1 / RESC and columns `All_*` — safe to delete.
- `Shape_pts` (Excel, optional): a non-rectangular hotspot as `x,y x,y …` in % of the floor plan — used for the curved ADVICE desks. When filled, it replaces the X/Y/W/H box.
  - Current files (Sep 2026) come from each company's official website; DELL from Wikimedia Commons. P2 Sustainable Solution and P7 Digitech One were recoloured from white to dark so they show on white.
  - SYNNEX (P4), Ritta (J8) and SynergySoft (P6) were supplied by TBIM. J7 is one combined logo: the JAI Group mark + "INNOPLAN" / "WISDOM" as text (replace `assets/logos/J7.png` when real Innoplan / Wisdom logos arrive). J4 Syntec and J5 Bimspaces use the pictures from the Excel file.
- Header banner: `assets/banner.webp` (top of the event poster); click it to view the full poster `assets/poster.webp`.
- Edit `TBIM_Interactive_Map_Database_Template.xlsx`, save it, then regenerate `data.js`:
  ```
  python3 excel_to_data.py
  ```
  (No extra packages needed. `data.js` is overwritten — do not edit it by hand.)
- Exported: booth logos (see above), booths (rows with `Visible = FALSE` or `DataStatus = Hidden` are skipped), rooms, and classes (speaker name, company, topic, key takeaway, time).
- Booth `Notes` are internal and are **not** shown on the map. A booth whose `DataStatus` is not `Ready` (e.g. `Needs confirmation`) shows "Details to be confirmed" instead of its description / contact.
- Training sessions show the **company** only (no speaker name).
- Not exported: speaker personal data (car plate, food allergy, phone, PIC) — it stays in Excel only.

## One-file version (to share / upload)
`TBIM_Interactive_Map.html` contains everything (page, data, routes and all images) in a single file — open it anywhere, offline, no `assets/` folder needed. Rebuild it after any change:
```
python3 excel_to_data.py        # only if the Excel file changed
python3 build_single_html.py
```
Do not edit `TBIM_Interactive_Map.html` directly — edit `index.html`, Excel, `routes.js` or `assets/`, then rebuild. (Install Pillow — `pip3 install pillow` — to make the file smaller.)

## Two tabs
1. **Job Fair & Partners** — clickable booth map (`assets/floorplan_clean.png`, data from Excel → `data.js`).
2. **Route & Training Rooms** — floor plans of SPU Building 11 in `assets/floors/` (1F–3F: TBIM CAD layout plans; 14F: `SPU Layout/BIMBOOT CAMP2026 (15ก.ย.69).pdf`) with animated routes:
   Entrance → Registration → Training Room 1 (1F Zone C) · Training Room 2 (2F, right escalator) · Training Room 3 (3F, central escalator) · Break point (coffee, bread & lunch, 1F) · Executive Session (14F, lift).
   - Route lines, pins and step texts are in `routes.js` (edited by hand, **not** generated from Excel). Coordinates are pixels on each floor image.
   - Room photos (`assets/rooms/`: HALL, TR1, TR2, TR3 — SPU SOE site-visit slides) open when a pin is tapped, and show in the route panel and the TR1 / Registration popups. Set a pin's `photo` in `routes.js`.
   - Break times are calculated automatically from the class schedule gaps (≥ 45 min = lunch).
   - Each class popup has a "Show route" button. Deep link: `index.html#route=tr2` (ids: reg, tr1, tr2, tr3, break, exec) — useful for QR codes at the doors.

## Suggested next version
- Floor selector: 1F / Training Rooms / other floors
- “You are here” + route arrows from Main Entrance
- QR deep links to a booth or class
- Exhibitor logo/photo gallery
- Google Sheet / Supabase sync
- Analytics for booth/class clicks
