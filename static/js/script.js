/* Elemen utama */
const forms = document.querySelectorAll("form.calc-form");
const resultPanel = document.getElementById("resultPanel");
const historyList = document.getElementById("historyList");
const emptyHistory = document.getElementById("emptyHistory");
const themeToggle = document.getElementById("themeToggle");
const clearHistoryBtn = document.getElementById("clearHistory");
const logikaOperator = document.getElementById("logikaOperator");
const logikaBGroup = document.getElementById("logikaBGroup");

/* Riwayat lokal */
let history = JSON.parse(localStorage.getItem("calcHistory") || "[]");

/* Inisialisasi tampilan */
renderHistory();
applySavedTheme();
updateLogikaFields();

/* Event submit form */
forms.forEach((form) => {
  form.addEventListener("submit", handleFormSubmit);
});

/* Toggle tema */
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  const mode = document.body.classList.contains("dark-mode") ? "dark" : "light";
  themeToggle.textContent = document.body.classList.contains("dark-mode") ? "Light Mode" : "Dark Mode";
  localStorage.setItem("themeMode", mode);
});

/* Hapus riwayat */
clearHistoryBtn.addEventListener("click", () => {
  history = [];
  localStorage.removeItem("calcHistory");
  renderHistory();
});

/* Tampilkan/sembunyikan B untuk NOT */
logikaOperator.addEventListener("change", updateLogikaFields);

/* Atur field logika */
function updateLogikaFields() {
  if (logikaOperator.value === "not") {
    logikaBGroup.style.display = "none";
    logikaBGroup.querySelector("select").removeAttribute("required");
  } else {
    logikaBGroup.style.display = "block";
    logikaBGroup.querySelector("select").setAttribute("required", "true");
  }
}

/* Kirim data ke backend */
async function handleFormSubmit(event) {
  event.preventDefault();

  const form = event.currentTarget;
  const apiUrl = form.dataset.api;
  const label = form.dataset.label;
  const formData = new FormData(form);
  const body = {};

  formData.forEach((value, key) => {
    body[key] = value.trim();
  });

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (!response.ok) {
      renderError(data.error || "Terjadi kesalahan.");
      return;
    }

    renderResult(data, label);
    addToHistory(label, data);
  } catch (error) {
    renderError("Tidak bisa terhubung ke server.");
  }
}

/* Tampilkan hasil */
function renderResult(data, category) {
  const stepsHtml = data.steps
    ? `<ol class="ps-3 mb-0">${data.steps.map((step) => `<li>${step}</li>`).join("")}</ol>`
    : "";

  resultPanel.innerHTML = `
    <div class="mb-3"><span class="badge bg-info text-dark">${category}</span></div>
    <p class="mb-1"><strong>Hasil:</strong> ${formatResult(data)}</p>
    <p class="mb-1"><strong>Formula:</strong> ${data.formula || "-"}</p>
    <div><strong>Langkah:</strong>${stepsHtml}</div>
  `;
}

/* Format hasil */
function formatResult(data) {
  if (Array.isArray(data.result)) {
    return data.result.join(", ");
  }
  return data.result;
}

/* Tampilkan error */
function renderError(message) {
  resultPanel.innerHTML = `
    <div class="alert alert-danger mb-0" role="alert">
      <strong>Kesalahan:</strong> ${message}
    </div>
  `;
}

/* Tambah riwayat */
function addToHistory(label, data) {
  const entry = {
    id: Date.now(),
    timestamp: new Date().toLocaleString("id-ID", {
      hour: "2-digit",
      minute: "2-digit",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    }),
    category: label,
    formula: data.formula || "-",
    result: formatResult(data),
  };

  history.unshift(entry);
  if (history.length > 10) history.pop();

  localStorage.setItem("calcHistory", JSON.stringify(history));
  renderHistory();
}

/* Render riwayat */
function renderHistory() {
  historyList.innerHTML = "";

  if (history.length === 0) {
    emptyHistory.style.display = "block";
    return;
  }

  emptyHistory.style.display = "none";

  history.forEach((item) => {
    const node = document.createElement("div");
    node.className = "list-group-item bg-transparent";
    node.innerHTML = `
      <div class="d-flex justify-content-between align-items-center mb-1">
        <span class="fw-semibold">${item.category}</span>
        <small class="text-muted">${item.timestamp}</small>
      </div>
      <div class="small text-muted history-label">${item.formula}</div>
      <div class="mt-2"><strong>Hasil:</strong> ${item.result}</div>
    `;
    historyList.appendChild(node);
  });
}

/* Tema tersimpan */
function applySavedTheme() {
  const mode = localStorage.getItem("themeMode") || "light";

  if (mode === "dark") {
    document.body.classList.add("dark-mode");
    themeToggle.textContent = "Light Mode";
  } else {
    document.body.classList.remove("dark-mode");
    themeToggle.textContent = "Dark Mode";
  }
}