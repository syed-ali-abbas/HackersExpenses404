const searchField = document.querySelector('#searchField');
const tableOutput = document.querySelector('.table-output');
const appTable = document.querySelector('.app-table');
const paginationContainer = document.querySelector('.pagination-container');
const tableBody = document.querySelector('.table-body');
tableOutput.style.display='none';
searchField.addEventListener('keyup',(e)=>{
const searchValue = e.target.value;
if(searchValue.trim().length>0){
    tableBody.innerHTML='';
    paginationContainer.style.display='none';
    console.log(searchValue);
fetch('/search-expenses',{
body: JSON.stringify({searchText:searchValue}),
method:'POST',
})
.then((res)=>res.json())
.then((data)=>{
    console.log(data);
    tableOutput.style.display='block';
    appTable.style.display='none';
    if(data.length==0){
        tableOutput.innerHTML='No Record Found related to this search';
        // appTable.style.display='block';
        
    }
    else{
        
        data.forEach((element) => {
            tableBody.innerHTML+=`<tr>
            <td>${element.amount}</td>
            <td>${element.category}</td>
            <td>${element.descripption}</td>
            <td>${element.date}</td>
             </tr>`;
        });
        
        
    }
});
}
else{
    appTable.style.display='block';
    paginationContainer.style.display='block';
    tableOutput.style.display='none';

}

});