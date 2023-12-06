let editPost = () => {
    let getEditPost = document.querySelector(".edit_post");
    let getEditPostModal = document.querySelector(".edit_post_modal");
    let getEditPostCancel = document.querySelector(".edit_post_cancel");

    getEditPost.addEventListener("click", () => {
        getEditPostModal.style.display = "block";
    })
    getEditPostCancel.addEventListener("click", (e) => {
        e.preventDefault();
        getEditPostModal.style.display = "none";
    })
};

let deletePost = () => {
    let getDelPost = document.querySelector(".delete_post");
    let getDelPostModal = document.querySelector(".delete_post_modal");
    let getDelPostCancel = document.querySelector(".del_post_cancel");

    getDelPost.addEventListener("click", () => {
        getDelPostModal.style.display = "block";
    });

    getDelPostCancel.addEventListener("click", (e) => {
        e.preventDefault();
        getDelPostModal.style.display = "none";
    })
};

editPost();
deletePost();