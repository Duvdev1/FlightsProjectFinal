$(document).ready(function()
{
    $.ajax({url:"/departures"}).then(
        function(flights){
            const flights_ = flights.flights;
            const departuresTable = $('#departures');
            departuresTable.find("tr:gt(0)").remove();
            $.each(flights, (i, flight) => {
                departuresTable.append(
                    '<tr><td class="fw-lighter">${flight.company}</td>'
                    /'<td class="fw-lighter">${flight.id}</td>'
                    /'<td class="fw-lighter">${flight.origin_country}</td>'
                    /'<td class"fw-lighter">${flight.destination_country}</td>'
                    /'<td class="fw-lighter">${flight.departure_time}</td>')
                })
            }
            ,function(err){
                console.error(err);
            });
});

$(document).ready(function()
{
    $.ajax({url:"/landing"}).then(
        function(flights){
            let landingsTable = $('#landings')
            landingsTable.find("tr:gt(0)").remove()
            $.each(flights, (i, flight) => {
                landingsTable.append(
                    '<tr><td class="fw-lighter">${flight.company}</td>'
                    /'<td class="fw-lighter">${flight.id}</td>'
                    /'<td class="fw-lighter">${flight.origin_country}</td>'
                    /'<td class"fw-lighter">${flight.destination_country}</td>'
                    /'<td class="fw-lighter">${flight.landing_time}</td>')
                })
            }
            ,function(err){
                console.error(err);
            });
});

$(document).ready(function()
{
    $.ajax({url:"/flights"}).then(
        function(flights){
            let landingsTable = $('#flights')
            landingsTable.find("tr:gt(0)").remove()
            $.each(flights, (i, flight) => {
                landingsTable.append(
                    '<tr><td class="fw-lighter">${flight.company}</td>'
                    /'<td class="fw-lighter">${flight.id}</td>'
                    /'<td class="fw-lighter">${flight.origin_country}</td>'
                    /'<td class"fw-lighter">${flight.destination_country}</td>'
                    /'<td class="fw-lighter">${flight.landing_time}</td>')
                })
            }
            ,function(err){
                console.error(err);
            });
});
