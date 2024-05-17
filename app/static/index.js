function like(postId, medium){
    if (medium == "post"){
        var likeCount = document.getElementById(`likes-count-post-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-post-${postId}`);
        var likeButton = document.getElementById(`like-button-post-${postId}`);
        var liked_class_name = "fas fa-thumbs-up fa-2x"
        var not_liked_class_name = "far fa-thumbs-up fa-2x"
        var disliked_class_name = "fas fa-thumbs-down fa-2x"
        var not_disliked_class_name = "far fa-thumbs-down fa-2x"
    } else{
        var likeCount = document.getElementById(`likes-count-comment-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-comment-${postId}`);
        var likeButton = document.getElementById(`like-button-comment-${postId}`);
        var liked_class_name = "fas fa-thumbs-up fa-lg"
        var not_liked_class_name = "far fa-thumbs-up fa-lg"
        var disliked_class_name = "fas fa-thumbs-down fa-lg"
        var not_disliked_class_name = "far fa-thumbs-down fa-lg"
    }

    fetch(`/like/${postId}/like/${medium}`, {method: "POST"})
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if(data["liked"]  === true){
                likeButton.className = liked_class_name
            } else(
                likeButton.className = not_liked_class_name
            )
            if(data["disliked"]  === true){
                dislikeButton.className = disliked_class_name
            } else(
                dislikeButton.className = not_disliked_class_name
            )
        })
}

function dislike(postId, medium){
    if (medium == "post"){
        var likeCount = document.getElementById(`likes-count-post-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-post-${postId}`);
        var likeButton = document.getElementById(`like-button-post-${postId}`);
        var liked_class_name = "fas fa-thumbs-up fa-2x"
        var not_liked_class_name = "far fa-thumbs-up fa-2x"
        var disliked_class_name = "fas fa-thumbs-down fa-2x"
        var not_disliked_class_name = "far fa-thumbs-down fa-2x"
    } else{
        var likeCount = document.getElementById(`likes-count-comment-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-comment-${postId}`);
        var likeButton = document.getElementById(`like-button-comment-${postId}`);
        var liked_class_name = "fas fa-thumbs-up fa-lg"
        var not_liked_class_name = "far fa-thumbs-up fa-lg"
        var disliked_class_name = "fas fa-thumbs-down fa-lg"
        var not_disliked_class_name = "far fa-thumbs-down fa-lg"
    }
        
    fetch(`/like/${postId}/dislike/${medium}`, {method: "POST"})
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data["likes"];
        if(data["disliked"]  === true){
            dislikeButton.className = disliked_class_name
        } else(
            dislikeButton.className = not_disliked_class_name
        )
        if(data["liked"]  === true){
            likeButton.className = liked_class_name
        } else(
            likeButton.className = not_liked_class_name
        )
    })
}

function buttonHandling() {
    var buttons = document.getElementsByClassName("toggle-comments-button");

    Array.from(buttons).forEach(function(button) {
        var postId = button.getAttribute("data-post-id");
        
        // Add a variable to track if the button is clicked
        var isClicked = false;

        button.addEventListener('mouseover', function() {
            if (!isClicked) {
                button.classList.remove("fa-regular");
                button.classList.add("fa-solid");
            }
            else if (isClicked) {
                button.classList.remove("fa-solid");
                button.classList.add("fa-regular")
            }
        });

        button.addEventListener('mouseout', function() {
            if (!isClicked) {
                button.classList.remove("fa-solid");
                button.classList.add("fa-regular");
                button.style.transform = "scale(1)"; // Reset button size
            }
        });

        button.addEventListener('mousedown', function() {
            button.style.transform = "scale(0.85)";
            toggleComments(postId);
        });

        button.addEventListener('mouseup', function() {
            button.style.transform = "scale(1)";
        });

        button.addEventListener('click', function() {
            isClicked = !isClicked; // Toggle clicked state
        });

    });
}

function toggleComments(postId) {
    var commentsContainer = document.getElementById(`toggle-comments-field-${postId}`);
    var repliesContainer = document.getElementById(`replies-${postId}`);
    
    // If the comments are currently hidden, send a request to fetch them
    if (commentsContainer.style.display === 'none') {
        var xhr = new XMLHttpRequest();
        var url = '/get_comments/' + postId;
        xhr.open('GET', url, true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                commentsContainer.innerHTML = xhr.responseText;
                commentsContainer.style.display = '';
                repliesContainer.style.display = '';
            }
        };
        xhr.send();
    } else {
        // If the comments are visible, hide them
        commentsContainer.style.display = 'none';
        repliesContainer.style.display = 'none';
    }
}

