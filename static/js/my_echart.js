

    
function GetQueryValues() {
   
    var url = new URL(window.location.pathname, window.location.origin);

    var paramValue = document.getElementById("paramselect").value;

    sessionStorage.setItem("param", paramValue);

    url.searchParams.append("param", paramValue);

    window.location.href = url.toString();
    

}

function movepBar(pos) {
    //   var elem = document.getElementsByClassName("pMarker")[0];
      var elem = document.getElementsByClassName("pMarker")[0];
        elem.style.left = pos + "%"; 
        
  }

  
var updateFreq = 100;
const btn = document.querySelector("#map_play");
const btnbar = document.querySelector("#bar_play");

const btnStop = document.querySelector("#stop");
    
var intervalID = null;
var yyyy = 0
var barelem = document.getElementById("progressBar");
var elem = document.getElementsByClassName("pMarker")[0];
var pBar_delta = parseInt((barelem.scrollWidth - elem.scrollWidth)/(latest_year - start_year));
var pBar_delta = 100/(latest_year - start_year+1);

if (btn != null){
     
    updateFreq = 200;
}
else {
     
  updateFreq = 1000;
}

btnStop.addEventListener("click", function() {
    clearInterval(intervalID);
    yyyy=0;
    btnStop.style.display = "none";
    
    movepBar(0);

    if(window.location.pathname =="/top"){
        btnbar.innerText= "Play";
    
        option.series[0].data = dataset[latest_year];
        option.graphic.elements[0].style.text = latest_year;
        option.animationDurationUpdate = updateFreq;

        myChart.setOption(option);


                
    }
    else{
        btn.innerText = "Play";
    
        map_option = options[latest_year];
        map_option["tooltip"] = tooltip;
    
        myChart.setOption(map_option, true);
    }
});

if (btn!=null) {
btn.addEventListener("click",  function () {
    console.log(" process button click");
    
    years = Object.keys(options);
    if (yyyy == 0) {
        yyyy= years[0];
    }

    if (btn.innerText == "Play"){ 
        btn.innerText = "Pause";
        btnStop.style.display = "inline";
        intervalID = setInterval(setMap,updateFreq);
        
        function setMap() {
            if ( yyyy > years[years.length -1]){
                clearInterval(intervalID);
                yyyy = 0;
                btn.innerText = "Play";
                btnStop.style.display = "none";
                movepBar(0);
            }
            else{
                map_option = options[yyyy];
                // map_option["tooltip"] = tooltip;
                myChart.setOption(map_option, true);
                
                // var elem = document.getElementsByClassName("pMarker")[0];
                var elem = document.getElementsByClassName("pMarker")[0];
                var pos = elem.style.left.slice(0,elem.style.left.length-1);
                if (pos == ""){
                    pos= 0;
                }
                if(yyyy > start_year){
                    movepBar(parseFloat(pos) +pBar_delta);
                }
                yyyy++;
            }
        }
    }
    else {
        clearInterval(intervalID);
        btn.innerText = "Play";
    }

  
});
}

if (btnbar!=null) {
btnbar.addEventListener("click",  function () {
    console.log(" process button click");
    
    years = Object.keys(dataset);
    if (yyyy == 0) {
        yyyy= years[0];
    }

    if (btnbar.innerText == "Play"){ 
        btnbar.innerText = "Pause";
        btnStop.style.display = "inline";
        intervalID = setInterval(setMap,500);
        
        function setMap() {
            if ( yyyy > years[years.length -1]){
                clearInterval(intervalID);
                yyyy = 0;
                btnbar.innerText = "Play";
                btnStop.style.display = "none";
                movepBar(0);
            }
            else{
                option.series[0].data = dataset[yyyy];
                option.animationDurationUpdate = updateFreq;
                option.graphic.elements[0].style.text = yyyy;
                // map_option["tooltip"] = tooltip;

                myChart.setOption(option);
                
                // var elem = document.getElementsByClassName("pMarker")[0];
                var elem = document.getElementsByClassName("pMarker")[0];
                var pos = elem.style.left.slice(0,elem.style.left.length-1);
                if (pos == ""){
                    pos= 0;
                }
                if(yyyy > start_year){
                    movepBar(parseFloat(pos) +pBar_delta);
                }
                yyyy++;
            }
        }
    }
    else {
        clearInterval(intervalID);
        btnbar.innerText = "Play";
    }

  
});
}

function toggleHide(id) {
    var obj = document.getElementById(id);
            if (obj.style.visibility == 'visible') {
                obj.style.visibility = 'hidden';
            }
            else {
                obj.style.visibility = 'visible';
            }
        }