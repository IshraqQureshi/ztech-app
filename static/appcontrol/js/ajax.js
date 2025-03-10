$(document).ready(function(){

    $('#face_btn').click(function(e){
        e.preventDefault();
        let user_id = $(this).data('user_id')
        if(user_id == '')
        {
            user_id = 0;
        }
        register_face(user_id)
    });

});

$(document).ready(function(){

    $('#capture_btn').click(function(e){
        e.preventDefault();
        let face_id = $(this).val()
        if(face_id == '')
        {
            face_id = 0;
        }
        capture_face(face_id)
    });

});


function register_face(user_id=false){
    
    let data = {};
    data.user_id = user_id;
    
    $.ajax({
        url: '/appcontrol/employees/ajax_register_face/',
        type: 'POST',        
        data: data,
        success: function(response){
            
            if ( response.status && confirm('Face registered successfully. Click OK to reload the page.') )
            {
                window.location.reload();
            }else {
                alert(response.message);
            }
            
        }
    })
}

function capture_face(face_id=false){
    
    let data = {};
    data.face_id = face_id;
    
    $.ajax({
        url: '/appcontrol/visitors/ajax_register_face/',
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