// =========================================
// FILE: app/static/js/dashboard.js
// =========================================

// SIDEBAR ACTIVE
const menuItems = document.querySelectorAll(".menu li");

menuItems.forEach(item => {
    item.addEventListener("click", () => {

        menuItems.forEach(i => {
            i.classList.remove("active");
        });

        item.classList.add("active");
    });
});


// ALERT AUTO CLOSE
const alertBox = document.querySelector(".alert");

if(alertBox){

    setTimeout(() => {
        alertBox.style.display = "none";
    }, 3000);
}