function loadComments(postId) {
    var commentsContainer = document.getElementById(`toggle-comments-field-${postId}`);
    var repliesContainer = document.getElementById(`replies-${postId}`);
    
    var xhr = new XMLHttpRequest();
    var url = '/get_comments/' + postId;
    xhr.open('GET', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            commentsContainer.innerHTML = xhr.responseText;
        }
    };
    xhr.send();
}

function handleSubmitButtons() {
    var submitButtons = document.getElementsByClassName("submit");

    Array.from(submitButtons).forEach(function(submitButton) {
        submitButton.addEventListener("mousedown", function() {
            // Add transparent border when clicked
            submitButton.style.boxShadow = "0 0 20px 10px rgba(0, 0, 0, 0.2) inset";
            submitButton.style.transform = "scale(0.975)";
            submitButton.style.fontSize = "1.025em";
        });

        submitButton.addEventListener("mouseup", function() {
            // Remove transparent border when mouse released
            submitButton.style.boxShadow = "none";
            submitButton.style.transform = "scale(1)";
        });

        submitButton.addEventListener("click", function() {
            
        })
    });
}
function removeErrorMessages() {
    var submitButtons = document.getElementsByClassName("comment_submit");

    Array.from(submitButtons).forEach(function(submitButton) {
        var postId = submitButton.getAttribute("data-post-id");
        submitButton.addEventListener("click", function() {
            handleNewCommentInput(postId);
            // Display any existing error messages
            var errorField = document.getElementById(`comment-error-${postId}`);
            if (errorField) {
                errorField.style.display = 'none';
            }
        });
    });
}

function handleNewCommentInput(postId) {
    const form = document.getElementById('comment-form-' + postId);
    const formData = new FormData(form);

    fetch('/', {  // Assuming the route for form submission is the same as the current page route
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            console.log('Comment Submitted');
            // Clear the comment input field
            document.getElementById(`comment-form-${postId}`).reset();
            // Display flash message
            document.getElementById('flash-message').style.display = 'block';
            // Hide flash message after a few seconds
            setTimeout(() => {
                document.getElementById('flash-message').style.display = 'none';
            }, 3000);
            // Update comment button visibility
            const button = document.getElementById(`toggle-comments-button-${postId}`);
            console.log(button)
            button.style.display = ''; // Show button
        }
        else if (response.status === 400) {
            // Form validation errors received
            response.json().then(data => {
                const errors = data.errors;
                const errorMessage = Object.values(errors).join(', '); // Concatenate error messages
                // Display the error message in the designated <span> element
                const errorSpan = document.getElementById(`json-error-${postId}`);
                const showError = document.getElementById(`comment-error-${postId}`);
                errorSpan.textContent = errorMessage;
                showError.style.display='';
            });
        }
        else {
            console.log ('Comment submission failed');
        }
    })
    .catch(error => {
        console.error('Error submitting comment:', error);
    });
}

function pollForUpdates() {
    console.log('test');
    setInterval(() => {
        const urlParams = new URLSearchParams(window.location.search);
        var page = urlParams.get('page');
        var filter = urlParams.get('filter')
        var category = window.location.pathname.split('/').filter(Boolean)[1];
        console.log(category)
        fetch(`/check_updates?page=${page}&filter=${filter}&category=${category}`) // Replace '/check_updates' with the appropriate route to check for updates
            .then(response => {
                if (response.ok) {
                    console.log(response);
                    return response.json();
                } else {
                    throw new Error('Network response was not ok');
                }
            })
            .then(data => {
                console.log(data)
                // Update comment button visibility for each post
                data.forEach(postId => {
                    console.log(postId)
                    var button = document.getElementById(`toggle-comments-button-${postId}`);
                    if (postId > 0) {
                        console.log("has comments");
                        loadComments(postId)
                        button.style.display = ''; // Show button
                    } else {
                        postId = Math.abs(postId)
                        button = document.getElementById(`toggle-comments-button-${postId}`)
                        button.style.display = 'none'; // Hide button
                    }
                });
            })
            .catch(error => {
                console.error('Error checking for updates:', error);
            });
    }, 10000); // Poll every 10 seconds (10000 milliseconds)
}


document.addEventListener('DOMContentLoaded', function() {
    buttonHandling();
    handleSubmitButtons();
    removeErrorMessages();
    pollForUpdates();
});