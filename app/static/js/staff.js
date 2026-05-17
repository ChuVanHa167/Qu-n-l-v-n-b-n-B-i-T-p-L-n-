// =====================================================
// STAFF JS
// =====================================================

console.log("Staff JS Loaded");


// =====================================================
// SEARCH TABLE
// =====================================================

const searchInput = document.getElementById(
    "documentSearch"
);

if (searchInput) {

    searchInput.addEventListener(
        "keyup",
        function () {

            const keyword =
                this.value.toLowerCase();

            const rows =
                document.querySelectorAll(
                    "tbody tr"
                );

            rows.forEach(function (row) {

                const text =
                    row.innerText.toLowerCase();

                if (text.includes(keyword)) {

                    row.style.display = "";

                } else {

                    row.style.display = "none";

                }

            });

        }
    );

}


// =====================================================
// CONFIRM ACTION
// =====================================================

const forms =
    document.querySelectorAll("form");

forms.forEach(function(form) {

    form.addEventListener(
        "submit",
        function(e) {

            const ok = confirm(
                "Xác nhận thao tác?"
            );

            if (!ok) {

                e.preventDefault();

            }

        }
    );

});


// =====================================================
// FAKE BUTTONS
// =====================================================

const fakeButtons =
    document.querySelectorAll(
        ".btn-primary, .btn-danger"
    );

fakeButtons.forEach(function(btn){

    btn.addEventListener(
        "click",
        function(){

            console.log(
                "Button clicked"
            );

        }
    );

});