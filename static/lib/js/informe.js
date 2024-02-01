const $informe = document.getElementById('informe');

$informe.addEventListener('submit',function(e){
	e.preventDefault();
    Swal.fire({
        "title":"¿Desea guardar los cambios?",
         
        "icon": "question",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Aceptar",
        "reverseButtons":true,
        "confirmButtonColor":"#d81216",
        "cancelButtonColor":"#1D2939"
    
    })
    .then(function(result){
        if(result.isConfirmed){
            Swal.fire('Proceso realizado correctamente', '', 'success')
            $informe.submit();
        }
    })
});
function validarExt()
{
    var archivoInput = document.getElementById('tesis');
    var archivoRuta = archivoInput.value;
    var extPermitidas = /(.pdf)$/i;
    if(!extPermitidas.exec(archivoRuta)){
        Swal.fire('Error','Seleccionar archivo en formato PDF','error')
        archivoInput.value = '';
        return false;
    }

}


function vacio(){
    var archivoInput = document.getElementById('tesis');
      if(archivoInput.value == ""){
        Swal.fire('Error','No seleccionó ningun archivo','error')
       
      return false;
      }
   }


   function botonaceptar(){
    var archivoInput = document.getElementById('tesis');
    var archivoRuta = archivoInput.value;
    var extPermitidas = /(.pdf)$/i;
    if(!extPermitidas.exec(archivoRuta)){
        Swal.fire('Error','Seleccionar archivo en formato PDF','error')
        archivoInput.value = '';
        return false;
    }
    else{
        var opcion = confirm("¿ Desea guardar los cambios ?");
        if (opcion == true) {
            Swal.fire('Proceso realizado correctamente', '', 'success')
            return true;
        } else {
            return false;
        }
    }
	
   }