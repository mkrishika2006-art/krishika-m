// ===== API URL =====
const API_BASE = "https://class2lens-backend.onrender.com";

// ===== Submit enrollment =====
document.getElementById("enrollForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("studentName").value;
    const reg = document.getElementById("studentReg").value;
    const photoFile = document.getElementById("photo").files[0];

    if (!photoFile) {
        alert("Please upload a photo!");
        return;
    }

    // Create form data for file upload
    const formData = new FormData();
    formData.append("name", name);
    formData.append("register_no", reg);
    formData.append("photo", photoFile);

    try {
        const res = await fetch(`${API_BASE}/enroll`, {
            method: "POST",
            body: formData
        });

        const data = await res.json();

        if (res.ok) {
            document.getElementById("status").innerText = "Student enrolled successfully!";
        } else {
            document.getElementById("status").innerText = "Enrollment failed!";
        }

    } catch (err) {
        console.error(err);
        document.getElementById("status").innerText = "Error connecting to server!";
    }
});
