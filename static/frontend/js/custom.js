$(document).ready(function(){
    
    // Global Variables
    var finger_verify = 0;
    var face_verify = 0;
    let employee_id = false;

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
        }, 1000);
    })

    $('.visitor-btn').click(function(e){
        e.preventDefault();
        $('.face_capture').animate({
            left: '0',
        }, 1000);
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
                            }, 1000); 

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
                        console.log(employee_id);
                        console.log(response.employee_id);
                        if(response.employee_id == employee_id)
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
                if( response.face_id )
                {
                    $('.finger-capture').animate({
                        left: '0',
                    }, 1000);                             
                }
            }
        });

    })

});