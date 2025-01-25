$(document).ready(function(){
    
    // Global Variables
    var face_verify = 0;
    let employee_id = false;
    localStorage.clear();

    // Section Aimnations
    setTimeout( () => {
        
        $('.welcome.section .content h1').animate({
            bottom: '-100vh',
        }, 1000, () => {
            $('.welcome.section .content h1').remove();
        } );

        $('.welcome.section .content h3').animate({
            top: '-100vh',
        }, 1000, () => {
            
            $('.welcome.section .content h3').remove();
            $('.welcome.section').animate({
                left: '-100vw',    
            });
            $('.welcome.section').animate({
                left: '-100vw',
            }, 1000, () => {
                $('.welcome.section').remove();
            });

            $('.who_you_are').animate({
                left: '0',
            }, 1000);

        } )

    }, 4000 )

    
    // Switch Between Sections
    $('.employee-btn').click(function(e){
        e.preventDefault();
        $('.face_recog').animate({
            left: '0',
        }, 500, () => {
            $('.face_recog_content').css('top', 0);
            $('.face_recog_img').css('top', 0);
        });
    })

    $('.visitor-btn').click(function(e){
        e.preventDefault();
        $('.face_capture').animate({
            left: '0',
        }, 500, () => {
            $('.face_recog_content').css('top', 0);
            $('.face_recog_img').css('top', 0);
        });
    })

    $('.back_btn').click(function(e){
        e.preventDefault();        
        $(this).parents('section').animate({
            left: '100vw',
        }, 1000);
    })


    // Ajax Events
    $('.face_btn').click(function(e){
        e.preventDefault();        

        if ( face_verify < 5 )
        {            
            $.ajax({
                url: '/frontend/face_recognition/',
                type: 'GET',        
                success: function(response){
                    if(response.status){
                        employee = response.employee
                        face_verify = 0;

                        $('.face_recog').animate({
                            left: '100vw',
                        }, 200, () => {});

                        $('.employee_details').animate({
                            left: '0vw',
                        }, 1000, () => {
                            

                            
                            $.ajax({
                                type: 'POST',
                                url: '/frontend/mark_attendance/',
                                data: {
                                    id: employee.id
                                },
                                success: function(res) {
                                    if(res.status){
                                        const employee_image = $('img').attr('src',`/${employee.image_dir}`)
                                        $('.employee_image').append(employee_image)
                                        $('#employee_name').text(employee.first_name + ' ' + employee.last_name)
                                        $('#punch').text(res.message)
                                        $('#punch_time').text(response.punch_time)
                                        $('#date').text(response.date)
                                        
                                        setTimeout(() => {
                                            location.reload();
                                        }, 5000);
                                    }
                                }
                            })
                        });
                    }else{
                        face_verify = face_verify + 1;
                    }
                }
            });
        }
        else{
            alert('Out Of Verifications')
        }
    })

    $('.capture_btn').click(function(e){
        e.preventDefault();        
                 
        $.ajax({
            url: '/frontend/face_capture/',
            type: 'POST',        
            success: function(response){
                if( response.status )
                {
                    if(response.save)
                    {
                        localStorage.setItem('visitor_face_id', response.face_id)
                    }
                    else
                    {
                        localStorage.setItem('visitor_face_id', response.visitor_id)
                    }

                                  
                }
                else{
                    alert('Please Try Again')
                }
            }
        });

    });
    
});