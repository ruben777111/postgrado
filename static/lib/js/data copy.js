let dataTable;
let dataTableIsInitialized=false;
const initDataTable = async()=>{
    if(dataTableIsInitialized){
        dataTable.destroy();
    }
    await listaEvidencia();
    dataTable = $("#data").DataTable({})
    dataTableIsInitialized=true;
};


const listaEvidencia = async()=> {
    try{
        const response = await fetch("/usuario/listado_evidencia/");
        const data = await response.json();
        console.log(data)
        let content=``;
        data.evidencias.forEach((evidencia,index)=>{
            content +=`
            <tr>
                <td><input type='button' value='Edit' class='btn btn-warning btn-sm btn-edit' data-sid=" + x[i].id + "> <input type='button' value='Delete' class='btn btn-danger btn-sm btn-delete' data-sid=" + x[i].id +"> <td> 
                <td>${evidencia.nro_requisito}</td>
                <td>${evidencia.requisito}</td>
            <tr>
            `;

        });
        tableBody_users.innerHTML=content;
        }catch(ex){
            alert(ex);
    }
};
window.addEventListener("load",async()=>{
await initDataTable();

});