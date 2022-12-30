document.addEventListener("DOMContentLoaded", function () {
    getGPSdataDia()
    gpsDataConexion(0)
    getTemperatura()
    getTemperaturaGeneral()
    getAnalisisTemp()
    getConsumo()
    getConsumoGeneral()
    getBateriaAhora()
    getBateriaId()
    //graficarConexion()
    // 0 -> Wifi; 1 -> 3g; 2 -> 4g
    //idUsuarioBateria
});
function getBateriaId() {
    // llamada cuando cambie
    let idUsuarioBateria = document.getElementById("idUsuarioBateria");
    bateriaDataId('2731', 0);
    document.getElementById('idUsuarioBateria').value = '2731'

    idUsuarioBateria.addEventListener('change', function () {
        bateriaDataId(this.value,0)
    });
}
const bateriaDataId = async (idUsuario, btnTiempo) => {
    try {
        const response = await fetch("getBateria/" + idUsuario + "/" + btnTiempo);
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            graficarConsumoBateria(data.listaFechas, data.listaBateria, idUsuario)
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        alert("No se encontraron rutas")
    }
}
const getBateriaAhora = async () => {
    try {
        graficaBateriaPastel()
        const response = await fetch("getBateriaAhora/");
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            graficaBateriaPastel(data.mas50, data.menos50, data.igual50)
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        alert("No se encontraron rutas")
    }
}
function getConsumoGeneral() {
    // llamada cuando cambie
    graficarConsumoGeneral();
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10

    // llamada cuando la fecha cambie
    document.getElementById('fechaConsumoGeneral').value = ano + "-" + mes + "-" + dia;
    let fechaConsumoGeneral = document.getElementById("fechaConsumoGeneral");

    consumoDataGeneral(ano + "-" + mes + "-" + dia, 0);

    fechaConsumoGeneral.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        if (fechaSeleccionada < fechaHoy) {
            consumoDataGeneral(this.value, 0) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday: "long", year: "numeric", month: "short", day: "numeric" }))
            document.getElementById('fechaConsumoGeneral').value = ano + "-" + mes + "-" + dia;
        }
    });
}
const consumoDataGeneral = async (fecha, btnConsumo) => {
    try {
        const response = await fetch("getConsumoGeneral/" + fecha + "/" + btnConsumo);
        const data = await response.json();
        if (data.mensaje == "Correcto") {
            graficarConsumoGeneral(data.listaId, data.listaConsumo)
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        alert("No se encontraron rutas")
    }
}
function getConsumo() {
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10

    // llamada cuando la fecha cambie
    document.getElementById('fechaConsumoGeneral').value = ano + "-" + mes + "-" + dia;
    document.getElementById('fechaConsumoUsuario').value = ano + "-" + mes + "-" + dia;
    // llamada cuando cambie
    let idUsuarioConsumo = document.getElementById("idUsuarioConsumo");
    let horario = document.getElementById("horario");
    let fechaConsumoUsuario = document.getElementById("fechaConsumoUsuario");
    
    graficaTemperatura()
    consumoData('2731', 'manana', fechaConsumoUsuario.value);
    document.getElementById('idUsuarioConsumo').value = '2731'
    document.getElementById('horario').value = 'manana'

    idUsuarioConsumo.addEventListener('change', function () {
        consumoData(this.value, document.getElementById('horario').value, document.getElementById('fechaConsumoUsuario').value)
    });

    horario.addEventListener('change', function () {
        consumoData(document.getElementById('idUsuarioConsumo').value, this.value, document.getElementById('fechaConsumoUsuario').value)
    });

    fechaConsumoUsuario.addEventListener('change', function () {
        consumoData(document.getElementById('idUsuarioConsumo').value, this.value, document.getElementById('fechaConsumoUsuario').value)
    });

}
const consumoData = async (idUsuario, horario, fecha) => {
    try {
        const response = await fetch("getConsumo/" + idUsuario + "/" + horario + "/" + fecha + "/" );
        const data = await response.json();;
        if (data.mensaje == "Correcto") {
            graficarConsumo(data.listaConsumo, data.horas)
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
}

function getAnalisisTemp() {
    // llamada cuando cambie
    graficarAnalisisTemp();
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10

    // llamada cuando la fecha cambie
    document.getElementById('fechaAnalisisTemp').value = ano + "-" + mes + "-" + dia;
    let fechaAnalisisTemp = document.getElementById("fechaAnalisisTemp");

    temperaturaDataAnalisis(ano + "-" + mes + "-" + dia);

    fechaAnalisisTemp.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        if (fechaSeleccionada < fechaHoy) {
            temperaturaDataAnalisis(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday: "long", year: "numeric", month: "short", day: "numeric" }))
            document.getElementById('fechaAnalisisTemp').value = ano + "-" + mes + "-" + dia;
        }
    });
}
const temperaturaDataAnalisis = async (fecha) => {
    try {
        const response = await fetch("getTemperaturaAnalisis/" + fecha);
        const data = await response.json();;
        if (data.mensaje == "Correcto") {
            graficarAnalisisTemp(data.mas30, data.menos30, data.igual30, data.igual0)
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
}
function getTemperaturaGeneral() {
    // llamada cuando cambie
    graficarTemperaturaGeneral();
    fechaHoy = new Date();
    var mes = fechaHoy.getMonth() + 1; //obteniendo mes
    var dia = fechaHoy.getDate(); //obteniendo dia
    var ano = fechaHoy.getFullYear(); //obteniendo año
    if (dia < 10)
        dia = '0' + dia; //agrega cero si el menor de 10
    if (mes < 10)
        mes = '0' + mes //agrega cero si el menor de 10

    // llamada cuando la fecha cambie
    document.getElementById('fechaTempGen').value = ano + "-" + mes + "-" + dia;
    let fechaTempGen = document.getElementById("fechaTempGen");

    temperaturaDataGeneral(ano + "-" + mes + "-" + dia);

    fechaTempGen.addEventListener('change', function () {
        fechaSeleccionada = new Date(parseInt((this.value).split("-")[0]), parseInt((this.value).split("-")[1]) - 1, parseInt((this.value).split("-")[2]));
        if (fechaSeleccionada < fechaHoy) {
            temperaturaDataGeneral(this.value) // anio-mes-dia 2021-11-14
        } else {
            alert("La fecha debe ser menor al dia: " + fechaHoy.toLocaleDateString('es-es', { weekday: "long", year: "numeric", month: "short", day: "numeric" }))
            document.getElementById('fechaTempGen').value = ano + "-" + mes + "-" + dia;
        }
    });
}
const temperaturaDataGeneral = async (fecha) => {
    try {
        const response = await fetch("getTemperaturaGeneral/" + fecha);
        const data = await response.json();;
        if (data.mensaje == "Correcto") {
            graficarTemperaturaGeneral(data.rManana, data.rTarde, data.rNoche)
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
}
function getTemperatura() {
    // llamada cuando cambie
    let idUsuario = document.getElementById("idUsuario");
    graficaTemperatura()
    document.getElementById("idUsuario").value = '2731'
    temperaturaData('2731');

    idUsuario.addEventListener('change', function () {
        console.log(this.value)
        temperaturaData(this.value)
    });
}

const temperaturaData = async (idUsuario) => {
    try {
        const response = await fetch("getTemperatura/" + idUsuario);
        const data = await response.json();;
        if (data.mensaje == "Correcto") {
            graficaTemperatura(data.listaManana, data.listaTarde, data.listaNoche, data.listaDias)
        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
}

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
        var cont = 1;
        htmlTabla = "";
        if (data.mensaje == "Correcto") {
            data.dataGPS0.forEach(dispositivo => {
                if (cont % 2 == 0) {
                    clase = ""
                } else {
                    clase = 'class="alt"'
                }
                htmlTabla = htmlTabla + "<tr " + clase + "><td>" + dispositivo[1] + "</td><td>" + dispositivo[0] + "</td></tr>"
                cont = cont + 1
            });
            document.getElementById('reemplazarTablaNroGPS0').innerHTML = htmlTabla;

            htmlTabla = "<tr><td>" + data.totalGPS1 + " Dispositivos </td><td>" + data.totalGPS0 + " Dispositivos </td></tr>"
            document.getElementById('reemplazarTablaNroGPS').innerHTML = htmlTabla;

            graficarGPSdia(data.totalGPS1, data.totalGPS0)

        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
}

function btn7dias() {
    gpsDataConexion(0)
}
function btn15dias() {
    gpsDataConexion(1)
}
function btn1mes() {
    gpsDataConexion(2)
}
function btnActualizarPastel() {
    getBateriaAhora()
}

function mConsumo() {
    consumoDataGeneral(document.getElementById('fechaConsumoGeneral').value, 0)
}
function tConsumo() {
    consumoDataGeneral(document.getElementById('fechaConsumoGeneral').value, 1)
}
function minConsumo() {
    consumoDataGeneral(document.getElementById('fechaConsumoGeneral').value, 2)
}

function bateriaHora() {
    bateriaDataId(document.getElementById('idUsuarioBateria').value, 2)
}
function bateriaMediaHora() {
    bateriaDataId(document.getElementById('idUsuarioBateria').value, 1)
}
function bateriaCuartoHora() {
    bateriaDataId(document.getElementById('idUsuarioBateria').value, 0)
}

const gpsDataConexion = async (nroBtn) => {
    try {
        const response = await fetch("getConexion/" + nroBtn);
        const data = await response.json();
        if (data.mensaje == "Correcto") {

            graficarConexion(data.listaWifi, data.lista3G, data.lista4G, data.listaDias)

        } else {
            alert("No se encontraron rutas")
        }

    } catch (e) {
        console.log(e)
        alert("No se encontraron rutas")
    }
}

function graficarGPSdia(totalGPS1, totalGPS0) {
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
            }, {
                name: 'GPS Off',
                y: totalGPS0
            }]
        }]
    });
}

