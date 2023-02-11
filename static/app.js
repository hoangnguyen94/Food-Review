// Function to click Like to add api to database

const likeButtons = $( '.like-button' );
$(document).on("click", ".like-button", () =>
{
    const apiId = event.target.dataset.apiId;
    const userId = event.target.dataset.userId;
    const $button = $( event.target);
    
    likeButtons.each( function ()
    {
        const apiId = this.dataset.apiId;
        const $button = $(this);
        if (localStorage.getItem(apiId) === 'Unlike') {
            $button.removeClass("btn-primary");
            $button.addClass("btn-secondary");
            $button.text("Unlike");
        }
    } );
    
    $.ajax({
        type: 'POST',
        url: '/like',
        data: JSON.stringify({ apiId, userId }),
        contentType: 'application/json',
        success: ( data ) =>
        {
            console.log( data );
            if ( data.success === true && $button.text() == 'Like' )
            {
                $button.removeClass( "btn-primary" );
                $button.addClass( "btn-secondary" );
                $button.text( 'Unlike' );
            } else if ( data.success === true && $button.text() == 'Unlike' )
            {   
                $button.removeClass( "btn-secondary" );
                $button.addClass( "btn-primary" );
                $button.text('Like');
            }
        },
        error: (error) => {
            console.error('Error:', error);
        }
    });
} );

















