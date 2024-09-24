$('input[type="file"]').on('change', function(){
    var ext = $( this ).val().split('.').pop();
    if ($( this ).val() != '') {
      if(ext == "pdf"){
  
        if($(this)[0].files[0].size > 3000000){

          $(this).val('');
          alert("Se solicita un archivo no mayor a 4 MB. Por favor se sugiere verificar.");
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