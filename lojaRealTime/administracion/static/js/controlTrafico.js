document.addEventListener("DOMContentLoaded", function () {
    //controlTransito()
    graficaVelicidadRango()
    graficar()
    //document.getElementById('intervaloActualizar').value = 30;
    //let intervalo = document.getElementById("intervaloActualizar");
    //actualizarTabla(intervalo)
    //actualizarTabla()
});


// Funciones para marcar vias con velocidades para Control Trafico
const controlTransito = () => {
    console.log("Entro")
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10

    // llamada cuando la fecha para la grafica semanal cambie
    document.getElementById('fechaVias').value = ano + "-" + mes + "-" + dia;
    let fechaVias = document.getElementById("fechaVias");

    graficar(ano + "-" + mes + "-" + dia);

    fechaVias.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        console.log((this.value).split("-")[0], (this.value).split("-")[1], (this.value).split("-")[2])
        if (fechaSeleccionada < fechaHoy) {
            marcarRutasCT(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday: "long", year: "numeric", month: "short", day: "numeric" }))
            document.getElementById('fechaSemanalTrafico').value = ano + "-" + mes + "-" + dia;
        }
    });
}
const marcarRutasCT = async (fecha) => {
    try {
        //html = ' '
        document.getElementById('reemplazar1').innerHTML = ' ';
        document.getElementById('reemplazar2').innerHTML = ' ';
        document.getElementById('reemplazar3').innerHTML = ' ';
        document.getElementById('reemplazar4').innerHTML = ' ';
        document.getElementById('reemplazar5').innerHTML = ' ';
        document.getElementById('reemplazar6').innerHTML = ' ';
        document.getElementById('reemplazar7').innerHTML = ' ';
        document.getElementById('reemplazar8').innerHTML = ' ';
        document.getElementById('reemplazar9').innerHTML = ' ';
        const response = await fetch("getRutasMapaDashFecha/" + fecha);
        const data = await response.json();
        var c = 1;
        if (data.mensaje == "Correcto") {
            data.vias.forEach(vias => {
                inicio = { lat: Number(vias.lat), lng: Number(vias.long) }
                html = ' <div class="grid-item"><h3>' + vias.velocidad + ' km/h</h3><p id="" style="margin-bottom: 0px;">' + vias.via + '</p></div>'
                document.getElementById('reemplazar' + c).innerHTML = html;
                c = c + 1;
            });

        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
};

// Funciones para marcar vias con velocidades para Control Trafico
const graficaVelicidadRango = () => {
    console.log("Entro graficar")
    fechaHoy = new Date();

    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10

    document.getElementById('fechaRangoMax').value = ano + "-" + mes + "-" + dia;
    var fechaMax = ano + "-" + mes + "-" + dia;
    fechaHistorica = new Date();
    fechaHistorica.setDate(fechaHoy.getDate() + (-7))

    var mes = fechaHistorica.getMonth() + 1; //obteniendo mes
    var dia = fechaHistorica.getDate(); //obteniendo dia
    var ano = fechaHistorica.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10
    
    document.getElementById('fechaRangoMin').value = ano + "-" + mes + "-" + dia;

    let fechaRangoMin = document.getElementById("fechaRangoMin");
    let fechaRangoMax = document.getElementById("fechaRangoMax");

    
    var fechaMin = ano + "-" + mes + "-" + dia;

    //getVelocidad(fechaMin, fechaMax);

    // llamada cuando la fecha para la grafica semanal cambie
    fechaRangoMin.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));

        fechaMaximaSeleccionada = new Date(parseInt((fechaMax).split("-")[0]), parseInt((fechaMax).split("-")[1]) - 1, parseInt((fechaMax).split("-")[2]))

        fechaMin = this.value;

        if (fechaSeleccionada < fechaHoy && fechaSeleccionada < fechaMaximaSeleccionada) {
            getVelocidad(fechaMin, fechaMax) // anio-mes-dia 2021-11-14
            //console.log("Correcto")
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday: "long", year: "numeric", month: "short", day: "numeric" }))
            document.getElementById('fechaRangoMin').value = fechaMin;
        }
    });

    fechaRangoMax.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));

        fechaMax = this.value;

        fechaMinimaSeleccionada = new Date(parseInt((fechaMin).split("-")[0]), parseInt((fechaMin).split("-")[1]) - 1, parseInt((fechaMin).split("-")[2]))

        if (fechaSeleccionada < fechaHoy && fechaSeleccionada > fechaMinimaSeleccionada) {
            getVelocidad(fechaMin, fechaMax) // anio-mes-dia 2021-11-14
            //console.log("Correcto 2")
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday: "long", year: "numeric", month: "short", day: "numeric" }))
            document.getElementById('fechaRangoMax').value = ano + "-" + mes + "-" + dia;
        }
    });
}


