const $formulario = document.getElementById('informe');

$formulario.addEventListener('submit',function(e){
	e.preventDefault();
    Swal.fire({
        "title":"¿Desea registrar?",
         
        "icon": "question",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Aceptar",
        "reverseButtons":true,
		"confirmButtonColor":"#1D2939",
		"cancelButtonColor":"#dc3545"
    
    })
    .then(function(result){
        if(result.isConfirmed){
            
            if($formulario.submit()){
                
                $formulario.submit();
                
            }
            
            Swal.fire({
         
              icon: 'success',
              title: 'Registro guardado correctamente',
              text: "Espere a que este mensaje se cierre automáticamente.",
              showConfirmButton: false,
             
            })
            
        }      


    })
});


