function updateLikeCount(action, post_id) {
    toggleLikeButtons(post_id, action);
    jQuery.ajax({
        type: 'POST',
        url: '/post/' + post_id + '/like',
        data: {'action': action},
        success: function(response) {
            jQuery('#like-count-' + post_id).text(response.likes);
        },
        error: function(error) {
            console.error(error);
        }
    });
}

function toggleLikeButtons(post_id, action) {
    var likeButton = document.getElementById('like-button-' + post_id);
    var dislikeButton = document.getElementById('dislike-button-' + post_id);

    if (action === 'increment') {
        likeButton.disabled = true;
        dislikeButton.disabled = false;
    } else if (action === 'decrement') {
        likeButton.disabled = false;
        dislikeButton.disabled = true;
    }
}

function toggleCollapsibleContent(post_id) {
    var content = document.getElementById("comments-" + post_id);
    if (content.style.display === "none") {
        content.style.display = "block";
    } else {
        content.style.display = "none";
    }
}

function submitComment(post_id) {
    var commentInput = document.getElementById("comment-input-" + post_id);
    var commentText = commentInput.value;

    $.ajax({
        type: 'POST',
        url: '/post/' + post_id + '/comment',
        data: {'comment_text': commentText},
        success: function(response) {
            // Clear the input field and update the comments section
            commentInput.value = "";
            updateComments(post_id);
        },
        error: function(error) {
            console.error(error);
        }
    });
}

var updatingComments = false;  // Flag to track if an update is in progress

function updateComments(post_id) {
    if (!updatingComments) {  // Check if an update is not already in progress
        updatingComments = true;  // Set the flag to true
        
        $.get('/post/' + post_id + '/get_comments', function(data) {
            var commentsContainer = document.getElementById("comments-" + post_id);
            commentsContainer.innerHTML = data.comments_html;
            
            updatingComments = false;  // Reset the flag when update is complete
        });
    }
}