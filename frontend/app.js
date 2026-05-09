async function generateSQL() {

    const input = document.getElementById("input");
    const chatBox = document.getElementById("chat-box");

    const question = input.value;

    if (!question) return;

    chatBox.innerHTML += `
        <div class="message user">
            ${question}
        </div>
    `;

    input.value = "";

    const res = await fetch("http://127.0.0.1:8000/generate-sql", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ question })
    });

    const data = await res.json();

    chatBox.innerHTML += `
    <div class="message ai">
        <strong>SQL:</strong><br>
        <code>${data.sql}</code>

        <br><br>

        <button onclick="copySQL(\`${data.sql}\`)">
            Copy SQL
        </button>
    </div>
`;
function copySQL(sql) {
    navigator.clipboard.writeText(sql);
    alert("SQL copied!");
}

    chatBox.scrollTop = chatBox.scrollHeight;
}