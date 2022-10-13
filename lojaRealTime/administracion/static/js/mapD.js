let map;
const localizaciones = async()=>{
    try{
        const svgMarker = {
            path: "M 25, 50 a 25,25 0 1,1 50,0 a 25,25 0 1,1 -50,0",
            fillColor: "red",
            fillOpacity: 0.35,
            strokeWeight: 0,
            rotation: 0,
            scale: 3,
            anchor: new google.maps.Point(0,0),
          };
        
        const response = await fetch("getValoresMapaDash");
        const data = await response.json();
        const total = (Object.keys(data.vehiculos)).length;
        console.log(total)
        if (data.mensaje == "Correcto"){
            data.vehiculos.forEach(vehiculo => {
                posVehiculo = {lat: Number(vehiculo.latitud), lng: Number(vehiculo.longitud)}
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