/**
 * Created by LFarfan on 01/12/2016.
 */

//Document on ready -------------
$(function () {
    "use strict";
    getLocales();
});
// -- END DOCUEMTNT ON READY

//VARIABLES COMUNES
var id_curso;
var rangofechas = [];
var id_localambiente;
var id_ambiente = undefined;
var locales = [];
var local_selected = {};
var peaaula = [];
var ambientes = []
var ambiente_selected = []
//

$('#local').change(e => {
    "use strict";
    getRangoFechas($('#local').val());
    $('#tabla_pea').find('tbody').empty();
    local_selected = findInObject2(locales, $('#local').val(), 'id_local');
    setTimeout(getAmbientes($('#local').val(), 0), 1000);
});

$('#ambiente').change(e => {
    "use strict";
    id_ambiente = $('#ambiente').val();
    getPEA(id_localambiente);
});

$('#fechas').change(() => {
    "use strict";
    getAmbientes($('#local').val(), $.inArray($('#fechas').val(), rangofechas));
});

if (session.curso == '4') {
    $('#fechas').change(e => {
        if (id_localambiente !== undefined) {
            getPEA(id_localambiente)
        }
    });
} else {
    $('#div_fechas').hide();
}


function getLocales() {
    let ubigeo = `${session.ccdd}${session.ccpp}${session.ccdi}`;
    //let url = session.rol == '3' ? `${BASE_URL}localubigeo/${ubigeo}/${session.curso}/` : `${BASE_URL}localzona/${session.id}/`;
    let url = session.rol__id == 1 || session.rol__id == 3 || session.rol__id == 4 ? `${BASE_URL}localubigeo/${ubigeo}/${session.curso}/` : `${BASE_URL}localzona/${session.ccdd}${session.ccpp}${session.ccdi}/${session.curso}/${session.zona}`;
    "use strict";
    $.ajax({
        url: url,
        type: 'GET',
        success: response => {
            locales = response;
            setSelect_v2('local', response, ['id_local', 'nombre_local'])
        },
        error: error => {
            console.log('ERROR!!', error)
        }
    })
}

function getRangoFechas(id_local) {
    "use strict";
    $.ajax({
        url: `${BASEURL}/getRangeDatesLocal/${id_local}/`,
        type: 'GET',
        success: response => {
            setSelect_v2('fechas', response.fechas);
            rangofechas = response.fechas;
            $('#fechas').val(rangofechas[0]);
        },
        error: error => {
            console.log(error);
        }
    });
}

function getAmbientes(id_local, fecha = null) {
    //"use strict";
    let url = session.curso == 4 ? `${BASEURL}/localambiente/${id_local}/${fecha}` : `${BASEURL}/localambiente/${id_local}/`;
    $.ajax({
        url: url,
        type: 'GET',
        success: response => {
            ambientes = response.ambientes;
            id_curso = response.id_curso;
            setTable2('tabla_detalle_ambientes', response.ambientes, ['nombre_ambiente', 'numero', 'capacidad', 'cant_pea', {pk: 'id_localambiente'}]);
        },
        error: error => {
            console.log('ERROR!!', error);
        }
    })
}

function getPEA(id_ambiente) {
    "use strict";
    id_localambiente = id_ambiente;
    ambiente_selected = findInObject2(ambientes, id_ambiente, 'id_localambiente')
    let ajax_options = {};
    if (session.curso == '4') {
        ajax_options = {
            url: `${BASEURL}/getPeaCurso5/`,
            type: 'POST',
            data: {'id_localambiente': id_ambiente, fecha: $('#fechas').val()},
            success: '',
            error: ''
        }
    } else {
        ajax_options = {
            url: `${BASEURL}/peaaulabylocalambiente/${id_ambiente}`,
            type: 'GET',
            success: '',
            error: ''
        }
    }
    ajax_options['success'] = (response => {
        let html = '';
        peaaula = response;
        $('#tabla_pea').find('tbody').empty();
        $.each(response, (key, val) => {
            html += `<tr>`;
            html += `<td>${parseInt(key) + 1}</td>`;
            html += `<td>${val.id_pea.dni}</td>`;
            html += `<td>${val.id_pea.ape_paterno}</td>`;
            html += `<td>${val.id_pea.ape_materno}</td>`;
            html += `<td>${val.id_pea.nombre}</td>`;
            html += `<td>${val.id_pea.id_cargofuncional.nombre_funcionario}</td>`;
            html += `</tr>`;
        });
        $('#tabla_pea').find('tbody').html(html);
    });
    ajax_options['error'] = (error => {
        console.log('ERROR!!', error)
    });
    $.ajax(ajax_options);
}

function doAsignacion(show = false) {
    let ubigeo = `${session.ccdd}${session.ccpp}${session.ccdi}`;
    $.ajax({
        url: `${BASEURL}/asignacion/`,
        type: 'POST',
        data: {ubigeo: ubigeo, zona: session.zona, id_curso: session.curso},
        success: response => {
            console.log(response);
            $('#modal_pea_sobrante').unblock();
            show ? getSobrantes() : '';
            $('#local').trigger('change');
        },
        error: error => {
            console.log('ERROR!!', error)
            $('#modal_pea_sobrante').unblock();
        }
    })
}
function doAsignacionReserva() {
    "use strict";
    let ubigeo = `${session.ccdd}${session.ccpp}${session.ccdi}`;
    $.ajax({
        url: `${BASEURL}/asignacion/`,
        type: 'POST',
        data: {ubigeo: ubigeo, zona: `${session.zona}`, contingencia: 1, id_curso: session.curso},
        success: response => {
            $('#modal_pea_sobrante').unblock();
            getReserva();
        },
        error: error => {
            console.log('ERROR!!', error)
            $('#modal_pea_sobrante').unblock();
        }
    })
}

