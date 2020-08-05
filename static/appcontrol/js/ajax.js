$(document).ready(function(){

    $('#fingerprint_btn_1').click(function(e){
        e.preventDefault();
        $('.finger_print_popup').addClass('active');
        $('input[name=fingerprint_1]').val('')
        register_fingerprint()
    });

});

function register_fingerprint(fingerprint_type=false)
{
    $('.fingerprint_success').hide();   
    $.ajax({
        url: '/appcontrol/employees/ajax_register_fingerprint/',
        type: 'POST',        
        success: function(response){
            
            if ( response != '' )
            {
                $('.finger_print_popup').removeClass('active');

                $('.finger_print_success').addClass('active');
                setTimeout(() => {
                    $('.finger_print_success').removeClass('active');    
                }, 3000);
                // response = JSON.parse(response);
                $('input[name=fingerprint_1]').val(response.fingerprint_id)
                $('.fingerprint_success').show();
            }
            
        }
    })
}