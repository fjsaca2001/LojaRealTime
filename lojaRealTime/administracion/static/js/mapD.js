let map;
let map2;
let marcadores = [];
// crea un nuevo objeto `Date`
var today = new Date();
 
const setListener = () => {
    document.querySelectorAll("nVia").forEach()
}

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
        document.getElementById('vDetenidos').innerHTML = total;
        // obtener la fecha y la hora
        var fecha = today.toLocaleDateString('en-US');
        document.getElementById('fecha').innerHTML = "Fecha: " + fecha;
 
        /*
            Resultado: 1/27/2020, 9:30:00 PM
        */
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
        alert("No se encontraron vehiculos")
    }
};

const localizacionesTodas = async () => {
    try {

        const response = await fetch("getUbicacionesDash");
        const data = await response.json();
        const total = (Object.keys(data.vehiculos)).length;
        if (marcadores.length != 0) {
            eliminarMarcadores()
        }
        if (data.mensaje == "Correcto") {
            data.vehiculos.forEach(vehiculo => {
                posVehiculo = { lat: Number(vehiculo.latitud), lng: Number(vehiculo.longitud) }
                agregarMarcador(posVehiculo, vehiculo)
            });
        } else {
            alert("No se encontraron vehiculos")
        }

    } catch (e) {
        alert("No se encontraron vehiculos" + e)
    }
};


const marcarRutas = async () => {
    try {
        var objConfDR = {
            map: map2
        };
        const response = await fetch("getRutasMapaDash");
        const data = await response.json();
        var c = 1;
        if (data.mensaje == "Correcto") {
            data.vias.forEach(vias => {
                inicio = { lat: Number(vias.lat), lng: Number(vias.long) }
                html = ' <div class="seccioneCaracteristicas"><h3>'+ vias.velocidad +' Km/h</h3><p id="nombreVia" class="nVia" style="margin-bottom: 0px;">'+ vias.via +'</p></div> '
                document.getElementById('reemplazar'+c).innerHTML = html;
                var dr = new google.maps.DirectionsRenderer(objConfDR);
                var objConfDS = {
                    origin: inicio, //LatLong - String 
                    destination: vias.via,
                    travelMode: google.maps.TravelMode.DRIVING
                }
                var ds = new google.maps.DirectionsService();
                ds.route(objConfDS, funRutear);
                function funRutear(resultados, status){
                    //Muestra la linea entre a y b
                    if(status == 'OK'){
                        dr.setDirections(resultados);
                    }else{
                    }
                }
                c = c + 1;
            });
            
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        alert("No se encontraron rutas")
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
    marcarRutas()

    setInterval(() => {
        localizacionesTodas()
        var today = new Date();
        var hora = today.toLocaleTimeString('en-US');
        document.getElementById('hora').innerHTML = "Hora: " + hora;
    }, 5000);

    
    infoWindow = new google.maps.InfoWindow();
    setListener()
}


function eliminarMarcadores() {
    //1 se borran los marcadores antiguos
    agregarMarcadorMapa(null)
    //2 eliminar toda referencia a los marcadores antiguos
    marcadores = [];
}

function agregarMarcadorMapa(map) {
    for (let i = 0; i < marcadores.length; i++) {
        marcadores[i].setMap(map);
    }
}

function agregarMarcador(position, vehiculo) {
    const icon = {
        url: "http://127.0.0.1:8000/static/img/iconoTaxi.png", // url
        scaledSize: new google.maps.Size(30, 30), // scaled size
        origin: new google.maps.Point(0, 0), // origin
        anchor: new google.maps.Point(0, 0) // anchor
    };
    const marcador = new google.maps.Marker({
        position,
        map,
        icon,
    });
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

    marcadores.push(marcador);
}

