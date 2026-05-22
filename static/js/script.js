// --- Elemen DOM ---
const forms           = document.querySelectorAll("form.calc-form");
const resultPanel     = document.getElementById("resultPanel");
const historyList     = document.getElementById("historyList");
const emptyHistory    = document.getElementById("emptyHistory");
const themeToggle     = document.getElementById("themeToggle");
const clearHistoryBtn = document.getElementById("clearHistory");
const logikaOperator  = document.getElementById("logikaOperator");
const logikaBGroup    = document.getElementById("logikaBGroup");

// --- Sound effect ---
const clickSound   = new Audio("/static/suaratambahan/efektekan.mp3");
const resultSound  = new Audio("/static/suaratambahan/efekhasil.mp3");

// --- Riwayat dari LocalStorage ---
let history = JSON.parse(localStorage.getItem("calcHistory") || "[]");

// --- Inisialisasi Awal ---
renderHistory();
applySavedTheme();
updateLogikaFields();

// --- Efek klik pada semua tombol ---
document.querySelectorAll("button").forEach((button) => {
  button.addEventListener("click", () => {
    clickSound.currentTime = 0;
    clickSound.play().catch(() => {});
  });
});

// --- Event Submit Semua Form ---
forms.forEach((form) => form.addEventListener("submit", handleFormSubmit));

// --- Toggle Dark / Light Mode ---
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");
  const isDark = document.body.classList.contains("dark-mode");
  themeToggle.textContent = isDark ? "Light Mode" : "Dark Mode";
  localStorage.setItem("themeMode", isDark ? "dark" : "light");
});

// --- Hapus Semua Riwayat ---
clearHistoryBtn.addEventListener("click", () => {
  history = [];
  localStorage.removeItem("calcHistory");
  renderHistory();
});

// --- Tampilkan / Sembunyikan Input B pada NOT ---
logikaOperator.addEventListener("change", updateLogikaFields);

function updateLogikaFields() {
  const isNot = logikaOperator.value === "not";
  logikaBGroup.style.display = isNot ? "none" : "block";
  logikaBGroup.querySelector("select").toggleAttribute("required", !isNot);
}

// --- Kirim Form ke Backend ---
async function handleFormSubmit(event) {
  event.preventDefault();
  const form   = event.currentTarget;
  const apiUrl = form.dataset.api;
  const label  = form.dataset.label;

  // --- Kumpulkan Data Form ---
  const body = {};
  new FormData(form).forEach((value, key) => (body[key] = value.trim()));

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    if (!response.ok) { renderError(data.error || "Terjadi kesalahan."); return; }

    renderResult(data, label);
    addToHistory(label, data);

  } catch {
    renderError("Tidak bisa terhubung ke server.");
  }
}

// --- Tampilkan Hasil ke Panel ---
function renderResult(data, category) {
  const stepsHtml = data.steps
    ? `<ol class="ps-3 mb-0">${data.steps.map((s) => `<li>${s}</li>`).join("")}</ol>`
    : "";

  resultPanel.innerHTML = `
    <div class="mb-3"><span class="badge bg-info text-dark">${category}</span></div>
    <p class="mb-1"><strong>Hasil:</strong> ${formatResult(data)}</p>
    <p class="mb-1"><strong>Formula:</strong> ${data.formula || "-"}</p>
    <div><strong>Langkah:</strong>${stepsHtml}</div>
  `;

  resultSound.currentTime = 0;
  resultSound.play().catch(() => {});
}

// --- Format Hasil (Array atau Angka) ---
function formatResult(data) {
  return Array.isArray(data.result) ? data.result.join(", ") : data.result;
}

// --- Tampilkan Pesan Error ---
function renderError(message) {
  resultPanel.innerHTML = `
    <div class="alert alert-danger mb-0" role="alert">
      <strong>Kesalahan:</strong> ${message}
    </div>
  `;
}

// --- Simpan Entri ke Riwayat ---
function addToHistory(label, data) {
  const entry = {
    id: Date.now(),
    timestamp: new Date().toLocaleString("id-ID", {
      hour: "2-digit", minute: "2-digit",
      day: "2-digit", month: "2-digit", year: "numeric",
    }),
    category: label,
    formula:  data.formula || "-",
    result:   formatResult(data),
  };

  history.unshift(entry);
  if (history.length > 10) history.pop();
  localStorage.setItem("calcHistory", JSON.stringify(history));
  renderHistory();
}

// --- Render Daftar Riwayat ---
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

// --- Terapkan Tema Tersimpan ---
function applySavedTheme() {
  const isDark = localStorage.getItem("themeMode") === "dark";
  document.body.classList.toggle("dark-mode", isDark);
  themeToggle.textContent = isDark ? "Light Mode" : "Dark Mode";
}