var $ = jQuery.noConflict();
$(document).ready(function() {

    table = $('#example').DataTable( {
        paging: false
    } );
     
    table.destroy();
     
    table = $('#example').DataTable( {
        searching: false
    } );
   $('#data').DataTable( {
       "language": {
           "lengthMenu": "Mostrar"+`
           <select class="custom-select custom-select-sm form-control form-control-sm">
            <option value ='10'>10</option>
            <option value ='25'>25</option>
            <option value ='50'>50</option>
            <option value ='100'>100</option>
            <option value ='-1'>Todos</option>
            `+" registros por página",
           "zeroRecords": "No hay registros disponibles",
           "info": "Mostrar _PAGE_ de _PAGES_ paginas",
           "infoEmpty": "No hay registros disponibles",
           "infoFiltered": "(filtrado de _MAX_ registros totales)",
           "search":"Buscar",
           "paginate":{
            'next':"Siguiente",
            'previous':"Anterior"
           }
       }
   } );
} );
