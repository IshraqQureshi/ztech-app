$(document).ready(function(){

    $('#face_btn').click(function(e){
        e.preventDefault();
        let face_id = $(this).val()
        if(face_id == '')
        {
            face_id = 0;
        }
        register_face(face_id)
    });

});


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