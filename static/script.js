const citySelect = document.getElementById("city");
const dateInput = document.getElementById("date");
const predictBtn = document.getElementById("predictBtn");

const vars = ["Temperature_K","Precipitation_kgm2","Wind_speed_ms","Wind_dir_deg","Humidity_kgkg-1","Cloud_top_temp_K"];
let charts = {};
let map = L.map("map").setView([20,0],2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);
let cityMarker;
let lastDate = "";

async function fetchCities(){
  const res = await fetch("/capitals");
  const data = await res.json();
  data.forEach(c=>{
    const opt = document.createElement("option");
    opt.value = c.City;
    opt.text = c.City;
    citySelect.add(opt);
  });
}

async function fetchPrediction(city,date){
  const res = await fetch("/predict",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({city,date})
  });
  return await res.json();
}

function updateCharts(top3){
  vars.forEach(v=>{
    const ctx = document.getElementById(v+"_top3").getContext("2d");
    if(charts[v]) charts[v].destroy();
    const data = top3[v].map(x=>parseFloat(x));
    charts[v] = new Chart(ctx,{
      type:"line",
      data:{labels:["1","2","3"], datasets:[{label:v,data,fill:true,tension:0.4,borderColor:"#b39cff",backgroundColor:"rgba(179,156,255,0.2)"}]},
      options:{responsive:true,plugins:{legend:{display:false}},scales:{y:{beginAtZero:false}}}
    });
  });
}

async function updateMetrics(){
  const city = citySelect.value;
  let date = dateInput.value;

  if(!city) return;

  if(date) lastDate = date;
  else date = lastDate;

  const data = await fetchPrediction(city,date);

  if(data.error){
    vars.forEach(v=>{
      document.getElementById(v+"_avg").innerText = data.error;
    });
    return;
  }

  vars.forEach(v=>{
    let val = data[v+"_avg"];
    if(v==="Temperature_K" && val!==null) val = (val-273.15).toFixed(1)+" °C";
    if(v==="Cloud_top_temp_K" && val!==null) val = val.toFixed(1)+" °C";
    document.getElementById(v+"_avg").innerText = val!==null?val:"--";
  });

  const chartData = {};
  vars.forEach(v=>{
    let top = data[v+"_top3"];
    if(v==="Temperature_K") top = top.map(x=>((x-273.15).toFixed(2)));
    if(v==="Cloud_top_temp_K") top = top.map(x=>x.toFixed(2));
    chartData[v] = top;
  });
  updateCharts(chartData);

  if(cityMarker) map.removeLayer(cityMarker);
  cityMarker = L.marker([data.Latitude,data.Longitude]).addTo(map).bindPopup(city).openPopup();
  map.setView([data.Latitude,data.Longitude],5);

  dateInput.value = lastDate;
}

predictBtn.addEventListener("click",updateMetrics);
fetchCities();
