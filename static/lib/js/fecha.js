$(document).ready(function () {
 
    const fecha = new Date();
    fecha1=fecha.getDate() + "/" + (fecha.getMonth() + 1) + "/" + fecha.getFullYear()+ " " +fecha.getHours()+ ":" +fecha.getMinutes();
    $("#fecha").val(fecha1);

});