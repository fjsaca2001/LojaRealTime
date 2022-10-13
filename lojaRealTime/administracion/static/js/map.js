let map;

const localizaciones = async()=>{
    try{
        // Consulta de datos para los valores del mapa
        const response = await fetch("getValoresMapa");
        const data = await response.json();
        const total = (Object.keys(data.vehiculos)).length;
        document.getElementById('puntosTrafico').innerHTML=total;
        console.log(total)
        let opacidad = 0
        
        if (data.mensaje == "Correcto"){
            data.vehiculos.forEach(vehiculo => {
                posVehiculo = {lat: Number(vehiculo.latitud), lng: Number(vehiculo.longitud)}
                if(vehiculo.velocidad < 4){
                    opacidad = 0.50
                    console.log("Velocidad: " + vehiculo.velocidad + "Opacidad: " + opacidad)
                }else if(vehiculo.velocidad < 7 && vehiculo.velocidad > 3){
                    opacidad = 0.20
                    console.log("Velocidad: " + vehiculo.velocidad + "Opacidad: " + opacidad)
                }else {
                    opacidad = 0.10
                    console.log("Velocidad: " + vehiculo.velocidad + "Opacidad: " + opacidad)
                }
                const svgMarker = {
                    path: "M 25, 50 a 25,25 0 1,1 50,0 a 25,25 0 1,1 -50,0",
                    fillColor: "red",
                    fillOpacity: opacidad,
                    strokeWeight: 0,
                    rotation: 0,
                    scale: 3,
                    anchor: new google.maps.Point(0,0),
                  };
                const marcador = new google.maps.Marker({
                    position: posVehiculo,
                    map: map,
                    icon: svgMarker
                }) 
            });
        }else{
            alert("No se encontraron vehiculos")
        }

    }catch (e){
        console.log(e)
        alert("No se encontraron vehiculos")
    }
};
/*
const cargaInicial = async () =>{
    await localizaciones();
};
*/
function initMap(){
    let loja = {lat: -3.99313, lng: -79.20422}
    map = new google.maps.Map(document.getElementById("map"),{
        center: loja,
        zoom: 18
    })
    localizaciones()
}
/*
window.addEventListener("load", async() => {
    await cargaInicial();
});
*/
