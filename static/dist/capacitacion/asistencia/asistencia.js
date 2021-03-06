/**
 * Created by lfarfan on 05/12/2016.
 */
$(function () {
    getLocales();
    updateUserSession();
});
var cierre;
function updateUserSession() {
    $.getJSON(`${BASEURL}/updateUserSession/${session.id}`, response => {
        localStorage.removeItem('usuario');
        localStorage.setItem('usuario', JSON.stringify(response[0]));
        cierre_actual = session.cierre;
        session = JSON.parse(localStorage.getItem('usuario'));
        cierre = session.cierre;
        if (session.curso == "6" || session.curso == "15" || session.curso == "16") {
            if (session.curso == "6") {
                dia_curso = 1
                getPeaCurso6(session.cierre_dia1);
            }
            $('#div_is_not_6').hide();

            if (session.rol__id == 3) {
                $('#btn_cierre_dia1').show();
            } else {
                $('#btn_cierre_dia1').remove();
            }
        } else {
            $('#div_is_6').hide();
            $('#div_is_not_6').show();
        }
    })
}

var turno;
var local = [];
var local_selected = {};
var rangofechas = [];
var peaaula = [];
var aula_selected;
var ambientes = [];
var ambiente_selected = [];
$('#local').change(e => {
    "use strict";
    let id_local = $('#local').val();
    getAmbientes(id_local);
    getRangoFechas(id_local);
});

$('#fechas').change(e => {
    "use strict";
    getPEA(aula_selected);
});


function disabledTurnos(turno) {
    if (turno == '0') {
        $('input[name^="turno_manana"]').map((key, val) => {
            "use strict";
            $(val).prop('disabled', false);
        });
        $('input[name^="turno_tarde"]').map((key, val) => {
            "use strict";
            $(val).prop('disabled', true);
        });
    } else if (turno == '1') {
        $('input[name^="turno_manana"]').map((key, val) => {
            "use strict";
            $(val).prop('disabled', true);
        });
        $('input[name^="turno_tarde"]').map((key, val) => {
            "use strict";
            $(val).prop('disabled', false);
        });
    }
}

function getRangoFechas(id_local) {
    "use strict";
    $.ajax({
        url: `${BASEURL}/getRangeDatesLocal/${id_local}/`,
        type: 'GET',
        success: response => {
            setSelect_v2('fechas', response.fechas);
            turno = response.turno;
            rangofechas = response.fechas;
            $('#fechas').val(rangofechas[0]);
        },
        error: error => {
            console.log(error);
        }
    });
}

function getLocales() {
    let ubigeo = `${session.ccdd}${session.ccpp}${session.ccdi}`;
    //let url = session.rol == '3' ? `${BASE_URL}localubigeo/${ubigeo}/${session.curso}/` : `${BASE_URL}localzona/${ubigeo}/${session.zona}/${session.curso}/`;
    //let url = session.rol == '3' ? `${BASE_URL}localubigeo/${ubigeo}/${session.curso}/` : `${BASE_URL}localzona/${session.id}/`;
    let url = session.rol__id == 1 || session.rol__id == 3 || session.rol__id == 4 ? `${BASE_URL}localubigeo/${ubigeo}/${session.curso}/` : `${BASE_URL}localzona/${session.ccdd}${session.ccpp}${session.ccdi}/${session.curso}/${session.zona}`;
    "use strict";
    $.ajax({
        url: url,
        type: 'GET',
        success: response => {
            local = response;
            setSelect_v2('local', response, ['id_local', 'nombre_local'])
        },
        error: error => {
            console.log('ERROR!!', error)
        }
    })
}
function getAmbientes(id_local) {
    "use strict";
    $.ajax({
        url: `${BASEURL}/localambiente/${id_local}/`,
        type: 'GET',
        success: response => {
            ambientes = response;
            setTable('tabla_detalle_ambientes', response.ambientes, ['numero', 'nombre_ambiente', 'capacidad', {pk: 'id_localambiente'}]);
        },
        error: error => {
            console.log('ERROR!!', error);
        }
    });
}

