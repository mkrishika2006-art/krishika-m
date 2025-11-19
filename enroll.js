document.getElementById("enrollForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const name = document.getElementById("studentName").value;
    const regno = document.getElementById("studentReg").value;
    const file = document.getElementById("photo").files[0];

    if (!file) {
        alert("Please upload a photo");
        return;
    }

    const formData = new FormData();
    formData.append("name", name);
    formData.append("regno", regno);
    formData.append("photo", file);

    try {
        const response = await fetch("https://class2lens-backend.onrender.com/enroll", {
            method: "POST",
            body: formData,
        });

        const result = await response.json();
        document.getElementById("status").textContent = result.message;
    } catch (error) {
        document.getElementById("status").textContent =
            "Enrollment failed — backend not reachable.";
    }
});

