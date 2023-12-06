/**let getLikeLink = document.querySelectorAll(".like_post");

getLikeLink.forEach((val) => {
    val.addEventListener("click", () => {
        let postId = val.id;
        alert(postId);
        let getThumbsup = document.querySelector(".fa-thumbs-up")
        let res = fetch("/like/" + postId, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        }).then((response) => {
            console.log(response.json());
            return response.json();
        }).then(data => {
            console.log(data.json())
        })
        .catch((error) => {
            console.log(error);
        });
    });
});*/

let likeButtons = document.querySelectorAll("#post_container .like_post");
console.log(likeButtons)
likeButtons.forEach((likeButton) => {
    likeButton.addEventListener("click", () => {
        let postId = likeButton.id;
        let url = '/like/' + postId;
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
        })
        .then((res) => res.json())
        .catch((error) => console.error(error))
        .then(data => {
            if (data.has_liked == "liked") {
                likeButton.style.color = "red";
            } else {
                likeButton.style.color = "grey";
            }
        });
    });
});