function setCheckedTurnoManana(obj, fecha, val) {
    "use strict";
    let checked = '';
    $.each(obj, (key, value) => {
        if (value.fecha == fecha) {
            checked = value.turno_manana == val ? 'checked' : '';
            value.turno_manana == val ? console.log(value) : '';
        }
    });
    return checked;
}

function setCheckedTurnoTarde(obj, fecha, val) {
    "use strict";
    let checked = '';
    $.each(obj, (key, value) => {
        if (value.fecha == fecha) {
            checked = value.turno_tarde == val ? 'checked' : '';
        }
    });
    return checked;
}

function getPEA(id_localambiente) {
    "use strict";
    aula_selected = id_localambiente;
    ambiente_selected = findInObject2(ambientes.ambientes, id_localambiente, 'id_localambiente');
    if ($.fn.DataTable.isDataTable('#tabla_pea')) {
        $('#tabla_pea').dataTable().fnDestroy();
    }
    $.ajax({
        url: `${BASEURL}/peaaulaasistencia/${id_localambiente}/`,
        type: 'GET',
        success: response => {
            peaaula = response;
            let fecha_selected = $('#fechas').val();
            let json = {};
            let html = '';
            let thead = `<tr>
                            <th>N°</th>
                            <th>Nombre Completo</th>
                            <th>Cargo</th>`;
            let pea_por_fecha = [];
            if (peaaula.length > 0) {
                if ('id_instructor' in response[0]) {
                    response[0].id_instructor != null ? $('#instructor').val(response[0].id_instructor).trigger("change") : $('#instructor').val(-1).trigger("change");
                }
                if (session.curso == 10) {
                    pea_por_fecha = peaaula.filter(function (e) {
                        return e.pea_fecha == $('#fechas').val();
                    });
                } else {
                    pea_por_fecha = peaaula;
                }

                $.each(pea_por_fecha, (key, val) => {
                    html += `<tr ${val.id_pea.baja_estado == 1 ? 'style="background-color: #f1a6a6"' : "" } ${val.id_pea.alta_estado == 1 ? 'style="background-color: #caeacb"' : "" }>`;
                    html += `<td>${key + 1}</td>`;
                    html += `<td>${val.id_pea.ape_paterno} ${val.id_pea.ape_materno} ${val.id_pea.nombre}</td><td>${val.id_pea.id_cargofuncional.nombre_funcionario}</td>`;

                    if (val.id_pea.baja_estado == 1) {
                        html += `<td></td><td></td>`;
                    } else {
                        html += `<td><div name="m${fecha_selected}" class="form-group">
                                        <input type="hidden" id="id_peaaula" name="id_peaaula${val.id_peaaula}" value="${val.id_peaaula}">
										<div class="checkbox checkbox-right">
											<label>
												<input type="radio" name="turno_manana${key}${fecha_selected}" ${setCheckedTurnoManana(val.peaaulas, fecha_selected, "0")} value="0">
												Puntual
											</label>
										</div>
										<div class="checkbox checkbox-right">
											<label>
												<input type="radio" name="turno_manana${key}${fecha_selected}" ${setCheckedTurnoManana(val.peaaulas, fecha_selected, "1")} value="1">
												Tardanza
											</label>
										</div>
										<div class="checkbox checkbox-right">
											<label>
												<input type="radio" name="turno_manana${key}${fecha_selected}" ${setCheckedTurnoManana(val.peaaulas, fecha_selected, "2")} value="2">
                                                Falta
											</label>
										</div>
									</div></td>`;
                        html += `<td><div name="${fecha_selected}" class="form-group">
                                        <input type="hidden" id="id_peaaula" name="id_peaaula${val.id_peaaula}" value="${val.id_peaaula}">
										<div class="checkbox checkbox-right">
											<label>
												<input type="radio" name="turno_tarde${key}${fecha_selected}" ${setCheckedTurnoTarde(val.peaaulas, fecha_selected, "0")} value="0">
												Puntual
											</label>
										</div>

										<div class="checkbox checkbox-right">
											<label>
												<input type="radio" name="turno_tarde${key}${fecha_selected}" ${setCheckedTurnoTarde(val.peaaulas, fecha_selected, "1")} value="1">
												Tardanza
											</label>
										</div>
										<div class="checkbox checkbox-right">
											<label>
												<input type="radio" name="turno_tarde${key}${fecha_selected}" ${setCheckedTurnoTarde(val.peaaulas, fecha_selected, "2")} value="2">
                                                Falta
											</label>
										</div>
									</div></td>`;
                    }
                    html += '</tr>';
                });
                thead += `<th>MAÑANA</th><th>TARDE</th>`;
                thead += `</tr>`;
                json.html = html;
            } else {
                $('#instructor').val(-1).trigger("change");
            }
            $('#tabla_pea').find('thead').html(thead);
            setTable('tabla_pea', json);
            disabledTurnos(turno);
            $('#tabla_pea').DataTable();
        },
        error: error => {
            console.log('ERROR!!', error)
        }
    })
}

