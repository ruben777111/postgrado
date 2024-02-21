btn.addEventListener('click', () => {
	console.log('btn clicked');
});

var $ = jQuery.noConflict();



function abrir_modal_edicion(url) {
	$('#edicion').load(url, function () {
		$(this).modal('show');
	});
}
function abrir_modal_creacion(url) {
	$('#creacion').load(url, function () {
		$(this).modal('show');
	});
}
function abrir_modal_eliminacion(url) {
	$('#eliminacion').load(url, function () {
		$(this).modal('show');
	});
}
function cerrar_modal_creacion() {
	$('#creacion').modal('hide');
}

function cerrar_modal_edicion() {
	$('#edicion').modal('hide');
}
function cerrar_modal_eliminacion() {
	$('#eliminacion').modal('hide');
}
function activarBoton() {
	if ($('#boton_creacion').prop('disabled')) {
		$('#boton_creacion').prop('disabled', false);
	} else {
		$('#boton_creacion').prop('disabled', true);
	}
}

function mostrarErroresCreacion(errores) {
	$('#errores').html("");
	let error = "";
	for (let item in errores.responseJSON.error) {
		error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error[item] + '</strong></div>';
	}
	$('#errores').append(error);
}
function mostrarErroresEdicion(errores) {
	$('#erroresEdicion').html("");
	let error = "";
	for (let item in errores.responseJSON.error) {
		error += '<div class = "alert alert-danger" <strong>' + errores.responseJSON.error[item] + '</strong></div>';
	}
	$('#erroresEdicion').append(error);
}

function notificacionError(mensaje) {
	Swal.fire({
		title: 'Error!',
		text: mensaje,
		icon: 'error'
	})
}

function notificacionSuccess(mensaje) {
	Swal.fire({
		title: 'Buen Trabajo!',
		text: mensaje,
		icon: 'success'
	})
}


function eliminarusuario(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Esta acción deshabilitará al usuario",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/maestrante_eliminar/" + id
			}
		})
}

function habilitarusuario(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Esta acción habilitará al usuario para el proceso de Tesis",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/maestrante_habilitar/" + id

			}
		})
}


function actividad01(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Registrar actividad",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/actividad_01/" + id
			}
		})
}
function habilitarnumero(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Esta acción habilitará el número del docente",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/habilitar_numero/" + id
			}
		})
}
function deshabilitarnumero(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Esta acción deshabilitará el número del docente",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/deshabilitar_numero/" + id
			}
		})
}
function habilitardocente(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Esta acción habilitará al docente",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/docente_habilitar/" + id
			}
		})
}
function eliminardocente(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Esta acción deshabilitará al docente",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/docente_eliminar/" + id
			}
		})
}
function asistencia(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Registrar asistencia usuario",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/asistencia/" + id
			}
		})
}

function eliminarperfiltesis(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "Esta acción deshabilitará al usuario",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/perfil_tesis_eliminar/" + id
			}
		})
}

function quitarlista(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Quitar de la lista ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/quitarlista/" + id
			}
		})
}

function avanceuno() {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Programar actividad ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	}).then((result) => {
		if (result.isConfirmed) {
			// Envía el formulario después de hacer clic en "Aceptar"
			document.getElementById("miFormularioavance").submit();
			Swal.fire({

				icon: 'success',
				title: 'Registro guardado correctamente',
				text: "Espere a que este mensaje se cierre automáticamente.",
				showConfirmButton: false,

			})
		}
	});
}
function improcedenciatema(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Tema del perfil de tesis improcedente ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/improcedencia_perfil/" + id
			}
		})
}
function registraravance(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Avance de tesis NO aprobada ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/registrar_avance/" + id
			}
		})
}
function registraravance2(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Avance de tesis NO aprobada ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/registrar_avance_2/" + id
			}
		})
}
function registraravanceaprobado(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Avance de tesis aprobada ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/registrar_avance_aprobado/" + id
			}
		})
}
function procedenciatema(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Tema del perfil de tesis procedente ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/procedencia_perfil/" + id
			}
		})
}
function tesisprocedente(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Tema de tesis procedente ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/procedencia_tesis/" + id
			}
		})
}
function tesisimprocedente(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Tema de tesis Improcedente ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/improcedencia_tesis/" + id
			}
		})
}
function procedenciareporte(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Reporte general aprobada ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/procedencia_reporte/" + id
			}
		})
}
function procedenciareportetribunalinterno(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Reporte general de tribunal interno aprobada ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/procedencia_reporte_tribunal_interno/" + id
			}
		})
}

function activarreporte2(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Activar reporte ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/activar_reporte_2/" + id

			}
		})
}
function activarreporte3(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Activar reporte ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/activar_reporte_3/" + id
			}
		})
}
function prorroga(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "¿ Habilitar al maestrante para prorroga ?",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#1D2939",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')

				window.location.href = "/usuario/habilitar_prorroga/" + id
			}
		})
}
function siguienteproceso(id) {
	Swal.fire({
		"title": "Estas seguro",
		"text": "esta acción no tiene reversa",
		"icon": "question",
		"showCancelButton": true,
		"cancelButtonText": "Cancelar",
		"confirmButtonText": "Confirmar",
		"reverseButtons": true,
		"confirmButtonColor": "#dc3545",
		"cancelButtonColor": "#dc3545"

	})
		.then(function (result) {
			if (result.isConfirmed) {
				Swal.fire('Realizado!', '', 'success')
				window.location.href = "/usuario/procesar_requisito/" + id
			}
		})
}

var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
	return new bootstrap.Tooltip(tooltipTriggerEl)
})
