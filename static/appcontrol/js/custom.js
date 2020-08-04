$(document).ready(function() {
    
    if( $('body').find('#userRolesData').length > 0 )
    {
        $('#userRolesData').DataTable();
    }
    
    if( $('body').find('.custom-file-input').length > 0 )
    {
        document.querySelector('.custom-file-input').addEventListener('change',function(e){
            var fileName = document.getElementById("myInput").files[0].name;
            var nextSibling = e.target.nextElementSibling
            nextSibling.innerText = fileName
        
            $("input[name^='file_']").val(fileName);
        })
    }
});

