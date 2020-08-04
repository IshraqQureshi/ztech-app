$(document).ready(function(){

    $('#fingerprint_btn_1').click(function(e){
        e.preventDefault();
        register_fingerprint()
    });

});

function register_fingerprint(fingerprint_type=false)
{
    
    $.ajax({
        url: '/appcontrol/employees/ajax_register_fingerprint/',
        type: 'POST',        
        success: function(response){
            console.log(response)
        }
    })
}