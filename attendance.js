// ------------------------------
// Attendance Processing Script
// ------------------------------

const uploadBtn = document.getElementById("uploadBtn");
const classPhoto = document.getElementById("classPhoto");
const statusText = document.getElementById("status");
const resultsDiv = document.getElementById("results");

// Backend API URL
const API_URL = "https://class2lens-backend.onrender.com/attendance"; 
// (Later you will replace with your own deployed backend URL)


uploadBtn.addEventListener("click", async () => {
    if (!classPhoto.files || classPhoto.files.length === 0) {
        alert("Please upload a classroom photo first!");
        return;
    }

    const file = classPhoto.files[0];

    statusText.innerText = "Processing attendance... (this may take 5–10 seconds)";
    resultsDiv.innerHTML = "";

    const formData = new FormData();
    formData.append("image", file);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            statusText.innerText = "Error: " + data.error;
            return;
        }

        statusText.innerText = "Attendance Processed";

        renderResults(data);

    } catch (error) {
        console.error(error);
        statusText.innerText = "Error connecting to server!";
    }
});


// ------------------------------
// Display Attendance Results
// ------------------------------

function renderResults(data) {
    resultsDiv.innerHTML = "";

    if (!data.students || data.students.length === 0) {
        resultsDiv.innerHTML = "<p>No faces detected!</p>";
        return;
    }

    data.students.forEach(student => {
        const div = document.createElement("div");
        div.className = student.present ? "present" : "absent";

        div.innerHTML = `
            <strong>${student.name}</strong><br>
            Register No: ${student.regno}<br>
            Status: ${student.present ? "Present" : "Absent"}
        `;

        resultsDiv.appendChild(div);
    });
}
