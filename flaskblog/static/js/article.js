var currentUserId = document.getElementById("current-user-info").dataset.userId;

function getUsername(comment) {
    if (comment.user !== null) {
        return comment.user.username;
    } else {
        return "Unknown User";
    }
}

function urlForProfile(username) {
    return `/users/profile/${username}`;
}

// Function to generate the account URL
function urlForAccount() {
    return `/users/account`;
}

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
    content.classList.toggle("active"); // Toggle the active class
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

var updatingComments = false; // Flag to track if an update is in progress

function updateComments(post_id) {
    if (!updatingComments) {
        updatingComments = true;

        $.get('/post/' + post_id + '/get_comments', function(data) {
            var commentsContainer = document.getElementById("comments-" + post_id);
            
            var commentsHtml = '';
            for (var i = 0; i < data.comments_html.length; i++) {
                var comment = data.comments_html[i];
                var commentHtml = `
                    <p>
                        <strong>
                            ${comment.user !== currentUserId
                                ? `<a class="mr-2" href="${urlForProfile(getUsername(comment))}" style="color: rgb(195, 19, 19);">${getUsername(comment)}</a>`
                                : `<a class="mr-2" href="${urlForAccount()}" style="color: rgb(195, 19, 19);">${getUsername(comment)}</a>`
                            }
                        </strong>
                        ${comment.text}
                    </p>`;
                commentsHtml += commentHtml;
            }
            
            commentsContainer.innerHTML = commentsHtml;

            updatingComments = false;
        });
    }
}