const actualizarTabla = () => {
    //var TiempoIntervalo
    /*TiempoIntervalo = setInterval(() => {
        getTaxis()
    }, 1000);*/
    //intervaloEjecutar(intervalo.value)
    /*intervalo.addEventListener('change', function () {
        intervaloValor = intervalo.value * 1000
        clearInterval(TiempoIntervalo);
        TiempoIntervalo = setInterval(() => {
            getTaxis()
        }, intervaloValor);
    });*/
    getTaxis()
}

const getTaxis = async () => {
    try {
        const datos = [];
        const response = await fetch("getUbicacionesCT");
        const data = await response.json();
        //var c = 1;
        if (data.mensaje == "Correcto") {
            html = ""
            //dataTabla(data.vehiculos)
            /*data.vehiculos.forEach(vehiculo => {
                datos.push([vehiculo.id_usuario,
                vehiculo.id_vehiculo,
                vehiculo.latitud,
                vehiculo.longitud,
                vehiculo.velocidad,
                vehiculo.temperatura,
                vehiculo.consumo,
                vehiculo.bateria])
                html = html + '<tr><td>' + vehiculo.id_usuario + '</td><td>' + vehiculo.id_vehiculo + '</td><td>' + vehiculo.latitud + '</td><td>' + vehiculo.longitud + '</td><td>' + vehiculo.velocidad + '</td><td>' + vehiculo.temperatura + '</td><td>' + vehiculo.consumo + '</td><td>' + vehiculo.bateria + '</td></tr>'
                //c = c + 1;
            });
            document.getElementById('reemplazarTabla').innerHTML = html;*/
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
};

const getVelocidad = async (fechaMinima, fechaMaxima) => {
    console.log("Fecha Min: " + fechaMinima + " Fecha Max: " + fechaMaxima)
    try {
        const response = await fetch("getRutasMapaDashFecha/" + fechaMinima + "/" + fechaMaxima);
        const data = await response.json();
        var c = 1;
        if (data.mensaje == "Correcto") {
            
        } else {
            alert("No se encontraron datos")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron Datos")
    }
};

function graficar(){
    Highcharts.chart('containerVelocidadRango', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Velocidad de taxis'
        },
        xAxis: {
            categories: [
                '2010',
                '2011',
                '2012',
                '2013',
                '2014',
                '2015',
                '2016',
                '2017',
                '2018',
                '2019',
                '2020',
                '2021'
            ],
            crosshair: true
        },
        yAxis: {
            title: {
                useHTML: true,
                text: 'Velocidad (km/h)'
            }
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                '<td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
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
            name: 'Dias de la semana',
            data: [13.93, 13.63, 13.73, 13.67, 14.37, 14.89, 14.56,
                14.32, 14.13, 13.93, 13.21, 12.16]
        }]
    });

    // Create the chart
    Highcharts.chart('containerVelocidadPastel', {
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Browser market shares. January, 2022'
    },
    subtitle: {
        text: 'Click the slices to view versions. Source: <a href="http://statcounter.com" target="_blank">statcounter.com</a>'
    },

    accessibility: {
        announceNewData: {
            enabled: true
        },
        point: {
            valueSuffix: '%'
        }
    },

    plotOptions: {
        series: {
            dataLabels: {
                enabled: true,
                format: '{point.name}: {point.y:.1f}%'
            }
        }
    },

    tooltip: {
        headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
        pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
    },

    series: [
        {
            name: "Browsers",
            colorByPoint: true,
            data: [
                {
                    name: "Chrome",
                    y: 61.04,
                    drilldown: "Chrome"
                },
                {
                    name: "Safari",
                    y: 9.47,
                    drilldown: "Safari"
                },
                {
                    name: "Edge",
                    y: 9.32,
                    drilldown: "Edge"
                },
                {
                    name: "Firefox",
                    y: 8.15,
                    drilldown: "Firefox"
                },
                {
                    name: "Other",
                    y: 11.02,
                    drilldown: null
                }
            ]
        }
    ],
    drilldown: {
        series: [
            {
                name: "Chrome",
                id: "Chrome",
                data: [
                    [
                        "v97.0",
                        36.89
                    ],
                    [
                        "v96.0",
                        18.16
                    ],
                    [
                        "v95.0",
                        0.54
                    ],
                    [
                        "v94.0",
                        0.7
                    ],
                    [
                        "v93.0",
                        0.8
                    ],
                    [
                        "v92.0",
                        0.41
                    ],
                    [
                        "v91.0",
                        0.31
                    ],
                    [
                        "v90.0",
                        0.13
                    ],
                    [
                        "v89.0",
                        0.14
                    ],
                    [
                        "v88.0",
                        0.1
                    ],
                    [
                        "v87.0",
                        0.35
                    ],
                    [
                        "v86.0",
                        0.17
                    ],
                    [
                        "v85.0",
                        0.18
                    ],
                    [
                        "v84.0",
                        0.17
                    ],
                    [
                        "v83.0",
                        0.21
                    ],
                    [
                        "v81.0",
                        0.1
                    ],
                    [
                        "v80.0",
                        0.16
                    ],
                    [
                        "v79.0",
                        0.43
                    ],
                    [
                        "v78.0",
                        0.11
                    ],
                    [
                        "v76.0",
                        0.16
                    ],
                    [
                        "v75.0",
                        0.15
                    ],
                    [
                        "v72.0",
                        0.14
                    ],
                    [
                        "v70.0",
                        0.11
                    ],
                    [
                        "v69.0",
                        0.13
                    ],
                    [
                        "v56.0",
                        0.12
                    ],
                    [
                        "v49.0",
                        0.17
                    ]
                ]
            },
            {
                name: "Safari",
                id: "Safari",
                data: [
                    [
                        "v15.3",
                        0.1
                    ],
                    [
                        "v15.2",
                        2.01
                    ],
                    [
                        "v15.1",
                        2.29
                    ],
                    [
                        "v15.0",
                        0.49
                    ],
                    [
                        "v14.1",
                        2.48
                    ],
                    [
                        "v14.0",
                        0.64
                    ],
                    [
                        "v13.1",
                        1.17
                    ],
                    [
                        "v13.0",
                        0.13
                    ],
                    [
                        "v12.1",
                        0.16
                    ]
                ]
            },
            {
                name: "Edge",
                id: "Edge",
                data: [
                    [
                        "v97",
                        6.62
                    ],
                    [
                        "v96",
                        2.55
                    ],
                    [
                        "v95",
                        0.15
                    ]
                ]
            },
            {
                name: "Firefox",
                id: "Firefox",
                data: [
                    [
                        "v96.0",
                        4.17
                    ],
                    [
                        "v95.0",
                        3.33
                    ],
                    [
                        "v94.0",
                        0.11
                    ],
                    [
                        "v91.0",
                        0.23
                    ],
                    [
                        "v78.0",
                        0.16
                    ],
                    [
                        "v52.0",
                        0.15
                    ]
                ]
            }
        ]
    }
    });

}

/*function dataTabla(data){
    console.log("Entro")
    console.log(Object.values(data))
    let vehiculos = { }
    $(document).ready( function () {
        $('#table_id').DataTable({
            data: Object.values(data),
            columns: [
                { title: "acuri"},
                { title: "altitud"},
                { title: "bateria"},
                { title: "conexion"},
                { title: "consumo"},
                { title: "fecha_hora"},
                { title: "direccion"},
                { title: "estado"},
                { title: "gps"},
                { title: "id_usuario"},
                { title: "id_vehiculo"},
                { title: "latitud"},
                { title: "longitud"},
                { title: "red"},
                { title: "temperatura"},
                { title: "velocidad"},
            ],

        });
    } );
}*/