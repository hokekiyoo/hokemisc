function* zip(...args) {
  const length = args[0].length;

  // 引数チェック
  for (let arr of args) {
    if (arr.length !== length) {
      throw "Lengths of arrays are not eqaul.";
    }
  }
  for (let index = 0; index < length; index++) {
    let elms = [];
    for (arr of args) {
      elms.push(arr[index]);
    }
    yield elms;
  }
}

function initMap() {
  const pattern = 2; // 1が同じ方法で違う時間 2が同じ時間で違う方法
  const centers = {
    london: { lat: 51.519763556894745, lng: -0.12634440352170292 },
    caddi: { lat: 35.702543252116335, lng: 139.78857930148436 },
    prague: { lat: 50.130828242430816, lng: 14.436294767800266 },
  };
  center = centers.caddi;

  if (pattern === 1) {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: center,
      mapTypeId: "terrain",
    });
    k = "bicycling";
    const w1 = caddi_600[k];
    const w2 = caddi_1200[k];
    const w3 = caddi_1800[k];
    const w4 = caddi_3600[k];
    const w5 = caddi_10800[k];
    const w6 = caddi_86400[k];
    let ws = [w1, w2, w3, w4, w5, w6];
    let isolines = [];
    for (let i = 0; i < ws.length; i++) {
      let coords = [];
      for (let [lat, lng] of zip(ws[i]["lat"], ws[i]["lng"])) {
        coords.push({ lat: lat, lng: lng });
      }
      isolines.push(coords);
    }
    let maps = [];
    for (let i = 0; i < ws.length; i++) {
      let mp = new google.maps.Polygon({
        paths: isolines[i],
        strokeColor: "#F00",
        fillColor: "#F00",
        fillOpacity: 0.05,
        strokeOpacity: 1 - 0.2 * i,
      });
      maps.push(mp);
    }
    for (let i = 0; i < ws.length; i++) {
      maps[i].setMap(map);
    }
  } else {
    const map = new google.maps.Map(document.getElementById("map"), {
      zoom: 12,
      center: center,
      mapTypeId: "terrain",
    });

    const london = london_1800;
    ws = [
      london["walking"],
      london["bicycling"],
      london["driving"],
      london["transit"],
    ];
    let cs = ["#ff1744", "#2979ff", "#009688", "#ff9100"];
    let isolines = [];
    for (let i = 0; i < ws.length; i++) {
      let coords = [];
      for (let [lat, lng] of zip(ws[i]["lat"], ws[i]["lng"])) {
        coords.push({ lat: lat, lng: lng });
      }
      isolines.push(coords);
    }
    let maps = [];
    for (let i = 0; i < ws.length; i++) {
      let mp = new google.maps.Polygon({
        paths: isolines[i],
        fillColor: cs[i],
        fillOpacity: 0.1,
        strokeColor: cs[i],
      });
      maps.push(mp);
    }
    for (let i = 0; i < ws.length; i++) {
      maps[i].setMap(map);
    }
  }
}
