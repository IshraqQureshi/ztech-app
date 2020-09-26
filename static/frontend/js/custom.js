$(document).ready(function(){

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

            $('.finger-print.section').animate({
                left: '0',
            }, 1000);

        } )

    }, 4000 )

    var finger_verify = 0;

    $('.finger-btn').click(function(e){
        e.preventDefault();        

        if ( finger_verify < 5 )
        {
            $('.popUp').addClass('active');

            $.ajax({
                url: '/finger-verification/finger_print_verification/',
                type: 'POST',        
                success: function(response){
                    if( response.employee_name )
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
                    else{
                        finger_verify = finger_verify + 1;
                        alert(finger_verify)
                    }

                    $('.popUp').removeClass('active');
                },
                error: function(){                    
                    finger_verify = finger_verify + 1;
                    $('.popUp').removeClass('active');
                }
            })
        }
        else{
            alert('Out Of Verifications')
        }
    })

});