var map = L.map('mapid').setView([59.9386300, 30.3141300], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

var startMarker = L.marker([59.9386300, 30.3141300], {draggable:'true'}).addTo(map);
var targetMarker = L.marker([59.9276300, 30.3141300], {draggable:'true'}).addTo(map);


var rangeControl = L.control();
rangeControl.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'leaflet-control');
    div.innerHTML += '<input id="rangeinput" type="textbox" />';
    return div;
};
map.addControl(rangeControl);

var findControl = L.control();
findControl.onAdd = function (map) {
    var div = L.DomUtil.create('div', 'leaflet-control');
    div.innerHTML += '<button id="find">Find path</button>';
    return div;
};
map.addControl(findControl);

var input = document.getElementById("rangeinput");
var button = document.getElementById("find");
let line = L.polyline([]).addTo(map);

var buttonOnClick = function(){
  range = parseFloat(input.value);

  if (isNaN(range)) {
    alert("Wrong range format");
    return;
  }
  var requestBody = new Object();
  requestBody.path_len = range;
  
  var startNode = startMarker.getLatLng();
  requestBody.start = new Object();
  requestBody.start.lon = startNode.lng;
  requestBody.start.lat = startNode.lat;
  
  var targetNode = targetMarker.getLatLng();
  requestBody.target = new Object();
  requestBody.target.lon = targetNode.lng;
  requestBody.target.lat = targetNode.lat;

  var xhr = new XMLHttpRequest();
  xhr.open("POST", '/api/', true)
  xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');
  

  xhr.onload = function() {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        console.log(json);
        var nodes = json.nodes.map(function(obj){
          return [obj.lat, obj.lon]
        })
        console.log(line);
        line.setLatLngs(nodes);

      } else 
        if (xhr.status === 400){
        alert(JSON.parse(xhr.responseText).error);
      }
    }
  }

  xhr.send(JSON.stringify(requestBody));


}

button.onclick = buttonOnClick;
