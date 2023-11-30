let getProfilePic = () => {
    let getProfilePic = document.querySelectorAll(".pp");
    let getProfilePicModal = document.querySelector('.pro_pic_modal');
    let getProfilePicClose = document.querySelector(".profile-pic-close");

    getProfilePic.forEach((val) => {
        val.addEventListener("click", () => {
            console.log(getProfilePicModal);
            var profilePic = document.createElement("img");
            profilePic.className = 'profile-pic-img';
            profilePic.src = val.src;
            if (getProfilePicModal.childNodes[3] == undefined) {
                getProfilePicModal.appendChild(profilePic);
            }
            getProfilePicModal.style.display = "block";
        })
    })

    window.onclick = function (event) {
        if (event.target == getProfilePicModal) {
            getProfilePicModal.style.display = "none";
            check = false;
        }
    }

    getProfilePicClose.addEventListener("click", () => {
        getProfilePicModal.style.display = "none";
    });
}

getProfilePic();