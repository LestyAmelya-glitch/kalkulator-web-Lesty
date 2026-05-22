// --- Elemen DOM ---
const forms           = document.querySelectorAll("form.calc-form");
const resultCard      = document.getElementById("resultCard");
const resultPanel     = document.getElementById("resultPanel");
const saveHistoryBtn  = document.getElementById("saveHistory");
const closeResultBtn  = document.getElementById("closeResult");
const historyWrapper  = document.getElementById("historyWrapper");
const historyCard     = document.getElementById("historyCard");
const historyList     = document.getElementById("historyList");
const emptyHistory    = document.getElementById("emptyHistory");
const themeToggle     = document.getElementById("themeToggle");
const clearHistoryBtn = document.getElementById("clearHistory");
const logikaOperator  = document.getElementById("logikaOperator");
const logikaBGroup    = document.getElementById("logikaBGroup");

let pendingResult = null;

// --- Sound effect ---
const clickSound   = new Audio("/static/suaratambahan/efektekan.mp3");
const resultSound  = new Audio("/static/suaratambahan/efekhasil.mp3");

// --- Riwayat dari LocalStorage ---
let history = JSON.parse(localStorage.getItem("calcHistory") || "[]");

// --- Inisialisasi Awal ---
renderHistory();
applySavedTheme();
updateLogikaFields();

// --- Transformasi: chooser compact handler ---
const transformChooser   = document.getElementById("transformChooser");
const transformAccordion = document.getElementById("transformAccordion");
const transformChoices   = document.querySelectorAll(".transform-choice");
const transformBackBtn   = document.getElementById("transformBack");
const transformTabButton = document.querySelector('button[data-bs-target="#transformasi"]');

if (transformTabButton) {
  transformTabButton.addEventListener('shown.bs.tab', () => {
    if (transformChooser) transformChooser.classList.remove('d-none');
    if (transformAccordion) transformAccordion.classList.add('d-none');
    // collapse any open panels
    document.querySelectorAll('#transformAccordion .accordion-collapse.show').forEach(c => {
      const inst = bootstrap.Collapse.getInstance(c);
      if (inst) inst.hide();
    });
  });
}

transformChoices.forEach((btn) => {
  btn.addEventListener('click', (e) => {
    const target = btn.dataset.target; // e.g. #basisCollapse
    if (!target) return;
    transformChooser.classList.add('d-none');
    transformAccordion.classList.remove('d-none');
    const collapseEl = document.querySelector(target);
    if (collapseEl) {
      // Hide other open collapses first
      document.querySelectorAll('#transformAccordion .accordion-collapse.show').forEach(c => {
        const inst = bootstrap.Collapse.getInstance(c);
        if (inst) inst.hide();
      });
      // show requested collapse
      new bootstrap.Collapse(collapseEl, { toggle: true });
      collapseEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  });
});

if (transformBackBtn) {
  transformBackBtn.addEventListener('click', () => {
    transformChooser.classList.remove('d-none');
    transformAccordion.classList.add('d-none');
    document.querySelectorAll('#transformAccordion .accordion-collapse.show').forEach(c => {
      const inst = bootstrap.Collapse.getInstance(c);
      if (inst) inst.hide();
    });
  });
}

// --- Efek klik pada semua tombol ---
document.querySelectorAll("button").forEach((button) => {
  button.addEventListener("click", () => {
    clickSound.currentTime = 0;
    clickSound.play().catch(() => {});
  });
});

// --- Event Submit Semua Form ---
forms.forEach((form) => form.addEventListener("submit", handleFormSubmit));

// --- Tombol hasil ---
saveHistoryBtn.addEventListener("click", savePendingResult);
closeResultBtn.addEventListener("click", closeResultCard);

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

    showResult(data, label);

  } catch {
    renderError("Tidak bisa terhubung ke server.");
  }
}

// --- Tampilkan Hasil ke Panel ---
function showResult(data, category) {
  pendingResult = { category, data };

  const stepsHtml = data.steps
    ? `<ol class="ps-3 mb-0">${data.steps.map((s) => `<li>${s}</li>`).join("")}</ol>`
    : "";

  resultPanel.innerHTML = `
    <div class="mb-3"><span class="badge bg-info text-dark">${category}</span></div>
    <p class="mb-1"><strong>Hasil:</strong> ${formatResult(data)}</p>
    <p class="mb-1"><strong>Formula:</strong> ${data.formula || "-"}</p>
    <div><strong>Langkah:</strong>${stepsHtml}</div>
  `;

  resultCard.classList.remove("d-none");
  requestAnimationFrame(() => {
    resultCard.classList.add("show-popup");
  });

  resultSound.currentTime = 0;
  resultSound.play().catch(() => {});
}

function closeResultCard() {
  pendingResult = null;
  resultCard.classList.remove("show-popup");
  resultCard.addEventListener("transitionend", () => {
    if (!resultCard.classList.contains("show-popup")) {
      resultCard.classList.add("d-none");
    }
  }, { once: true });
}

function savePendingResult() {
  if (!pendingResult) return;
  addToHistory(pendingResult.category, pendingResult.data);
  closeResultCard();
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
    historyWrapper.classList.add("d-none");
    historyCard.classList.remove("show-popup");
    return;
  }

  historyWrapper.classList.remove("d-none");
  historyCard.classList.add("show-popup");

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