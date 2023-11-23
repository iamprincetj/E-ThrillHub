let getPost = document.querySelector("#main-ul #post");
let getPostLnk = document.querySelector("#main-ul li .post");
let check = false;


getPost.addEventListener("click", function () {
    if (check) {
        getPostLnk.style.display = "none";
        check = false;
        return;
    } else {
        getPostLnk.style.display = "block";
        check = true;
    }
});