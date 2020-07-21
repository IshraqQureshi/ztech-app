$(document).ready(function() {
    
    if( $('body').find('#userRolesData').length > 0 )
    {
        $('#userRolesData').DataTable();
    }
    

});

document.querySelector('.custom-file-input').addEventListener('change',function(e){
    var fileName = document.getElementById("myInput").files[0].name;
    var nextSibling = e.target.nextElementSibling
    nextSibling.innerText = fileName
})