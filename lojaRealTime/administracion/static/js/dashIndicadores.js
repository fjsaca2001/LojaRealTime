document.addEventListener("DOMContentLoaded", function () {
    getFechaDash()
    //Grafica barras horarios
    graficarSemanaHistoricaDash()
    // grafica de puntos dia
    graficarDiaHistoricoDash()
    // Grafica barras taxis
    graficarTaxisPorHorarios()
    // Grafica pastel
    graficaReporteSemanalHistoricoDash((0,0,0,0,0,0,0))
    
});

function getFechaDash() {
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10
    
    // llamada cuando la fecha para la grafica semanal cambie
    document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
    let fechaA = document.getElementById("fechaSemanalTrafico");
    valoresFechaSemanalDash(ano + "-" + mes + "-" + dia);

    fechaA.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        console.log((this.value).split("-")[0], (this.value).split("-")[1], (this.value).split("-")[2])
        if (fechaSeleccionada < fechaHoy) {
            valoresFechaSemanalDash(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday:"long", year:"numeric", month:"short", day:"numeric"}) )
            document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
        }
    });

    //Llamada cuando la fecha del grafico por dia cambie
    document.getElementById('fechaDiaTrafico').value = ano + "-" + mes + "-" + dia;
    let fechaD = document.getElementById("fechaDiaTrafico");
    valoresFechaDiaDash(ano + "-" + mes + "-" + dia);

    fechaD.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        console.log((this.value).split("-")[0], (this.value).split("-")[1], (this.value).split("-")[2])
        if (fechaSeleccionada < fechaHoy) {
            valoresFechaDiaDash(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday:"long", year:"numeric", month:"short", day:"numeric"}) )
            document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
        }
    });

    //Llamada cuando la fecha del grafico reporte semanal cambie
    document.getElementById('fechaDiaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
    let fechaSemanal = document.getElementById("fechaDiaSemanalTrafico");
    valoresFechaReporteDash(ano + "-" + mes + "-" + dia);

    fechaSemanal.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        console.log((this.value).split("-")[0], (this.value).split("-")[1], (this.value).split("-")[2])
        if (fechaSeleccionada < fechaHoy) {
            valoresFechaReporteDash(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday:"long", year:"numeric", month:"short", day:"numeric"}) )
            document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
        }
    });


    //Llamada cuando la fecha del grafico reporte semanal cambie
    document.getElementById('fechaTaxisConectados').value = ano + "-" + mes + "-" + dia;
    let fechaTaxisConectados = document.getElementById("fechaTaxisConectados");
    valoresFechaTaxisConectados(ano + "-" + mes + "-" + dia);

    fechaTaxisConectados.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        console.log((this.value).split("-")[0], (this.value).split("-")[1], (this.value).split("-")[2])
        if (fechaSeleccionada < fechaHoy) {
            valoresFechaTaxisConectados(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday:"long", year:"numeric", month:"short", day:"numeric"}) )
            document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
        }
    });

}
// llamada cuando la fecha para la grafica semanal cambie
const valoresFechaTaxisConectados = async (fecha) => {
    try {
        const response = await fetch("getValoresDashboardIndicadoresHistoricosTaxisActivos/" + fecha);
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            graficarTaxisPorHorarios(data.sumaManana, data.sumaTarde, data.sumaNoche); //dManana, dTarde, dNoche
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron datos")
    }
};

