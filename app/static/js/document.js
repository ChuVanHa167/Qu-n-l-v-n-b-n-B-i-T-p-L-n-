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

// ==========================================
// AI AUTO EXTRACT
// ==========================================
async function processAI() {

    const fileInput = document.getElementById(
        'document_file'
    );

    if (!fileInput.files.length) {

        alert("Hãy chọn file");

        return;
    }

    // =====================================
    // SHOW AI BOX
    // =====================================
    const aiBox = document.getElementById(
        'ai_processing_box'
    );

    const progressBar = document.getElementById(
        'ocr_progress_bar'
    );

    const statusText = document.getElementById(
        'ocr_status_text'
    );

    const liveText = document.getElementById(
        'ocr_live_text'
    );

    aiBox.style.display = 'block';

    progressBar.style.width = '0%';

    liveText.innerHTML = '';

    statusText.innerHTML =
        'AI đang đọc tài liệu...';

    // =====================================
    // FAKE AI SCAN EFFECT
    // =====================================
    let progress = 0;

    const fakeScan = setInterval(() => {

        progress += 10;

        progressBar.style.width =
            progress + '%';

        statusText.innerHTML =
            'AI đang OCR tài liệu... ' +
            progress + '%';

        liveText.innerHTML +=
            "▋ Đang phân tích dữ liệu...\n";

        liveText.scrollTop =
            liveText.scrollHeight;

        if(progress >= 90){

            clearInterval(fakeScan);
        }

    }, 300);

    // =====================================
    // SEND FILE
    // =====================================
    const formData = new FormData();

    formData.append(
        'file',
        fileInput.files[0]
    );

    try {

        const response = await fetch(
            '/admin/documents/ai-extract',
            {
                method: 'POST',
                body: formData
            }
        );

        const result = await response.json();

        clearInterval(fakeScan);

        progressBar.style.width = '100%';

        statusText.innerHTML =
            'AI xử lý hoàn tất';

        if (!result.success) {

            alert(result.message);

            return;
        }

        const data = result.data;

        // =================================
        // SHOW OCR TEXT
        // =================================
        liveText.innerHTML =
            data.ocr_text.substring(0, 3000);

        // =================================
        // AUTO FILL
        // =================================
        document.querySelector(
            'input[name="title"]'
        ).value = data.title || '';

        document.querySelector(
            'textarea[name="content"]'
        ).value = data.content || '';

        document.querySelector(
            'select[name="document_type"]'
        ).value =
            data.document_type || 'incoming';

        document.querySelector(
            'select[name="category"]'
        ).value =
            data.category || 'Nội bộ';

        document.querySelector(
            'select[name="priority"]'
        ).value =
            data.priority || 'normal';

        alert("AI xử lý thành công");

    } catch (error) {

        console.log(error);

        alert("AI xử lý thất bại");
    }
}

const documentNumberInput = document.querySelector(
    'input[name="document_number"]'
);

if(documentNumberInput){

    documentNumberInput.value =
        data.document_number || '';
}

const signerInput = document.querySelector(
    'input[name="signer"]'
);

if(signerInput){

    signerInput.value =
        data.signer || '';
}

const issuerInput = document.querySelector(
    'input[name="issuer"]'
);

if(issuerInput){

    issuerInput.value =
        data.issuer || '';
}

const issueDateInput = document.querySelector(
    'input[name="issue_date"]'
);

if(issueDateInput){

    issueDateInput.value =
        data.issue_date || '';
}

const keywordInput = document.querySelector(
    'input[name="keywords"]'
);

if(keywordInput){

    keywordInput.value =
        data.keywords || '';
}