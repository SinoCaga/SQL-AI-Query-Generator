async function generateSQL() {
    try {
        const input = document.getElementById("input");

        // 🔥 SAFETY CHECK (fixes your crash)
        if (!input) {
            alert("❌ Input field not found. Check index.html: id='question'");
            return;
        }

        const question = input.value;

        if (!question.trim()) {
            alert("❌ Please enter a question");
            return;
        }

        console.log("📤 Sending question:", question);

        const response = await fetch("http://127.0.0.1:8000/generate-sql", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        console.log("📡 Response status:", response.status);

        const data = await response.json();

        console.log("📦 Backend response:", data);

        // Show SQL safely
        document.getElementById("sqlBox").innerText =
            data.sql || "No SQL returned";

        // Show results
        renderTable(data.results);

    } catch (error) {
        console.error("❌ Error:", error);
        alert("Something went wrong. Check console.");
    }
}

function renderTable(data) {
    const container = document.getElementById("results");

    if (!container) {
        console.error("Results container not found");
        return;
    }

    if (!data) {
        container.innerHTML = "No results";
        return;
    }

    if (data.error) {
        container.innerHTML = `<pre>${data.error}</pre>`;
        return;
    }

    if (!Array.isArray(data) || data.length === 0) {
        container.innerHTML = "No data found";
        return;
    }

    const keys = Object.keys(data[0]);

    let html = "<table><tr>";

    keys.forEach(k => {
        html += `<th>${k}</th>`;
    });

    html += "</tr>";

    data.forEach(row => {
        html += "<tr>";
        keys.forEach(k => {
            html += `<td>${row[k]}</td>`;
        });
        html += "</tr>";
    });

    html += "</table>";

    container.innerHTML = html;
}

function copySQL() {
    const sqlBox = document.getElementById("sqlBox");

    if (!sqlBox) return;

    navigator.clipboard.writeText(sqlBox.innerText);
    alert("SQL copied!");
}