// llamada cuando la fecha para la grafica semanal cambie
const valoresFechaSemanalDash = async (fecha) => {
    try {
        const response = await fetch("getValoresDashboardIndicadoresHistoricos/" + fecha);
        const data = await response.json();
        dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
        htmlTabla = ''
        if (data.mensaje == "Correcto") {
            graficarSemanaHistoricaDash(data.estadisticaManana, data.estadisticaTarde, data.estadisticaNoche); //dManana, dTarde, dNoche
            for (let i = 0; i < dias.length; i++) {
                suma = (data.estadisticaManana[i] + data.estadisticaTarde[i] + data.estadisticaNoche[i])/3
                if (i % 2 == 0) {
                    clase = ""
                } else {
                    clase = 'class="alt"'
                }
                htmlTabla = htmlTabla + "<tr " + clase + "><td>" + dias[i] + "</td><td>" + Math.round(suma) + "</td></tr>"
            }
            document.getElementById('reemplazarTablaEmbotellamientos').innerHTML = htmlTabla;
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron datos")
    }
};

//Llamada cuando la fecha del grafico por dia cambie
const valoresFechaDiaDash = async (fecha) => {
    try {
        const response = await fetch("getValoresDashboardIndicadoresHistoricos2/" + fecha);
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            graficarDiaHistoricoDash(data.eManana, data.eTarde, data.eNoche); //dManana, dTarde, dNoche
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron datos")
    }
};

//Llamada cuando la fecha del grafico por dia cambie
const valoresFechaReporteDash = async (fecha) => {
    try {
        const response = await fetch("getValoresDashboardIndicadoresHistoricos3/" + fecha);
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            graficaReporteSemanalHistoricoDash(data.estadisticasSemana); //dManana, dTarde, dNoche
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron datos")
    }
};

// llamada cuando la fecha para la grafica semanal cambie
function graficarSemanaHistoricaDash(estadisticaManana, estadisticaTarde, estadisticaNoche) {
    Highcharts.chart('containerHorarios', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Reporte histórico de embotellamiento en base a horarios'
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

//Llamada cuando la fecha del grafico por dia cambie
function graficarDiaHistoricoDash(eManana, eTarde, eNoche){
    // Data retrieved https://en.wikipedia.org/wiki/List_of_cities_by_average_temperature
    Highcharts.chart('container-Dia', {
        chart: {
            type: 'spline'
        },
        title: {
            text: 'Embotellamientos según el día ingresado'
        },
        subtitle: {
            text: 'Horarios: ' + 'Mañana: 6am - 12pm; Tarde: 12pm - 19pm; Noche: 19pm - 12am'
        },
        xAxis: {
            categories: ['Mañana', 'Tarde', 'Noche'],
            accessibility: {
                description: 'Months of the year'
            }
        },
        yAxis: {
            title: {
                text: 'Número de embotellamientos'
            }
        },
        tooltip: {
            crosshairs: true,
            shared: true
        },
        plotOptions: {
            spline: {
                marker: {
                    radius: 4,
                    lineColor: '#666666',
                    lineWidth: 1
                }
            }
        },
        series: [{
            name: 'Embotellamientos',
            marker: {
                symbol: 'square'
            },
            data: [eManana,eTarde,eNoche]
        }]
    });
        
}

//Llamada cuando la fecha del grafico reporte semanal cambie
function graficaReporteSemanalHistoricoDash(estadisticasSemana){
    Highcharts.chart('container-semana', {
        chart: {
            type: 'pie',
            options3d: {
                enabled: true,
                alpha: 45
            }
        },
        title: {
            text: 'Reporte historico semanal de embotellamientos'
        },
        subtitle: {
            text: 'Reporte diario'
        },
        plotOptions: {
            pie: {
                innerSize: 100,
                depth: 45
            }
        },
        series: [{
            name: 'Numero de embotellamientos',
            data: [
                ['Lunes', estadisticasSemana[0]],
                ['Martes', estadisticasSemana[1]],
                ['Miercoles', estadisticasSemana[2]],
                ['Jueves', estadisticasSemana[3]],
                ['Viernes', estadisticasSemana[4]],
                ['Sabado', estadisticasSemana[5]],
                ['Domingo', estadisticasSemana[6]],
            ]
        }]
    });
}

function graficarTaxisPorHorarios(sumaManana, sumaTarde, sumaNoche){
    Highcharts.chart('containerTaxisPorHorarios', {
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Clasificación de taxis conectados'
        },
        xAxis: {
            categories: ['Mañana', 'Tarde', 'Noche'],
            title: {
                text: null
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Nro de taxis',
                align: 'high'
            },
            labels: {
                overflow: 'justify'
            }
        },
        tooltip: {
            valueSuffix: ''
        },
        plotOptions: {
            bar: {
                dataLabels: {
                    enabled: true
                }
            }
        },
        series: [{
            name: 'Taxis conectados',
            data: [sumaManana,sumaTarde,sumaNoche],
            colorByPoint: true,
            showInLegend: false,
        }]
    });
}