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


document.getElementById('tipo-1').addEventListener('click', function(e) {
   
    $(op1).prop('checked', $(this).prop("checked"));
    $(op2).prop('checked', false);
    $(op3).prop('checked', false);
    tipo1.hidden = false;  
    tipo2.hidden = true;
    tipo2.value = "";
    tipo3.hidden = true;
    tipo3.value = "";
    vigencia_inicio.hidden = true;
    vigencia_final.hidden = true;
    vigencia_inicio.value = "";
    vigencia_final.value = "";
  });
  
  document.getElementById('tipo-2').addEventListener('click', function(e) {
    $(op1).prop('checked', false);
    $(op2).prop('checked', $(this).prop("checked"));
    $(op3).prop('checked', false);
    tipo1.hidden = true;  
    tipo1.value = ""; 
    tipo2.hidden = false;
    tipo3.hidden = true;
    tipo3.value = "";
    vigencia_inicio.hidden = true;
    vigencia_final.hidden = true;
    vigencia_inicio.value = "";
    vigencia_final.value = "";
  });
  
  document.getElementById('tipo-3').addEventListener('click', function(e) {
    $(op1).prop('checked', false);
    $(op2).prop('checked', false);
    $(op3).prop('checked', $(this).prop("checked"));  
    tipo1.hidden = true;  
    tipo1.value = "";  
    tipo2.hidden = true;
    tipo2.value = "";
    tipo3.hidden = false;
    vigencia_inicio.hidden = false;
    vigencia_final.hidden = false;
  });