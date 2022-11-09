let map;
let map2 
const localizaciones = async () => {
    try {
        const svgMarker = {
            path: "M 25, 50 a 25,25 0 1,1 50,0 a 25,25 0 1,1 -50,0",
            fillColor: "red",
            fillOpacity: 0.35,
            strokeWeight: 0,
            rotation: 0,
            scale: 3,
            anchor: new google.maps.Point(0, 0),
        };
        const response = await fetch("getValoresMapaDash");
        const data = await response.json();
        const total = (Object.keys(data.vehiculos)).length;
        console.log(total)
        document.getElementById('vDetenidos').innerHTML=total;
        if (data.mensaje == "Correcto") {
            data.vehiculos.forEach(vehiculo => {
                posVehiculo = { lat: Number(vehiculo.latitud), lng: Number(vehiculo.longitud) }
                const marcador = new google.maps.Marker({
                    position: posVehiculo,
                    map: map,
                    icon: svgMarker
                })
                let html = `
                            <h3>Centro de información</h3>
                            <p><b>Latitud: </b>${vehiculo.latitud}</p>
                            <p><b>Longitud: </b>${vehiculo.longitud}</p>
                            <p><b>Hora: </b>${vehiculo.hora_actual}</p>
                            <p><b>Velocidad: </b>${vehiculo.velocidad} km/h</p>
                            `
                google.maps.event.addListener(marcador, "click", () => {
                    infoWindow.setContent(html);
                    infoWindow.open(map, marcador)
                })
            });
        } else {
            alert("No se encontraron vehiculos")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron vehiculos")
    }
};
const localizacionesTodas = async () => {
    try {
        const icon = {
            url: "http://127.0.0.1:8000/static/img/iconoTaxi.png", // url
            scaledSize: new google.maps.Size(50, 50), // scaled size
            origin: new google.maps.Point(0,0), // origin
            anchor: new google.maps.Point(0, 0) // anchor
        };
        const response = await fetch("getUbicacionesDash");
        const data = await response.json();
        const total = (Object.keys(data.vehiculos)).length;
        console.log(total)
        if (data.mensaje == "Correcto") {
            data.vehiculos.forEach(vehiculo => {
                posVehiculo = { lat: Number(vehiculo.latitud), lng: Number(vehiculo.longitud) }
                const marcador = new google.maps.Marker({
                    position: posVehiculo,
                    map: map,
                    icon: icon
                })
                let html = `
                            <h3>Centro de información</h3>
                            <p><b>Id Vehiculo: </b>${vehiculo.id_vehiculo}</p>
                            <p><b>Latitud: </b>${vehiculo.latitud}</p>
                            <p><b>Longitud: </b>${vehiculo.longitud}</p>
                            <p><b>Bateria: </b>${vehiculo.bateria}</p>
                            <p><b>Velocidad: </b>${vehiculo.velocidad} km/h</p>
                            `
                google.maps.event.addListener(marcador, "click", () => {
                    infoWindow.setContent(html);
                    infoWindow.open(map, marcador)
                })
            });
        } else {
            alert("No se encontraron vehiculos")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron vehiculos")
    }
};

const marcarRutas = async () => {
    try {
        const response = await fetch("getUbicacionesDash");
        const data = await response.json();
        const total = (Object.keys(data.vehiculos)).length;
        console.log(total)
        if (data.mensaje == "Correcto") {
            data.vehiculos.forEach(vehiculo => {
                posVehiculo = { lat: Number(vehiculo.latitud), lng: Number(vehiculo.longitud) }
                const marcador = new google.maps.Marker({
                    position: posVehiculo,
                    map: map,
                    icon: icon
                })
                let html = `
                            <h3>Centro de información</h3>
                            <p><b>Id Vehiculo: </b>${vehiculo.id_vehiculo}</p>
                            <p><b>Latitud: </b>${vehiculo.latitud}</p>
                            <p><b>Longitud: </b>${vehiculo.longitud}</p>
                            <p><b>Bateria: </b>${vehiculo.bateria}</p>
                            <p><b>Velocidad: </b>${vehiculo.velocidad} km/h</p>
                            `
                google.maps.event.addListener(marcador, "click", () => {
                    infoWindow.setContent(html);
                    infoWindow.open(map, marcador)
                })
            });
        } else {
            alert("No se encontraron vehiculos")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron vehiculos")
    }
};

function initMap() {
    let loja = { lat: -3.99313, lng: -79.20422 }
    map = new google.maps.Map(document.getElementById("map"), {
        center: loja,
        zoom: 18
    });
    map2 = new google.maps.Map(document.getElementById("map2"), {
        center: loja,
        zoom: 18
    });
    localizaciones()
    localizacionesTodas()
    //marcarRutas()
    infoWindow = new google.maps.InfoWindow();
}
