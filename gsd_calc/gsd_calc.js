var num_pattern = /^([1-9][0-9]*|0)([\.,][0-9]*)?$/;
var sensordb = new Array();

function upd(result) {
    $.each(result, function(i, field) { 
		if (i.match(/^btn/)) {		// update button text
			$('.' + i.substr(3)).attr('value', field);
		} else if (i.match(/^plh/)) {	// update placeholder text
			$('.' + i.substr(3)).attr('placeholder', field)
		} else {					// update other html text
			$('#' + i).html(field);
		}
    }); 
}

function fill(result) {
    // remove previous options
    $("#sensors").find("option").remove();
    // fill select with sensor names and sensordb
    $("#sensors").append($("<option>", {value: 0, text: "--- select sensor ---"}));
    var i = 1;
    $.each(result, function(sensor, data) {
        $("#sensors").append($("<option>", {value: i, text: sensor}));
        sensordb[i] = data;
        i++;
    });
}

$(document).ready(function () {
	// get local messages
	var lang = navigator.language.substr(0,2);
	if (! lang.match(/^en/)) {
		$.getJSON(lang + '.json', upd); 
    }
    // load sensor database
    $.getJSON("sensordb.json", fill);
	// calculate if button clicked
	$("#calc").click(gsd_calc);
    // fill sensor data
    $("#sensors").on('change', function () {
        var i = $("#sensors").val()
        if (i > 0) {
            $("#swidth:text").val(sensordb[i].swidth);
            $("#focal:text").val(sensordb[i].focal);
            $("#iwidth:text").val(sensordb[i].iwidth);
            $("#iheight:text").val(sensordb[i].iheight);
        }
    });

});
	
// calculation
function gsd_calc() {
    var swidth = $("#swidth").val().replace(',', '.');
    var focal = $("#focal").val().replace(',', '.');
    var height = $("#height").val().replace(',', '.');
    var iwidth = $("#iwidth").val().replace(',', '.');
    var iheight = $("#iheight").val().replace(',', '.');
    var asize = $("#asize").val().substr(0, 1);

    var gsd = (swidth * height * 100.0) / (focal * iwidth);
    var gwidth = gsd * iwidth / 100.0;
    var gheight = gsd * iheight / 100.0;
    var aruco = gsd * asize * 6;

	$("#gsd").val(gsd.toFixed(1));
	$("#gwidth").val((gwidth).toFixed(1));
	$("#gheight").val((gheight).toFixed(1));
	$("#aruco").val((aruco).toFixed(0));
}
