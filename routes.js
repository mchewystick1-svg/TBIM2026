// Wayfinding data for the "Route & Training Rooms" tab.
// 1F / 2F / 3F: SPU Building 11 CAD plans (TBIM layout, "Plan Level 1-3"). 14F: "SPU Layout/BIMBOOT CAMP2026 (15ก.ย.69).pdf".
// All x, y values are PIXELS on that floor's image (w × h below) — open the .jpg to read positions.
// photo: shown when the pin is clicked (and in the panel of a route whose room / place matches). This file is edited by hand (NOT generated from Excel).
window.TBIM_ROUTES = {
  floors: [
    {id: "1F",  name: "1F · Exhibition Hall & TR-1", image: "assets/floors/1F.jpg",  w: 1530, h: 550},
    {id: "2F",  name: "2F · TR-2",                    image: "assets/floors/2F.jpg",  w: 1490, h: 475},
    {id: "3F",  name: "3F · TR-3",                    image: "assets/floors/3F.jpg",  w: 1490, h: 480},
    {id: "14F", name: "14F · Executive",              image: "assets/floors/14F.jpg", w: 1896, h: 690}
  ],

  // Pins shown on each floor. type: entrance | registration | room | escalator | lift | break
  places: [
    {id: "ENT",   floor: "1F",  x: 425,  y: 395, type: "entrance",     label: "Main Entrance", photo: "assets/rooms/HALL.jpg", info: "Building 11 · 1F Zone A exhibition hall."},
    {id: "REG",   floor: "1F",  x: 340,  y: 243, type: "registration", label: "Registration", photo: "assets/rooms/HALL.jpg", info: "Registration desk (2 staff). T-shirts are handed out after registration."},
    {id: "BRK",   floor: "1F",  x: 715,  y: 315, type: "break",        label: "Break · coffee, bread & lunch", photo: "assets/rooms/BREAK.svg", info: "Coffee & bread in the breaks, lunch at midday."},
    {id: "CE1",   floor: "1F",  x: 515,  y: 340, type: "escalator",    label: "Central escalator ↑ 3F"},
    {id: "RE1",   floor: "1F",  x: 1350, y: 245, type: "escalator",    label: "Right escalator ↑ 2F"},
    {id: "LIFT1", floor: "1F",  x: 950,  y: 200, type: "lift",         label: "Lift ↑ 14F"},
    {id: "TR1",   floor: "1F",  x: 1125, y: 330, type: "room",         label: "Training Room 1", room: "TR1", photo: "assets/rooms/TR1.jpg", info: "1F Zone C · training area 86 seats / 43 desks."},
    {id: "RE2",   floor: "2F",  x: 1300, y: 237, type: "escalator",    label: "Right escalator"},
    {id: "CE2",   floor: "2F",  x: 540,  y: 335, type: "escalator",    label: "Central escalator ↑ 3F"},
    {id: "TR2",   floor: "2F",  x: 1110, y: 330, type: "room",         label: "Training Room 2", room: "TR2", photo: "assets/rooms/TR2.jpg", info: "2F, opposite the glass room · tiered lecture room."},
    {id: "CE3",   floor: "3F",  x: 535,  y: 330, type: "escalator",    label: "Central escalator"},
    {id: "TR3",   floor: "3F",  x: 575,  y: 175, type: "room",         label: "Training Room 3", room: "TR3", photo: "assets/rooms/TR3.jpg", info: "3F theatre-room zone (Movie Room)."},
    {id: "LIFT14",floor: "14F", x: 1175, y: 200, type: "lift",         label: "Lift"},
    {id: "BRK14", floor: "14F", x: 610,  y: 445, type: "break",        label: "Executive break · coffee & tea"},
    {id: "EX",    floor: "14F", x: 615,  y: 255, type: "room",         label: "Executive Session", room: "EX1"}
  ],

  // Every route starts Main Entrance → Registration, then continues.
  // legs: the line drawn on each floor, in walking order. room: RoomID in Excel (for the session list).
  routes: [
    {id: "reg", name: "Entrance → Registration", color: "#0b2d4d", legs: [
      {floor: "1F", points: [[440,470],[425,395],[415,320],[365,262],[340,243]]}
    ], steps: [
      {floor: "1F", text: "Enter at the Main Entrance (1F)."},
      {floor: "1F", text: "Go straight to the Registration desk, collect your T-shirt."}
    ]},
    {id: "tr1", name: "Training Room 1", sub: "1F · Zone C", room: "TR1", color: "#1776d2", legs: [
      {floor: "1F", points: [[440,470],[425,395],[415,320],[365,262],[340,243],[420,285],[600,290],[715,300],[800,255],[955,245],[1000,245],[1045,262],[1125,330]]}
    ], steps: [
      {floor: "1F", text: "From Registration, walk across the hall past the Job Fair booths."},
      {floor: "1F", text: "Pass the Break point and the lift lobby."},
      {floor: "1F", text: "Enter Zone C — Training Room 1 is straight ahead."}
    ]},
    {id: "tr2", name: "Training Room 2", sub: "2F · right escalator", room: "TR2", color: "#16a36a", legs: [
      {floor: "1F", points: [[440,470],[425,395],[415,320],[365,262],[340,243],[420,285],[600,290],[715,300],[800,255],[955,245],[1000,245],[1045,245],[1250,240],[1350,245]]},
      {floor: "2F", points: [[1300,237],[1100,240],[1005,245],[1025,275],[1110,330]]}
    ], steps: [
      {floor: "1F", text: "From Registration, walk through the lift lobby into Zone C."},
      {floor: "1F", text: "Take the RIGHT escalator up to 2F."},
      {floor: "2F", text: "Walk back along the corridor — Training Room 2 is opposite the glass room."}
    ]},
    {id: "tr3", name: "Training Room 3", sub: "3F · central escalator", room: "TR3", color: "#7b4bd6", legs: [
      {floor: "1F", points: [[440,470],[425,395],[415,320],[365,262],[340,243],[420,300],[515,340]]},
      {floor: "2F", points: [[540,335]]},
      {floor: "3F", points: [[535,330],[545,265],[575,232],[575,175]]}
    ], steps: [
      {floor: "1F", text: "From Registration, take the CENTRAL escalator in the hall."},
      {floor: "2F", text: "At 2F, stay on the central escalator and continue up."},
      {floor: "3F", text: "At 3F, walk straight ahead — Training Room 3 (Movie Room)."}
    ]},
    {id: "break", name: "Break point", sub: "Coffee, bread & lunch · 1F", place: "BRK", color: "#e8a400", legs: [
      {floor: "1F", points: [[440,470],[425,395],[415,320],[365,262],[340,243],[420,285],[600,295],[715,315]]}
    ], steps: [
      {floor: "1F", text: "The Break point is on the right side of the exhibition hall, next to the lift lobby."},
      {floor: "1F", text: "Coffee & bread in the breaks, lunch at midday (times below)."}
    ], breaks: true},
    {id: "exec", name: "Executive Session", sub: "14F · lift", room: "EX1", color: "#5b6b7b", legs: [
      {floor: "1F",  points: [[440,470],[425,395],[415,320],[365,262],[340,243],[420,285],[600,290],[715,300],[800,255],[900,230],[950,200]]},
      {floor: "14F", points: [[1175,200],[1120,255],[1100,435],[900,440],[610,445],[620,410],[615,255]]}
    ], steps: [
      {floor: "1F",  text: "From Registration, walk to the lift lobby."},
      {floor: "1F",  text: "Take the lift to 14F."},
      {floor: "14F", text: "Walk along the corridor to Auditorium 1 — Executive Session. Break (coffee & tea) is outside the door."}
    ]}
  ]
};
