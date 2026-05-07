// =========================================
// FILE: app/static/js/document.js
// =========================================

// SEARCH DOCUMENT
const searchInput = document.querySelector("#documentSearch");

if(searchInput){

    searchInput.addEventListener("keyup", function(){

        let value = this.value.toLowerCase();

        let rows = document.querySelectorAll(".table tbody tr");

        rows.forEach(row => {

            let text = row.innerText.toLowerCase();

            if(text.includes(value)){
                row.style.display = "";
            }else{
                row.style.display = "none";
            }

        });

    });
}


// CONFIRM DELETE
const deleteButtons = document.querySelectorAll(".btn-delete");

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