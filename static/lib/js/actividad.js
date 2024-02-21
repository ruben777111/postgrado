  // Función para inicializar SweetAlert
  function inicializarSweetAlert() {
    // Vincula SweetAlert al evento submit del formulario
    document.getElementById("informe").addEventListener("submit", function (event) {
      event.preventDefault(); // Evita que el formulario se envíe de manera predeterminada

      Swal.fire({
        title: '¿Estás seguro?',
        text: 'Registrar actividad',
        icon: 'warning',
        showCancelButton: true,
        cancelButtonText: "Cancelar",
        confirmButtonText: "Confirmar",
        reverseButtons: true,
        confirmButtonColor: "#dc3545",
        cancelButtonColor: "#1D2939"
      }).then((result) => {
        if (result.isConfirmed) {
          // Si el usuario confirma, envía el formulario
          this.submit();
          Swal.fire({
         
         icon: 'success',
         title: 'Registro guardado correctamente',
         text: "Espere a que este mensaje se cierre automáticamente.",
         showConfirmButton: false,
        
       })
        }
      });
    });
  }

  // Llama a la función para inicializar SweetAlert cuando se abre el modal
  $(document).ready(function () {
    inicializarSweetAlert();
    $("textarea").keyup(function() {  
      var height = $(this).prop("scrollHeight") + 2 + "px";
      $(this).css({"height": height});
  });
  });