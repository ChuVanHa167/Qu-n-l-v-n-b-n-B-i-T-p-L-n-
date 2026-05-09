// =========================================
// FILE: app/static/js/dashboard.js
// =========================================

// =========================================
// ACTIVE SIDEBAR MENU
// =========================================
const menuLinks = document.querySelectorAll(".menu li a");

menuLinks.forEach(link => {

    if(link.href === window.location.href){

        link.parentElement.classList.add("active");
    }

});

// =========================================
// AUTO CLOSE ALERT
// =========================================
const alerts = document.querySelectorAll(".alert");

alerts.forEach(alert => {

    setTimeout(() => {

        alert.style.opacity = "0";

        setTimeout(() => {
            alert.remove();
        }, 500);

    }, 3000);

});

// =========================================
// TOGGLE SIDEBAR MOBILE
// =========================================
const toggleButton = document.querySelector("#sidebarToggle");

if(toggleButton){

    toggleButton.addEventListener("click", () => {

        document
            .querySelector(".sidebar")
            .classList.toggle("show");

    });

}

// =========================================
// SIMPLE COUNTER ANIMATION
// =========================================
const counters = document.querySelectorAll(".stats-card h2");

counters.forEach(counter => {

    const target = Number(counter.innerText);

    let current = 0;

    const increment = Math.ceil(target / 30);

    const updateCounter = () => {

        current += increment;

        if(current >= target){

            counter.innerText = target;

        }else{

            counter.innerText = current;

            setTimeout(updateCounter, 30);
        }
    };

    updateCounter();

});