function saveAsistencia() {
    "use strict";
    let tabla_pea = $('#tabla_pea').dataTable();
    let fecha_selected = $('#fechas').val();
    let div_data = tabla_pea.$('div[name="m' + fecha_selected + '"]');
    let data = [];
    let faltantes = 0;
    $.each(div_data, (key, val) => {
        let turno_manana = $(val).find('input[name^="turno_manana"]:checked').val();
        let id_peaaula = $(val).find(`input[name^="id_peaaula"]`).val();
        let input_tarde = tabla_pea.$(`input[name="id_peaaula${id_peaaula}"]`)[1];
        let turno_tarde = $(input_tarde).parent().find('input[name^="turno_tarde"]:checked').val();
        let json = {};
        if (turno_manana != undefined || turno_tarde != undefined) {
            json = {
                fecha: fecha_selected,
                turno_manana: turno_manana,
                turno_tarde: turno_tarde,
                id_peaaula: id_peaaula
            };
            data.push(json);
        } else {
            faltantes++;
        }
    });
    let title = 'Asistencia Completa, Guardar?';
    let type = 'success';
    if (faltantes > 0) {
        title = 'Aun tiene personas que ha marcado su asistencia, desea guardar?';
        type = 'warning';
    }
    swal({
        title: 'Guardar Asistencia',
        text: title,
        type: type,
        showCancelButton: true,
        confirmButtonColor: "#EF5350",
        confirmButtonText: "Si!",
        cancelButtonText: "No!",
        closeOnConfirm: true,
        closeOnCancel: true,
        showLoaderOnConfirm: true
    }, confirm => {
        if (confirm) {
            $.ajax({
                url: `${BASEURL}/update_peaaula/${aula_selected}/${$('#instructor').val()}/`,
                type: 'GET',
                success: function (response) {
                    getPEA(aula_selected);
                },
                error: function (error) {

                }
            });
            $.ajax({
                url: `${BASEURL}/save_asistencia/`,
                type: 'POST',
                data: JSON.stringify(data),
                success: function (response) {
                    swal({
                        title: "Asistencia Guardada con éxito!",
                        confirmButtonColor: "#2196F3"
                    });
                }
            });
        }
    });
}

function fn_darBaja() {
    "use strict";
    let id_pea = [];
    let inputs_checked_idpea = $('input[name="check_id_pea"]')
    $.each(inputs_checked_idpea, (key, val) => {
        if ($(val).is(':checked')) {
            id_pea.push($(val).val());
        }
    });
    $.ajax({
        url: `${BASEURL}/darBajaPea/`,
        type: 'POST',
        data: {'id_peas': id_pea},
        success: response => {
            $('#modal_pea_dar_baja').modal('hide');
            setTablaDarBaja();
        }
    });
}

function fn_darAlta() {
    "use strict";
    let id_pea = [];
    let inputs_checked_idpea = $('input[name="check_id_pea_dar_alta"]');
    $.each(inputs_checked_idpea, (key, val) => {
        if ($(val).is(':checked')) {
            id_pea.push($(val).val());
        }
    });
    $.ajax({
        url: `${BASEURL}/darAltaPea/`,
        type: 'POST',
        data: {'id_peas': id_pea},
        success: response => {
            $('#modal_pea_dar_alta').modal('hide');
            doAsignacion(1);
        }
    });
}

function darAlta() {
    "use strict";
    alert_confirm(fn_darAlta);
}
function darBaja() {
    "use strict";
    alert_confirm(fn_darBaja);
}

