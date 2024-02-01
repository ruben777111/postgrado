const $formulariosegtesis = document.getElementById('formulariosegtesis');
const $formularioinforme = document.getElementById('formularioinforme');

const $informe = document.getElementById('informe');
$formulariosegtesis.addEventListener('submit',function(e){
	e.preventDefault();
    Swal.fire({
        "title":"Estas seguro",
        "text":"esta acción no tiene reversa",
        "icon": "question",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Confirmar",
        "reverseButtons":true,
        "confirmButtonColor":"#dc3545",
        "cancelButtonColor":"#1D2939"
    
    })
    .then(function(result){
        if(result.isConfirmed){
            Swal.fire('Proceso realizado correctamente', '', 'success')
            $formulariosegtesis.submit();

            
        }
    })
});
$formulariosegtesis.addEventListener('submit',function(e){
	e.preventDefault();
    Swal.fire({
        "title":"Estas seguro",
        "text":"esta acción no tiene reversa",
        "icon": "question",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Confirmar",
        "reverseButtons":true,
        "confirmButtonColor":"#dc3545",
        "cancelButtonColor":"#1D2939"
    
    })
    .then(function(result){
        if(result.isConfirmed){
            Swal.fire('Proceso realizado correctamente', '', 'success')
            $formulariosegtesis.submit();

            
        }
    })
});


$informe.addEventListener('submit',function(e){
	e.preventDefault();
    Swal.fire({
        "title":"Estas seguro",
        "text":"esta acción no tiene reversa",
        "icon": "question",
        "showCancelButton":true,
        "cancelButtonText":"Cancelar",
        "confirmButtonText":"Confirmar",
        "reverseButtons":true,
        "confirmButtonColor":"#dc3545",
        "cancelButtonColor":"#1D2939"
    
    })
    .then(function(result){
        if(result.isConfirmed){
            $informe.submit();
        }
    })
});