document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const files = document.getElementById("cvFiles").files;
    const jobDescription = document.getElementById("jobDescription").value;

    if (files.length === 0) {
        alert("Upload at least one file.");
        return;
    }

    const formData = new FormData();
    for (let file of files) {
        formData.append("cvFiles", file);
    }
    formData.append("jobDescription", jobDescription);

    const response = await fetch("http://127.0.0.1:5000/analyze", {
        method: "POST",
        body: formData
    });

    const data = await response.json();

    if (data.error) {
        alert(data.error);
        return;
    }

    displayResults(data.results);
});

function displayResults(results) {
    const tbody = document.querySelector("#resultsTable tbody");
    tbody.innerHTML = "";

    results.forEach(res => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${res.candidate}</td>
            <td>${res.match}%</td>
            <td>${res.found.join(", ")}</td>
            <td>${res.missing.join(", ")}</td>
            <td>${res.summary}</td>
        `;

        tbody.appendChild(tr);
    });
}