function getContingencia() {
    if ($.fn.DataTable.isDataTable('#tabla_pea_dar_alta')) {
        $('#tabla_pea_dar_alta').dataTable().fnDestroy();
    }
    $.ajax({
        url: `${BASEURL}/sobrantes_zona/`,
        type: 'POST',
        data: {
            ubigeo: `${session.ccdd}${session.ccpp}${session.ccdi}`,
            zona: `${session.zona}`,
            id_curso: `${session.curso}`,
            contingencia: 1
        },
        success: response => {
            $('#modal_pea_dar_alta').modal('show');
            let html = '';
            $('#tabla_pea_dar_alta').find('tbody').empty();
            $.each(response, (key, val) => {
                html += `<tr>`;
                html += `<td>${val.dni}</td>`;
                html += `<td>${val.ape_paterno}</td>`;
                html += `<td>${val.ape_materno}</td>`;
                html += `<td>${val.nombre}</td>`;
                html += `<td><input type="checkbox" name="check_id_pea_dar_alta" value="${val.id_pea}"></td>`;
                html += `</tr>`;
            });
            $('#tabla_pea_dar_alta').find('tbody').html(html);
            $('#tabla_pea_dar_alta').dataTable();

            $('#modal_pea_dar_alta').modal('show');
        },
        error: error => {
            console.log('ERROR!!', error)
        }
    })
}

function setTablaDarBaja() {
    getPEA(aula_selected);
    if ($.fn.DataTable.isDataTable('#tabla_pea_dar_baja')) {
        $('#tabla_pea_dar_baja').dataTable().fnDestroy();
    }
    if (peaaula.length) {
        let html = '';
        $('#tabla_pea_dar_baja').find('tbody').empty();
        $.each(peaaula, (key, val) => {
            html += `<tr>`;
            html += `<td>${val.id_pea.dni}</td>`;
            html += `<td>${val.id_pea.ape_paterno}</td>`;
            html += `<td>${val.id_pea.ape_materno}</td>`;
            html += `<td>${val.id_pea.nombre}</td>`;
            html += `<td><input type="checkbox" name="check_id_pea" value="${val.id_pea.id_pea}"></td>`;
            html += `</tr>`;
        });
        $('#tabla_pea_dar_baja').find('tbody').html(html);
        $('#tabla_pea_dar_baja').dataTable();
    } else {
        alert('Debe seleccionar un aula');
    }
}


function reporte_pea_asistencia() {
    "use strict";
    let html = `<tr><th rowspan="2">N°</th><th rowspan="2">APELLIDOS</th><th rowspan="2">NOMBRES</th><th rowspan="2">CARGO</th>`;
    let td_mt = `<tr>`;
    if (session.curso == 4) {
        rangofechas = [$('#fechas').val()]
    }
    $.each(rangofechas, (i, v) => {
        html += `<th colspan="2">${v.substring(0, 5)}</th>`;
        td_mt += `<th>M</th><th>T</th>`;
    });
    html += `</tr>`;
    td_mt += `</tr>`;
    html = html + td_mt;

    $('#tabla_reporte_pea_asistencia').find('thead').html(html);
    set_reporte_pea_asistencia();
    $('#modal_reporte_pea_exportar').modal('show');

}

function set_reporte_pea_asistencia() {
    "use strict";
    let html = '';
    let fechas_persona = [];
    let obj_fecha = {};

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
        fechas_persona = [];
        key.peaaulas.map(f => {
            fechas_persona.push(f.fecha);
        });
        if (session.curso == 4) {
            rangofechas = [$('#fechas').val()]
        }
        if (key.id_pea.baja_estado == 1) {
            html += `<td colspan=${(rangofechas.length) * 2}><span>DADO DE BAJA</span></td>`;
        } else {
            rangofechas.map(fecha => {
                if ($.inArray(fecha, fechas_persona) >= 0) {
                    obj_fecha = findInObject2(key.peaaulas, fecha, 'fecha');
                    switch (obj_fecha.turno_manana) {
                        case 0:
                            html += `<td>P</td>`;
                            break;
                        case 1:
                            html += `<td>T</td>`;
                            break;
                        case 2:
                            html += `<td style="background-color: red">F</td>`;
                            break;
                        default:
                            html += `<td></td>`;
                    }
                    switch (obj_fecha.turno_tarde) {
                        case 0:
                            html += `<td>P</td>`;
                            break;
                        case 1:
                            html += `<td>T</td>`;
                            break;
                        case 2:
                            html += `<td style="background-color: red">F</td>`;
                            break;
                        default:
                            html += `<td></td>`;
                    }
                    if (obj_fecha.baja_estado == 1) {
                        html += `<td>B</td>`;
                    }
                } else {
                    html += `<td></td><td></td>`;
                }
            });
        }
        html += `</tr>`;
    });
    $('#tabla_reporte_pea_asistencia').find('tbody').html(html);

    let grupo_curso4 = session.curso == 4 ? `GRUPO ${$.inArray($('#fechas').val(), rangofechas) + 1}` : '';
    $('#descripcion_aula').text(`CONTROL DE ASISTENCIA DIARIA - AULA ${ambiente_selected.numero} ${grupo_curso4}`);
    setDetalleCabecera()
}


