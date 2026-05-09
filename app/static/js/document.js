// =========================================
// FILE: app/static/js/document.js
// =========================================

// =========================================
// SEARCH DOCUMENT
// =========================================
const searchInput = document.querySelector("#documentSearch");

if(searchInput){

    searchInput.addEventListener("keyup", function(){

        const value = this.value.toLowerCase();

        const rows = document.querySelectorAll(
            ".table tbody tr"
        );

        rows.forEach(row => {

            const text = row.innerText.toLowerCase();

            if(text.includes(value)){

                row.style.display = "";

            }else{

                row.style.display = "none";
            }

        });

    });

}

// =========================================
// CONFIRM DELETE
// =========================================
const deleteButtons = document.querySelectorAll(
    ".btn-delete"
);

deleteButtons.forEach(button => {

    button.addEventListener("click", function(event){

        const confirmDelete = confirm(
            "Bạn có chắc muốn xóa văn bản này?"
        );

        if(!confirmDelete){

            event.preventDefault();
        }

    });

});

// =========================================
// FILTER BY STATUS
// =========================================
const statusFilter = document.querySelector(
    "#statusFilter"
);

if(statusFilter){

    statusFilter.addEventListener("change", function(){

        const value = this.value.toLowerCase();

        const rows = document.querySelectorAll(
            ".table tbody tr"
        );

        rows.forEach(row => {

            const statusCell = row.querySelector(
                ".status"
            );

            if(!statusCell) return;

            const statusText = statusCell.innerText
                .toLowerCase();

            if(
                value === "all" ||
                statusText.includes(value)
            ){

                row.style.display = "";

            }else{

                row.style.display = "none";
            }

        });

    });

}

// =========================================
// PREVIEW UPLOAD FILE NAME
// =========================================
const fileInput = document.querySelector(
    "#documentFile"
);

if(fileInput){

    fileInput.addEventListener("change", function(){

        const fileName = this.files[0]?.name;

        const preview = document.querySelector(
            "#filePreview"
        );

        if(preview && fileName){

            preview.innerText =
                "📎 " + fileName;
        }

    });

}

// =========================================
// DOCUMENT DETAIL MODAL
// =========================================
const modalButtons = document.querySelectorAll(
    ".btn-view"
);

modalButtons.forEach(button => {

    button.addEventListener("click", () => {

        const modal = document.querySelector(
            "#documentModal"
        );

        if(modal){

            modal.classList.remove("hidden");
        }

    });

});

// =========================================
// CLOSE MODAL
// =========================================
const closeModal = document.querySelector(
    "#closeModal"
);

if(closeModal){

    closeModal.addEventListener("click", () => {

        document
            .querySelector("#documentModal")
            .classList.add("hidden");

    });

}