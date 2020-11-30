$(document).ready(function(){
    
    // Global Variables
    var finger_verify = 0;
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
                        employee_id = response.employee_id
                        
                        $('.face_recog').animate({
                            left: '-100vw',
                        }, 1000, () => {

                            $('.finger-print').animate({
                                left: '0',
                            }, 500, () => {
                                $('.finger_content').css('top', 0);
                                $('.finger_img').css('top', 0);
                            }); 

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

    $('.finger-btn').click(function(e){

        e.preventDefault();        

        if ( finger_verify < 5 )
        {
            $('.popUp').addClass('active');

            $.ajax({
                url: '/frontend/finger_print_verification/',
                type: 'POST',        
                success: function(response){
                    if( response.employee_name )
                    {                        
                        if(response.employee_faceId)
                        {
                            $('#employee_name').text(response.employee_name);
                            $('#punch_time').text(response.punch_in);
                            $('#date').text(response.date);
                            $('#punch').text('Punch Out Time');
                            if(response.punch_type)
                            {
                                $('#punch').text('Punch In Time');
                            }
                            $('.finger-print.section').animate({
                                left: '-100vw',
                            }, 1000);
                    
                            $('.employee_details.section').animate({
                                right: '0',
                            }, 1000);
                        }
                        else
                        {
                            alert('Face and Finger Not Matched!!')
                        }
                        
                    }
                    else{
                        finger_verify = finger_verify + 1;
                        // alert(finger_verify)
                        alert('Unknown Finger Verification, Please Try Again')
                    }

                    $('.popUp').removeClass('active');
                },
                error: function(){                    
                    finger_verify = finger_verify + 1;
                    alert('Unknown Finger Verification, Please Try Again')
                    $('.popUp').removeClass('active');
                }
            })
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

                    $('.finger-capture').animate({
                        left: '0',
                    }, 500, () => {
                        $('.finger_recog_content').css('top', 0);
                        $('.finger_recog_img').css('top', 0);
                    });                    
                }
                else{
                    alert('Please Try Again')
                }
            }
        });

    });
    
    $('.finger-capture-btn').click(function(e){

        e.preventDefault();                
        $('.popUp').addClass('active');

        $.ajax({
            url: '/frontend/finger_print_capture/',
            type: 'POST',        
            success: function(response){
                if(response.status)
                {
                    if(response.save)
                    {
                        localStorage.setItem('visitor_finger', response.fingerprint_id)                        
                    }
                    else{
                        localStorage.setItem('visitor', JSON.stringify(response.visitor))                        
                    }

                    $('.visitor-form').animate({
                        left: '0',
                    }, 1000);

                    let face_id = localStorage.getItem('visitor_face_id')
                    let visitor_finger = localStorage.getItem('visitor_finger')
                    let visitor = localStorage.getItem('visitor')

                    $('input[name=face_id]').val(face_id)
                    $('input[name=fingerprint_1]').val(visitor_finger)
                    $('input[name=fingerprint_2]').val(visitor_finger)
                    
                    if( visitor != null )
                    {
                        visitor = JSON.parse(visitor)

                        $('input[name=first_name]').val(visitor.first_name)
                        $('input[name=last_name]').val(visitor.last_name)
                        $('input[name=email]').val(visitor.email)
                        $('input[name=nic_number]').val(visitor.nic_number)
                        $('input[name=phone_number]').val(visitor.phone_number)
                        $('input[name=address]').val(visitor.address)
                    }

                    
                }
                $('.popUp').removeClass('active');
            },
            error: function(){                    
                $('.popUp').removeClass('active');
            }
        })        
    })

});