function graficarConexion(listaWifi, lista3G, lista4G, listaDias) {
    Highcharts.chart('containerConexion', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Tipo de conexión'
        },
        xAxis: {
            categories: listaDias,
            crosshair: true
        },
        yAxis: {
            title: {
                useHTML: true,
                text: 'Número de dispositivos'
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
            name: '4G',
            data: lista4G

        }, {
            name: '3G',
            data: lista3G

        }, {
            name: 'Wifi',
            data: listaWifi

        }]
    });
}

function graficaTemperatura(listaManana, listaTarde, listaNoche, listaDias) {
    Highcharts.chart('containerTemperatura', {

        title: {
            text: 'Temperatura por Usuario'
        },

        subtitle: {
            text: '°C'
        },

        yAxis: {
            title: {
                text: 'Temperatura (°C)'
            }
        },

        xAxis: {
            categories: listaDias,
        },

        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },

        series: [{
            name: 'Mañana',
            data: listaManana
        }, {
            name: 'Tarde',
            data: listaTarde
        }, {
            name: 'Noche',
            data: listaNoche
        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

    });
}

function graficarTemperaturaGeneral(rManana, rTarde, rNoche) {
    // Data retrieved from https://netmarketshare.com/
    // Build the chart

    Highcharts.chart('containerPromTempHorario', {
        chart: {
            type: 'column'
        },
        title: {
            text: 'Promedio Temperatura'
        },
        xAxis: {
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: 'Temperatura °C'
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: 'Temperatura: <b>{point.y:.1f} °C</b>'
        },
        series: [{
            colorByPoint: true,
            name: 'Population',
            data: [
                ['Mañana', rManana],
                ['Tarde', rTarde],
                ['Noche', rNoche]
            ],
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.1f}', // one decimal
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    });


    // Data retrieved from https://gs.statcounter.com/browser-market-share#monthly-202201-202201-bar

    // Create the chart

    // Set up the chart
}

function graficarAnalisisTemp(mas30, menos30, igual30, igual0) {
    new Highcharts.Chart({
        chart: {
            renderTo: 'containerAnalisisTem',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 15,
                beta: 15,
                depth: 50,
                viewDistance: 25
            }
        },
        xAxis: {
            categories: ['Mayores de 30°C', 'Menores de 30°C', 'Iguales a 30°C', 'Iguales a 0°C']
        },
        yAxis: {
            title: {
                enabled: false
            }
        },
        tooltip: {
            headerFormat: '<b>{point.key}</b><br>',
            pointFormat: 'Dispositivos: {point.y}'
        },
        title: {
            text: 'Análisis Temperatura'
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            column: {
                depth: 25
            }
        },
        series: [{
            data: [mas30, menos30, igual30, igual0],
            colorByPoint: true
        }]
    });
}

function graficarConsumo(listaConsumo, horas) {
    Highcharts.chart('containerConsumo', {

        title: {
            text: 'Consumo por usuario'
        },

        subtitle: {
            text: 'Mb'
        },

        yAxis: {
            title: {
                text: 'Nro Mb'
            }
        },

        xAxis: {
            title: {
                text: 'Horas'
            },
            categories: horas,
        },

        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },

        series: [{
            name: 'Consumo',
            data: listaConsumo
        }],
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }

    });
}

