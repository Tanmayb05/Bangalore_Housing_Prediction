function getBathValue() {
    var uiBath = document.getElementsByName("uiBath");
    for(var i in uiBath) {
        if(uiBath[i].checked) {
        return parseInt(i)+1;
        }
    }
    return -1; //Invalid Value
}

function getBHKValue() {
    var uiBHK = document.getElementsByName("uiBHK");
    for(var i in uiBHK) {
        if(uiBHK[i].checked) {
            return parseInt(i)+1;
        }
    }
    return -1; //Invalid Value
}

function onClickedEstimatePrice() {
    console.log("Estimate price button clicked");
    var sqft = document.getElementById("uiSqft");
    var bhk = getBHKValue();
    var bath = getBathValue();
    var location = document.getElementById("uiLocation");
    var estPrice = document.getElementById("uiEstimatePrice");

    // Use this if not using nginx.
    // var url = "http://127.0.0.1:5000/predict_home_price"; 

    // Use this if using nginx.
    var url = "api/predict_home_price";

    $.post(url, {
        total_sqft: parseFloat(sqft.value),
        bhk: bhk,
        bath: bath,
        location: location.value
    },function(data, status) {
        console.log(data.estimated_price);
        estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + "Lakh</h2>";
    });
}

function onPageLoad() {
    console.log("document loaded");
    var url = "http://127.0.0.1:5000/get_location_names";
    $.get(url, function(data, status) {
        console.log("got response for get_location_names request");
        if(data) {
            var locations = data.locations;
            var uiLocation = document.getElementById("uiLocation");
            $('#uiLocation').empty();
            $('#uiLocation').append("Choose a Location Place");
            for(var i in locations) {
                var option = new Option(locations[i]);
                $('#uiLocation').append(option);
            }
        }
    });
}

window.onload = onPageLoad;