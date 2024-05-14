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