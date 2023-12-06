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


setInterval(function() {
    var timestamps = document.querySelectorAll('.timestamp');
    timestamps.forEach(function(timestamp) {
        var postTime = new Date(timestamp.dataset.timestamp + 'Z');
        var now = new Date();
        var diffInSeconds = Math.floor((now - postTime) / 1000);
        var diffInMinutes = Math.floor(diffInSeconds / 60);
        var diffInHours = Math.floor(diffInMinutes / 60);
        var diffInDays = Math.floor(diffInHours / 24);
        
        if (diffInDays > 0) {
            timestamp.textContent = diffInDays + ' days ago';
        } else if (diffInHours > 0) {
            timestamp.textContent = diffInHours + ' hours ago';
        } else if (diffInMinutes > 0) {
            timestamp.textContent = diffInMinutes + ' minutes ago';
        } else if (diffInSeconds > 0) {
            timestamp.textContent = diffInSeconds + ' seconds ago';
        } else {
            timestamp.textContent = 'Just now';
        }
    });
    // END: ed8c6549bwf9;
}, 1000);


window.onload = function() {
    // This code will run after the entire page is loaded
    alert("Page has finished loading!");
};