function reporte_pea_asistencia_blanco() {
    "use strict";
    let html = `<tr><th rowspan="2">N°</th><th rowspan="2">APELLIDOS</th><th rowspan="2">NOMBRES</th><th rowspan="2">CARGO</th>`;
    let td_mt = `<tr>`;
    $.each(rangofechas, (i, v) => {
        html += `<th colspan="2">${v.substring(0, 5)}</th>`;
        td_mt += `<th>M</th><th>T</th>`;
    });
    html += `</tr>`;
    td_mt += `</tr>`;
    html = html + td_mt;

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
        rangofechas.map(fecha => {
            html += `<td></td><td></td>`;
        });
        html += `</tr>`;
    });
    $('#tabla_reporte_pea_asistencia').find('tbody').html(html);
    setDetalleCabecera()
}

$("#btn_exportar_evaluacion").on('click', function () {
    var uri = $("#div_listado_reporte").battatech_excelexport({
        containerid: "div_listado_reporte",
        datatype: 'table',
        returnUri: true
    });

    $(this).attr('download', 'listado_asistencia.xls').attr('href', uri).attr('target', '_blank');
    //Imprimir($('#tabla_reporte_pea_asistencia').parent().html());
});

function doAsignacion(alta, show = false) {
    let ubigeo = `${session.ccdd}${session.ccpp}${session.ccdi}`;
    let data = session.curso == 4 ? {
            ubigeo: ubigeo,
            zona: `${session.zona}`,
            id_curso: session.curso,
            alta: 1
        } : {
            ubigeo: ubigeo,
            zona: `${session.zona}`,
            id_curso: session.curso,
            alta: alta,
            aulaambiente: ambiente_selected.id_localambiente
        };
    $.ajax({
        url: `${BASEURL}/asignacion/`,
        type: 'POST',
        data: data,
        success: response => {
            $('#modal_pea_sobrante').unblock();
            show ? getSobrantes() : '';
            $('#local').trigger('change');
            getPEA(aula_selected);
        },
        error: error => {
            console.log('ERROR!!', error);
            $('#modal_pea_sobrante').unblock();
        }
    })
}

function setDetalleCabecera() {
    $('#descripcion_aula').text(session.curso__nombre_curso);
    $('#listado_nombre_local').text(local[0].nombre_local)
    $('#listado_direccion_local').text(local[0].nombre_via)
    $('#listado_fecha_local').text(local[0].fecha_inicio)
    $('#listado_aula_local').text(ambiente_selected.numero)
}


var pea_dia1 = [];
var pea_dia2 = [];
var contador = 0;
var dia_curso;


function getPeaCurso6(cierre) {
    $.getJSON(`${BASE_URL}peaCurso6/${session.ccdd}${session.ccpp}${session.ccdi}/${session.curso}/`, response => {
        pea_dia1 = response.pea_dia1
        pea_dia2 = response.pea_dia2
        if (cierre == 0) {
            $('#nombre_reporte').text('PRIMER DIA')
            renderPeaDia1();
        } else {
            $('#nombre_reporte').text('SEGUNDO DIA')
            renderPeaDia2();
        }
        getContador();

    });
}

