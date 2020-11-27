$(document).ready(function(){

    $('#fingerprint_btn_1').click(function(e){
        e.preventDefault();
        $('.finger_print_popup').addClass('active');
        $('input[name=fingerprint_1]').val('')
        register_fingerprint()
    });

    $('#face_btn').click(function(e){
        e.preventDefault();
        // $('.finger_print_popup').addClass('active');
        let face_id = $(this).val()
        if(face_id == '')
        {
            face_id = 0;
        }
        register_face(face_id)
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

function register_face(face_id=false){
    
    let data = {};
    data.face_id = face_id;
    
    $.ajax({
        url: '/appcontrol/employees/ajax_register_face/',
        type: 'POST',        
        data: data,
        success: function(response){
            
            if ( response != '' )
            {
                $('input[name=face_id]').val(response.face_id)
            }
            
        }
    })
}