function graficarConsumoGeneral(listaId, listaConsumo) {
    new Highcharts.Chart({
        chart: {
            renderTo: 'containerConsumoGeneral',
            type: 'column',
            options3d: {
                enabled: true,
                alpha: 15,
                beta: 15,
                depth: 50,
                viewDistance: 25
            }
        },
        xAxis: {
            categories: listaId
        },
        yAxis: {
            title: {
                enabled: false
            }
        },
        tooltip: {
            headerFormat: '<b>{point.key}</b><br>',
            pointFormat: 'Consumo: {point.y}'
        },
        title: {
            text: 'Consumo General de todos los dispositivos'
        },
        legend: {
            enabled: false
        },
        plotOptions: {
            column: {
                depth: 25
            }
        },
        series: [{
            data: listaConsumo,
            colorByPoint: true
        }]
    });
}

function graficarConsumoBateria(listaFechas, listaBateria, idUsuario) {
    // Data retrieved from https://fas.org/issues/nuclear-weapons/status-world-nuclear-forces/
    Highcharts.chart('containerConsumoBateria', {
        chart: {
            type: 'area'
        },
        title: {
            text: 'Consumo de bateria'
        },
        xAxis: {
            title: {
                text: 'Tiempo '
            },
            categories: listaFechas,
        },
        yAxis: {
            title: {
                text: 'Porcentaje de bateria'
            },
        },
        tooltip: {
            pointFormat: 'Usuario {series.name} con <b>{point.y:,.0f}%</b> de bateria<br/>'
        },
        plotOptions: {
            area: {
                marker: {
                    enabled: true,
                    symbol: 'circle',
                    radius: 2,
                    states: {
                        hover: {
                            enabled: true
                        }
                    }
                }
            }
        },
        series: [{
            name: idUsuario,
            data: listaBateria,
        }]
    });

}

function graficaBateriaPastel(mas50, menos50, igual50){
    Highcharts.chart('containerBateriaPastel', {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: 'pie'
        },
        title: {
            text: 'Porcentaje de dispositivos - Bateria'
        },
        tooltip: {
            pointFormat: '{series.name}: <b>{point.percentage:.0f}%</b>'
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
                name: 'Bateria más 50%',
                y: mas50,
                sliced: true,
                selected: true
            }, {
                name: 'Bateria menos 50%',
                y: menos50
            }, {
                name: 'Bateria igual 50%',
                y: igual50,
                sliced: true
            }]
        }]
    });
}