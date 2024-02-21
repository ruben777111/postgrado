$('input[type="file"]').on('change', function(){
    var ext = $( this ).val().split('.').pop();
    if ($( this ).val() != '') {
      if(ext == "pdf"){
  
        if($(this)[0].files[0].size > 100048576){
          console.log("El documento excede el tamaño máximo");
          $('#modal-title').text('¡Precaución!');
          $('#modal-msg').html("Se solicita un archivo no mayor a 200MB. Por favor verifica.");
          $("#modal-gral").modal();           
          $(this).val('');
        }else{
          $("#modal-gral").hide();
        }
      }
      else
      {
        $( this ).val('');
        alert("Por favor, subir un archivo en formato PDF");
      }
    }
  });