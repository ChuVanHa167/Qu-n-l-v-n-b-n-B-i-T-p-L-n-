// =========================================
// FILE: app/static/js/document.js
// =========================================

// =========================================
// DELETE CONFIRM
// =========================================
document.querySelectorAll(".btn-delete").forEach(button => {

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
// FILE PREVIEW
// =========================================
const fileInput = document.getElementById(
    "document_file"
);

if(fileInput){

    fileInput.addEventListener("change", function(){

        const preview = document.getElementById(
            "uploaded_file_preview"
        );

        if(this.files.length){

            preview.innerHTML = `
                <div class="file-preview-card">
                    📄 ${this.files[0].name}
                </div>
            `;
        }

    });

}

// =========================================
// OCR EFFECT STYLE
// =========================================
function detectLineType(line){

    const lower = line.toLowerCase();

    if(
        lower.includes("quyết định")
        ||
        lower.includes("thông báo")
        ||
        lower.includes("kế hoạch")
        ||
        lower.includes("báo cáo")
    ){
        return "ocr-title";
    }

    if(
        lower.includes("số:")
    ){
        return "ocr-number";
    }

    if(
        lower.includes("ngày")
        &&
        lower.includes("tháng")
    ){
        return "ocr-date";
    }

    if(
        lower.includes("hiệu trưởng")
        ||
        lower.includes("giám đốc")
        ||
        lower.includes("chủ tịch")
    ){
        return "ocr-signer";
    }

    return "ocr-normal";
}

// =========================================
// AI PROCESS
// =========================================
async function processAI(){

    const fileInput = document.getElementById(
        "document_file"
    );

    if(!fileInput.files.length){

        alert("Hãy chọn file");

        return;
    }

    const aiBox = document.getElementById(
        "ai_processing_box"
    );

    const progressBar = document.getElementById(
        "ocr_progress_bar"
    );

    const statusText = document.getElementById(
        "ocr_status_text"
    );

    const liveText = document.getElementById(
        "ocr_live_text"
    );

    aiBox.style.display = "block";

    progressBar.style.width = "0%";

    liveText.innerHTML = "";

    statusText.innerHTML =
        "🤖 AI đang đọc và hiểu ngữ nghĩa văn bản...";

    const formData = new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    try{

        let progress = 0;

        const fakeLoading = setInterval(() => {

            progress += 2;

            if(progress > 95){

                progress = 95;
            }

            progressBar.style.width =
                progress + "%";

        }, 120);

        const response = await fetch(
            "/admin/documents/ai-extract",
            {
                method: "POST",
                body: formData
            }
        );

        const result = await response.json();

        clearInterval(fakeLoading);

        progressBar.style.width = "100%";

        if(!result.success){

            alert(result.message);

            return;
        }

        const data = result.data;

        // =================================
        // SENTENCE DISPLAY
        // =================================
        const sentences = data.sentences || [];

        let index = 0;

        const scanner = setInterval(() => {

            if(index >= sentences.length){

                clearInterval(scanner);

                statusText.innerHTML =
                    "✅ AI đã hiểu và phân tích hoàn tất";

                return;
            }

            const line = document.createElement(
                "div"
            );

            line.className = detectLineType(
                sentences[index]
            );

            line.innerHTML = `
                ${sentences[index]}
            `;

            liveText.appendChild(line);

            liveText.scrollTop =
                liveText.scrollHeight;

            index++;

        }, 180);

        // =================================
        // AUTO FILL
        // =================================
        setTimeout(() => {

            document.querySelector(
                'input[name="title"]'
            ).value = data.title || "";

            document.querySelector(
                'input[name="document_number"]'
            ).value = data.document_number || "";

            document.querySelector(
                'input[name="issuer"]'
            ).value = data.issuer || "";

            document.querySelector(
                'input[name="signer"]'
            ).value = data.signer || "";

            document.querySelector(
                'input[name="issue_date"]'
            ).value = data.issue_date || "";

            document.querySelector(
                'input[name="keywords"]'
            ).value = data.keywords || "";

            document.querySelector(
                'textarea[name="content"]'
            ).value = data.summary || "";

            if(data.document_type){

                document.querySelector(
                    'select[name="document_type"]'
                ).value = data.document_type;

            }

            if(data.category){

                document.querySelector(
                    'select[name="category"]'
                ).value = data.category;

            }

            if(data.priority){

                document.querySelector(
                    'select[name="priority"]'
                ).value = data.priority;

            }

        }, 1200);

    }catch(error){

        console.log(error);

        alert("AI xử lý thất bại");

    }

}