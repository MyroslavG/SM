src="https://code.jquery.com/jquery-3.6.0.min.js"

function updateLikeCount(action, post_id) {
    toggleLikeButtons(post_id, action);
    jQuery.ajax({
        type: 'POST',
        url: '/post/' + post_id + '/like',
        data: {'action': action},
        success: function(response) {
            jQuery('#like-count-' + post_id).text(response.likes);
        },
        error: function(xhr) {
            if (xhr.status === 401) {
                // User is not logged in, redirect to login page
                window.location.href = 'users.login';
            } else {
                console.error(error);
            }
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
    content.classList.toggle("active"); // Toggle the active class
    updateComments(post_id);
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
            jQuery('#comment-count-' + post_id).text(response.comments);
            commentInput.value = "";
            updateComments(post_id);
        },
        error: function(xhr) {
            if (xhr.status === 401) {
                // User is not logged in, redirect to login page
                window.location.href = 'users.login';
            } else {
                console.error(error);
            }
        }
    });
}

var updatingComments = false; // Flag to track if an update is in progress

function updateComments(post_id) {
    if (!updatingComments) {
        updatingComments = true;

        $.get('/post/' + post_id + '/get_comments', function(data) {
            var commentsContainer = document.getElementById("comments-" + post_id);
            commentsContainer.innerHTML = data;

            updatingComments = false;
        });
    }
}

$(document).ready(function() {
    $('.delete-comment-btn').click(function() {
        var commentId = $(this).closest('.delete-comment-form').data('comment-id');
        
        $.ajax({
            type: 'POST',
            url: '/post/' + postId + '/comment/' + commentId + '/delete',
            success: function(response) {
                if (response.status === 'success') {
                    // Reload the comments section after successful deletion
                    updateComments(post_id);
                } else {
                    alert(response.message);  // Show error message
                }
            },
            error: function(error) {
                console.error(error);
            }
        });
    });
});