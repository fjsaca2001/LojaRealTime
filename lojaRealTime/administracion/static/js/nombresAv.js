/*
const localizacionesAV = async()=>{
    let geocoder;
    try{
        const response = await fetch("getValoresCongestion");
        const data = await response.json();
        const total = (Object.keys(data.vehiculos)).length;
        console.log(total)
        geocoder = new google.maps.Geocoder()
        if (data.mensaje == "Correcto"){
            data.vehiculos.forEach(vehiculo => {
                var latlong = {
                    lat : Number(vehiculo.latitud),
                    lng: Number(vehiculo.longitud)
                }
                geocodeLatLng(geocoder, latlong);
            });
        }else{
            alert("No se encontraron vehiculos")
        }

    }catch (e){
        console.log(e)
        alert("No se encontraron vehiculos")
    }
};

document.addEventListener("DOMContentLoaded", function(){
    localizacionesAV();
});

function geocodeLatLng(geocoder, latlong) {
    
    geocoder
      .geocode({ location: latlong })
      .then((response) => {
        if (response.results[0]) {
            console.log(response.results[0].formatted_address.split(","))
        } else {
          window.alert("No results found");
        }
      })
  }
*/