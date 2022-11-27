document.addEventListener("DOMContentLoaded", function () {
    getGPSdata()
    getGPSdataDia()
});

const getGPSdataDia = () => {
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10

    // llamada cuando la fecha cambie
    document.getElementById('fechaGPS').value = ano + "-" + mes + "-" + dia;
    let fechaGPS = document.getElementById("fechaGPS");

    gpsDataDia(ano + "-" + mes + "-" + dia);

    fechaGPS.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        if (fechaSeleccionada < fechaHoy) {
            gpsDataDia(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday: "long", year: "numeric", month: "short", day: "numeric" }))
            document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
        }
    });
}

const gpsDataDia = async (fecha) => {
    try {
        const response = await fetch("getGPSdia/" + fecha);
        const data = await response.json();
        var c = 1;
        htmlTabla = "";
        if (data.mensaje == "Correcto") {
            data.dataGPS0.forEach(dispositivo => {
                if (cont % 2 == 0){
                    clase = ""
                }else{
                    clase = 'class="alt"'
                }
                htmlTabla = htmlTabla + "<tr "+ clase +"><td>" + dispositivo[1] + "</td><td>" + dispositivo[0] + "</td></tr>"
                cont = cont + 1
            });
            document.getElementById('reemplazarTablaNroGPS0').innerHTML = htmlTabla;
            graficarGPSdia(data.totalGPS1, data.totalGPS0)

        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        alert("No se encontraron rutas")
    }
}

const getGPSdata = async () => {
    try {
        const response = await fetch("getGPS");
        htmlTabla = ""
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            htmlTabla = htmlTabla + "<tr><td>" + data.totalGPS1 + " Dispositivos </td><td>" + data.totalGPS0 + " Dispositivos </td></tr>"
            document.getElementById('reemplazarTablaNroGPS').innerHTML = htmlTabla;
            htmlTabla = ""
            cont = 0
            data.dataGPS0.forEach(dispositivo => {
                if (cont % 2 == 0){
                    clase = ""
                }else{
                    clase = 'class="alt"'
                }
                htmlTabla = htmlTabla + "<tr "+ clase +"><td>" + dispositivo[1] + "</td><td>" + dispositivo[0] + "</td></tr>"
                cont = cont + 1
            });
            document.getElementById('reemplazarTablaNroGPS0').innerHTML = htmlTabla;
            
            graficarGps(data.totalGPS1, data.totalGPS0)

        } else {

            alert("No se encontraron datos")

        }

    } catch (e) {
        alert("No se encontraron Datos")
    }
};

function graficarGps(totalGPS1, totalGPS0){
    // Data retrieved from https://netmarketshare.com/
    // Build the chart
    Highcharts.chart('containerGPS', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Porcentaje de dispositivos - Uso GPS'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        accessibility: {
            point: {
                valueSuffix: '%'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: false
                },
                showInLegend: true
            }
        },
        series: [{
            name: 'Dispositivos',
            colorByPoint: true,
            data: [{
                name: 'GPS On',
                y: totalGPS1,
                sliced: true,
                selected: true
            },  {
                name: 'GPS Off',
                y: totalGPS0
            }]
        }]
    });

}

function graficarGPSdia(totalGPS1, totalGPS0){
    Highcharts.chart('containerGPSdia', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Porcentaje de dispositivos - Uso GPS'
        },
        xAxis: {
            categories: [
                'GPS On',
                'GPS Off'
            ],
            crosshair: true
        },
        yAxis: {
            title: {
                useHTML: true,
                text: 'Total de dispositivos'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.0f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: [{
            name: 'Uso GPS',
            data: [totalGPS1, totalGPS0],
            colorByPoint: true,
            showInLegend: false,
        }]
    });
}