function getContador() {
    contador = 0;
    if (session.cierre == 0) {
        $('input[name="asistio_dia1"]').map((key, value) => {
            if ($(value).is(':checked')) {
                contador++;
            }
        });
    } else if (session.cierre == 1) {
        $('input[name="asistio_dia2"]').map((key, value) => {
            if ($(value).is(':checked')) {
                contador++;
            }
        });
    }
    $('#contador').text(contador)
}

function renderPeaDia1() {
    let html = '';
    if ($.fn.DataTable.isDataTable('#pea_total_distrito')) {
        $('#pea_total_distrito').DataTable().destroy();
    }
    pea_dia1.map((key, val) => {
        let checked = '';
        if (key.asistio_dia == 1) {
            checked = 'checked = "checked"'
        } else {
            checked = '';
        }
        html += `<tr>`;
        html += `<td>${parseInt(val) + 1}</td><td>${key.ape_paterno}</td><td>${key.ape_materno}</td><td>${key.nombre}</td><td>${key.zona}</td><th>
                                        <div class="checkbox">
											<label>
												<input type="checkbox" name="asistio_dia1" value="${key.id_pea}" class="styled" ${checked}>
											</label>
										</div></th>`;
        html += `</tr>`;
    });
    $('#pea_total_distrito').find('tbody').html(html);
    $('#pea_total_distrito').DataTable({
        "paging": false
    });
    $('input[name="asistio_dia1"]').click(() => {
        getContador();
    })
}

function renderPeaDia2() {
    $('#btn_cierre_dia1').hide();
    let html = '';
    if ($.fn.DataTable.isDataTable('#pea_total_distrito')) {
        $('#pea_total_distrito').DataTable().destroy();
    }
    pea_dia2.map((key, val) => {
        let checked = '';
        if (key.asistio_dia == 2) {
            checked = 'checked = "checked"'
        } else {
            checked = '';
        }
        html += `<tr>`;
        html += `<td>${parseInt(val) + 1}</td><td>${key.ape_paterno}</td><td>${key.ape_materno}</td><td>${key.nombre}</td><td>${key.zona}</td><th>
                                        <div class="checkbox">
											<label>
												<input type="checkbox" name="asistio_dia2" class="styled" value="${key.id_pea}" ${checked}>
											</label>
										</div></th>`;
        html += `</tr>`;
    });
    $('#pea_total_distrito').find('tbody').html(html);
    $('#pea_total_distrito').DataTable({
        "paging": false
    });
    $('input[name="asistio_dia2"]').click(() => {
        getContador();
    })
}

function __saveCurso6(dia = 1) {
    let ids_return;
    if (dia == 1) {
        let id_dia1 = []
        $('input[name="asistio_dia1"]').map((key, value) => {
            if ($(value).is(':checked')) {
                id_dia1.push({'id': $(value).val(), 'asistio': 1})
            } else {
                id_dia1.push({'id': $(value).val(), 'asistio': null})
            }
        })
        return id_dia1
    } else {
        let id_dia2 = []
        $('input[name="asistio_dia2"]').map((key, value) => {
            if ($(value).is(':checked')) {
                id_dia2.push({'id': $(value).val(), 'asistio': 2})
            } else {
                id_dia2.push({'id': $(value).val(), 'asistio': null})
            }
        })
        return id_dia2
    }
}
function cerrarAsistenciaDia1() {
    alert_confirm(__cerrarAsistenciaDia1, 'Esta usted seguro de cerrar la asistencia para el primer día?')
}

function __cerrarAsistenciaDia1() {
    $.getJSON(`${BASEURL}/cerrarDia1Grupo6/${session.ccdd}/${session.ccpp}/${session.ccdi}/`, response => {
        console.log(response);
        getPeaCurso6(0);
    });
}

function saveCurso6() {
    let data = __saveCurso6(cierre == 0 ? 1 : 2);
    alert_confirm(() => {
        $('#div_is_6').block({
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
        $.post(`${BASEURL}/saveAsistenciaCurso6/`, {
            json_data: JSON.stringify(data),
        }, response => {
            $('#div_is_6').unblock();
            alert_success('Asistencia Guardada con éxito');
            updateUserSession()
        })
    }, 'Esta usted seguro de guardar la asistencia?')
}

