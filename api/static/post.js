
let getPost = () => {
    let getPostModal = document.getElementById("post-div");
    let getPostLink = document.getElementById("post");
    let getClose = document.querySelector(".close");


    getPostLink.addEventListener("click", () => {
        getPostModal.style.display = "block";
    });

    getClose.addEventListener("click", () => {
        getPostModal.style.display = "none";
    });

    window.onclick = function (event) {
        console.log(event.target)
        if (event.target == getPostModal) {
            getPostModal.style.display = "none";
        }
    };
}


let makePost = () => {
    let getImagePost = document.querySelector("#imagepost")
    let showImg = document.querySelector("#show-img");
    let getImageLabel = document.querySelector("#label-image");

    getImagePost.addEventListener("change", (e) => {
        let reader = new FileReader();

        reader.onload = function () {
            var img = document.createElement("img");
            img.src = reader.result;
            img.className = "img-fluid";
            showImg.appendChild(img);
        }
        reader.readAsDataURL(e.target.files[0]);
    });

    let getPostLnk = document.querySelector("#main-ul li .post");
    let getLinkLabel = document.querySelector("#label-link")
    let getLinkPost = document.querySelector("#linkpost")

    let check_link = false;





    getLinkLabel.addEventListener("click", () => {
        if (check_link) {
            getLinkPost.style.display = "none";
            check_link = false;
        } else {
            getLinkPost.style.display = "block";
            check_link = true;
        }
    });
}

let getPostLikes = () => {
    let getLikelink = document.querySelector("#post_container #likes");
    let getModal = document.querySelector(".like_modal");

    getLikelink.addEventListener("click", () => {
        getModal.style.display = "block";
    });
}


let likeButtons = document.querySelectorAll("#post_container .like_post");
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

let likeButtonsComment = document.querySelectorAll(".comment_contents .like_comment");
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

getPost();
makePost();
getPostLikes();