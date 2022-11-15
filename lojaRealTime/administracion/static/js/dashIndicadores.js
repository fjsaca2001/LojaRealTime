document.addEventListener("DOMContentLoaded", function () {
    getFecha()
    graficarSemanaHistorica()
});
function getFecha() {
    console.log("Funcion");
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10
    document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
    let fechaA = document.getElementById("fechaSemanalTrafico");
    valoresFechaSemanal(ano + "-" + mes + "-" + dia);
    fechaA.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        console.log((this.value).split("-")[0], (this.value).split("-")[1], (this.value).split("-")[2])
        if (fechaSeleccionada < fechaHoy) {
            valoresFechaSemanal(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday:"long", year:"numeric", month:"short", day:"numeric"}) )
            document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
        }
    });
}

const valoresFechaSemanal = async (fecha) => {
    try {
        const response = await fetch("getValoresDashboardIndicadoresHistoricos/" + fecha);
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            graficarSemanaHistorica(data.estadisticaManana, data.estadisticaTarde, data.estadisticaNoche); //dManana, dTarde, dNoche
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron datos")
    }
};


function graficarSemanaHistorica(estadisticaManana, estadisticaTarde, estadisticaNoche) {
    Highcharts.chart('containerHorarios', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Reporte de embotellamiento en base a horarios'
        },
        subtitle: {
            text: 'Horarios: ' + 'Mañana: 6am - 12pm; Tarde: 12pm - 19pm; Noche: 19pm - 12am'
        },
        xAxis: {
            categories: [
                'Lunes',
                'Martes',
                'Miercoles',
                'Jueves',
                'Viernes',
                'Sabado',
                'Domingo'
            ],
            crosshair: true
        },
        yAxis: {
            title: {
                useHTML: true,
                text: 'Número de embotellamientos'
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
            name: 'Mañana',
            data: estadisticaManana

        }, {
            name: 'Tarde',
            data: estadisticaTarde

        }, {
            name: 'Noche',
            data: estadisticaNoche

        }]
    });
}