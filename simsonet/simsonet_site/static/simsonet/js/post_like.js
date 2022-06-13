function likePressed(button, post_id){
    var counterSpan = document.getElementById('like_counter_'+post_id);
    var counter = parseInt(counterSpan.innerText);
    var likeEvent = $.ajax({
        url: '/posts/api/'+post_id+'/like/', 
        type: 'POST',
        headers: {"Authorization": "Token "+user_auth_token}, 
        success: function() {
            button.classList.add("btn-primary");
            button.classList.remove("btn-outline-primary");
            counterSpan.innerText = counter+1;
        },
        error: function() {
            $.ajax({
                url: '/posts/api/'+post_id+'/like/', 
                type: 'DELETE',
                headers: {"Authorization": "Token "+user_auth_token}, 
                success: function() {
                    button.classList.add("btn-outline-primary");
                    button.classList.remove("btn-primary");
                    counterSpan.innerText = counter-1;
                },
                error: function() {
                    console.log('communication error');
                }
            });
        }
    });
};
