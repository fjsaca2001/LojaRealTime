let map;

const localizaciones = async()=>{
    try{
        const response = await fetch("getValoresMapa");
        const data = await response.json();
        //console.log(data)
        if (data.mensaje == "Correcto"){
            data.vehiculos.forEach(vehiculo => {
                posVehiculo = {lat: vehiculo.latitud, lng: vehiculo.longitud}
                const marcador = new google.maps.Marker({
                    position: posVehiculo,
                    map: map,
                }) 
            });
        }else{
            alert("No se encontraron vehiculos")
        }

    }catch (e){
        console.log(e)
    }
};

const cargaInicial = async () =>{
    await localizaciones();
};

function initMap(){
    let loja = {lat: -3.99313, lng: -79.20422}
    map = new google.maps.Map(document.getElementById("map"),{
        center: loja,
        zoom: 16
    })
    localizaciones()
}
