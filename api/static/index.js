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


window.onload = () => {
    let getLoadDiv = document.querySelector("#loading_modal");
    getLoadDiv.style.display = "none";
};