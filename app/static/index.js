function like(postId, medium){
    if (medium == "post"){
        var likeCount = document.getElementById(`likes-count-post-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-post-${postId}`);
        var likeButton = document.getElementById(`like-button-post-${postId}`);
    } else{
        var likeCount = document.getElementById(`likes-count-comment-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-comment-${postId}`);
        var likeButton = document.getElementById(`like-button-comment-${postId}`);
    }

    fetch(`/like/${postId}/like/${medium}`, {method: "POST"})
        .then((res) => res.json())
        .then((data) => {
            likeCount.innerHTML = data["likes"];
            if(data["liked"]  === true){
                likeButton.className = "fas fa-thumbs-up fa-2x"
            } else(
                likeButton.className = "far fa-thumbs-up fa-2x"
            )
            if(data["disliked"]  === true){
                dislikeButton.className = "fas fa-thumbs-down fa-2x"
            } else(
                dislikeButton.className = "far fa-thumbs-down fa-2x"
            )
        })
}

function dislike(postId, medium){
    if (medium == "post"){
        var likeCount = document.getElementById(`likes-count-post-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-post-${postId}`);
        var likeButton = document.getElementById(`like-button-post-${postId}`);
    } else{
        var likeCount = document.getElementById(`likes-count-comment-${postId}`);
        var dislikeButton = document.getElementById(`dislike-button-comment-${postId}`);
        var likeButton = document.getElementById(`like-button-comment-${postId}`);
    }
        
    fetch(`/like/${postId}/dislike/${medium}`, {method: "POST"})
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data["likes"];
        if(data["disliked"]  === true){
            dislikeButton.className = "fas fa-thumbs-down fa-2x"
        } else(
            dislikeButton.className = "far fa-thumbs-down fa-2x"
        )
        if(data["liked"]  === true){
            likeButton.className = "fas fa-thumbs-up fa-2x"
        } else(
            likeButton.className = "far fa-thumbs-up fa-2x"
        )
    })
}