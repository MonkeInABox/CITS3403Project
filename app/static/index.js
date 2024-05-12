function like(postId){
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`)
    const dislikeButton = document.getElementById(`dislike-button-${postId}`)

    fetch(`/like/${postId}/like`, {method: "POST"})
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

function dislike(postId){
    const likeCount = document.getElementById(`likes-count-${postId}`);
    const dislikeButton = document.getElementById(`dislike-button-${postId}`)
    const likeButton = document.getElementById(`like-button-${postId}`)

    fetch(`/like/${postId}/dislike`, {method: "POST"})
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