function getSobrantes() {
    "use strict";
    let ubigeo = `${session.ccdd}${session.ccpp}${session.ccdi}`;
    let _id_curso = session.curso;
    $('#tabla_pea_sobrante').DataTable();
    $('#tabla_pea_sobrante').dataTable().fnDestroy();
    $.ajax({
        url: `${BASEURL}/sobrantes_zona/`,
        type: 'POST',
        data: {ubigeo: ubigeo, zona: `${session.zona}`, id_curso: _id_curso, contingencia: 0},
        success: response => {
            $('#tabla_pea_sobrante').DataTable({
                "data": response,
                "columns": [
                    {"data": "dni"},
                    {"data": "ape_paterno"},
                    {"data": "ape_materno"},
                    {"data": "nombre"},
                    {"data": "cargo"},
                ]
            });
            $('#modal_pea_sobrante').modal('show');
        },
        error: error => {
            console.log('ERROR!!', error)
        }
    })
}

function getReserva() {
    "use strict";
    let ubigeo = `${session.ccdd}${session.ccpp}${session.ccdi}`;
    let _id_curso = session.curso;
    $('#tabla_pea_reserva').DataTable();
    $('#tabla_pea_reserva').dataTable().fnDestroy();
    $.ajax({
        url: `${BASEURL}/sobrantes_zona/`,
        type: 'POST',
        data: {ubigeo: ubigeo, zona: `${session.zona}`, id_curso: _id_curso, contingencia: 1},
        success: response => {
            $('#tabla_pea_reserva').DataTable({
                "data": response,
                "columns": [
                    {"data": "dni"},
                    {"data": "ape_paterno"},
                    {"data": "ape_materno"},
                    {"data": "nombre"},
                    {"data": "cargo"},
                ]
            });

            $('#modal_pea_reserva').modal('show');
        },
        error: error => {
            console.log('ERROR!!', error)
        }
    })
}

$('#btn_do_asignar_pea').on('click', function () {
    var light_4 = $('#modal_pea_sobrante');
    $(light_4).block({
        message: '<i class="icon-spinner4 spinner"></i><h5>Espere por favor, se esta realizando el proceso de asignación automática</h5>',
        overlayCSS: {
            backgroundColor: '#fff',
            opacity: 0.8,
            cursor: 'wait'
        },
        css: {
            border: 0,
            padding: 0,
            backgroundColor: 'none'
        }
    });
    $('#modal_pea_sobrante').modal('show');
    doAsignacion()
});

function redistribuirAula(id_localambiente) {
    alert_confirm(() => {
        $.ajax({
            url: `${BASEURL}/redistribuir_aula/${id_localambiente}`,
            type: 'GET',
            success: response => {
                doAsignacion();
                getPEA(id_localambiente);
            },
            error: error => {
                console.log('ERROR!!', error)
            }
        });

    }, 'Esta usted seguro de redistribuir la PEA de esta aula?')

}

function reporte_pea_asistencia_blanco() {
    "use strict";
    let html = `<tr><th rowspan="2">N°</th><th rowspan="2">APELLIDOS</th><th rowspan="2">NOMBRES</th><th rowspan="2">CARGO</th><th rowspan="2">ZONA</th>`;
    html += `</tr>`;

    $('#tabla_reporte_pea_asistencia').find('thead').html(html);
    set_reporte_pea_asistencia_blanco();
    $('#modal_reporte_pea_exportar').modal('show');
}

function set_reporte_pea_asistencia_blanco() {
    "use strict";
    let html = '';
    let pea_por_fecha = [];
    if (session.curso == 4) {
        pea_por_fecha = peaaula.filter(function (e) {
            return e.pea_fecha == $('#fechas').val();
        });
    } else {
        pea_por_fecha = peaaula;
    }
    pea_por_fecha.map((key, val) => {
        html += `<tr>`;
        html += `<td>${val + 1}</td>`;
        html += `<td>${key.id_pea.ape_paterno} ${key.id_pea.ape_materno}</td>`;
        html += `<td>${key.id_pea.nombre}</td>`;
        html += `<td>${key.id_pea.id_cargofuncional.nombre_funcionario}</td>`;
        html += `<td>${key.id_pea.zona}</td>`;
        html += `</tr>`;
    });
    $('#tabla_reporte_pea_asistencia').find('tbody').html(html);
    $('#descripcion_aula').text(session.curso__nombre_curso);
    $('#listado_nombre_local').text(local_selected.nombre_local)
    $('#listado_direccion_local').text(local_selected.nombre_via)
    $('#listado_fecha_local').text(local_selected.fecha_inicio)
    $('#listado_aula_local').text(ambiente_selected.numero)
}

$('#btn_exportar_evaluacion').on('click', e => {
    Imprimir($('#tabla_reporte_pea_asistencia').parent().html());
});