// elemen utama
const forms           = document.querySelectorAll("form.calc-form");
const resultCard      = document.getElementById("resultCard");
const resultOverlay   = document.getElementById("resultOverlay");
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
const transformChooser        = document.getElementById("transformChooser");
const transformAccordion      = document.getElementById("transformAccordion");
const transformChoices        = document.querySelectorAll(".transform-choice");
const transformAccordionItems = document.querySelectorAll("#transformAccordion .accordion-item");
const transformTabButton      = document.querySelector('button[data-bs-target="#transformasi"]');

// suara
const clickSound  = new Audio("/static/suaratambahan/efektekan.mp3");
const resultSound = new Audio("/static/suaratambahan/efekhasil.mp3");

// data awal
let history       = JSON.parse(localStorage.getItem("calcHistory") || "[]");
let pendingResult = null;

// mapping gambar per operator logika
const logikaImages = {
  and:  { pisang: "andpisang.png",  blubery: "andblubery.png" },
  or:   { pisang: "orpisang.png",   blubery: "orblubery.png" },
  not:  { pisang: "notpisang.png",  blubery: "notblubery.png" },
  xor:  { pisang: "xorpisang.png",  blubery: "xorblubery.png" },
  nand: { pisang: "nandpisang.png", blubery: "nandblubery.png" },
  nor:  { pisang: "norpisang.png",  blubery: "norblubery.png" },
};

// mapping gambar per operator aritmatika
const operatorImages = {
  tambah:  { pisang: "tambahpisang.png",        blubery: "tambahblubery.png" },
  kurang:  { pisang: "kurangpisang.png",         blubery: "kurangblubery.png" },
  kali:    { pisang: "kalipisang.png",           blubery: "kaliblubery.png" },
  bagi:    { pisang: "bagipisang.png",           blubery: "bagiblubery.png" },
  pangkat: { pisang: "pangkatpisang.png",        blubery: "pangkatblubery.png" },
  akar:    { pisang: "akarpisang.png",           blubery: "akarblubery.png" },
  modulus: { pisang: "moduluspisang.png",        blubery: "modulusblubery.png" },
  floor:   { pisang: "floordivisionpisang.png",  blubery: "floodivisionblubery.png" },
};

// mapping gambar per tombol transformasi
const transformImages = {
  basis:    { pisang: "basisbilanganpisang.png", blubery: "basisbilanganblubery.png" },
  suhu:     { pisang: "suhupisang.png",             blubery: "suhublubery.png" },
  uang:     { pisang: "matauangpisang.png",         blubery: "matauangblubery.png" },
  faktorial:{ pisang: "faktorialpisang.png",        blubery: "faktorialblubery.png" },
  fibonacci:{ pisang: "fibonaccipisang.png",        blubery: "fibonacciblubery.png" },
};

// jalankan saat load
renderHistory();
applySavedTheme();
updateLogikaFields();
pageEntranceAnimation();
initOperatorPreview();
initLogikaPreview();

// transisi masuk
function pageEntranceAnimation() {
  document.body.style.opacity    = "0";
  document.body.style.transform  = "translateY(16px)";
  document.body.style.transition = "opacity 0.5s ease, transform 0.5s ease";
  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      document.body.style.opacity   = "1";
      document.body.style.transform = "translateY(0)";
    });
  });
}

// counting up animasi angka
function animateCountUp(element, targetValue) {
  const numericValue = parseFloat(targetValue);
  if (isNaN(numericValue)) { element.textContent = targetValue; return; }
  const isFloat   = targetValue.toString().includes(".");
  const decimals  = isFloat ? (targetValue.toString().split(".")[1]?.length || 2) : 0;
  const duration  = 800;
  const startTime = performance.now();
  function update(currentTime) {
    const elapsed  = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const eased    = 1 - Math.pow(1 - progress, 3);
    const current  = numericValue * eased;
    element.textContent = isFloat ? current.toFixed(decimals) : Math.round(current).toString();
    if (progress < 1) requestAnimationFrame(update);
    else element.textContent = targetValue;
  }
  requestAnimationFrame(update);
}

// helper ganti gambar dengan animasi pop
function swapImage(imgEl, newSrc) {
  if (!imgEl) return;
  imgEl.style.opacity   = "0";
  imgEl.style.transform = "scale(0.7) rotate(-8deg)";
  setTimeout(() => {
    imgEl.src             = newSrc;
    imgEl.style.opacity   = "1";
    imgEl.style.transform = "scale(1) rotate(0deg)";
  }, 180);
}

// preview gambar operator logika
function initLogikaPreview() {
  const logikaSelect = document.getElementById("logikaOperator");
  const previewImg   = document.getElementById("logikaPreview");
  if (!logikaSelect || !previewImg) return;

  function updatePreview() {
    const op    = logikaSelect.value;
    const isDark = document.body.classList.contains("dark-mode");
    const theme  = isDark ? "blubery" : "pisang";
    const imgs   = logikaImages[op];
    if (imgs) swapImage(previewImg, `/static/gambar/${imgs[theme]}`);
  }

  logikaSelect.addEventListener("change", updatePreview);
  updatePreview();
}

// update preview logika saat tema berubah
function updateLogikaPreview() {
  const logikaSelect = document.getElementById("logikaOperator");
  const previewImg   = document.getElementById("logikaPreview");
  if (!logikaSelect || !previewImg) return;
  const op    = logikaSelect.value;
  const isDark = document.body.classList.contains("dark-mode");
  const theme  = isDark ? "blubery" : "pisang";
  const imgs   = logikaImages[op];
  if (imgs) previewImg.src = `/static/gambar/${imgs[theme]}`;
}

// preview gambar operator aritmatika
function initOperatorPreview() {
  const operatorSelect = document.querySelector('select[name="operator"]');
  const previewImg     = document.getElementById("operatorPreview");
  if (!operatorSelect || !previewImg) return;

  function updatePreview() {
    const op    = operatorSelect.value;
    const isDark = document.body.classList.contains("dark-mode");
    const theme  = isDark ? "blubery" : "pisang";
    const imgs   = operatorImages[op];
    if (imgs) swapImage(previewImg, `/static/gambar/${imgs[theme]}`);
  }

  operatorSelect.addEventListener("change", updatePreview);
  updatePreview();
}

// update preview operator saat tema berubah
function updateOperatorPreview() {
  const operatorSelect = document.querySelector('select[name="operator"]');
  const previewImg     = document.getElementById("operatorPreview");
  if (!operatorSelect || !previewImg) return;
  const op    = operatorSelect.value;
  const isDark = document.body.classList.contains("dark-mode");
  const theme  = isDark ? "blubery" : "pisang";
  const imgs   = operatorImages[op];
  if (imgs) previewImg.src = `/static/gambar/${imgs[theme]}`;
}

// update semua preview transformasi saat tema berubah
function updateTransformPreviews() {
  const isDark = document.body.classList.contains("dark-mode");
  const theme  = isDark ? "blubery" : "pisang";
  Object.keys(transformImages).forEach((key) => {
    const img = document.getElementById(`transformPreview-${key}`);
    if (img && transformImages[key]) {
      img.src = `/static/gambar/${transformImages[key][theme]}`;
    }
  });
}

// klik tombol: suara + ripple
document.querySelectorAll("button").forEach((button) => {
  button.addEventListener("click", (e) => {
    playClickSound();
    addRipple(button, e);
  });
});

forms.forEach((form) => form.addEventListener("submit", handleFormSubmit));
saveHistoryBtn.addEventListener("click", savePendingResult);
closeResultBtn.addEventListener("click", closeResultCard);
themeToggle.addEventListener("click", toggleTheme);
clearHistoryBtn.addEventListener("click", clearAllHistory);
logikaOperator.addEventListener("change", updateLogikaFields);

if (transformTabButton) {
  transformTabButton.addEventListener("shown.bs.tab", backToTransformChooser);
}
transformChoices.forEach((btn) => {
  btn.addEventListener("click", () => showSelectedTransform(btn.dataset.target));
});
document.querySelectorAll(".transform-back-btn").forEach((btn) => {
  btn.addEventListener("click", backToTransformChooser);
});

function playClickSound() {
  clickSound.currentTime = 0;
  clickSound.play().catch(() => {});
}

function addRipple(button, event) {
  const ripple = document.createElement("span");
  ripple.classList.add("ripple");
  const rect = button.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  ripple.style.width  = ripple.style.height = `${size}px`;
  ripple.style.left   = `${event.clientX - rect.left - size / 2}px`;
  ripple.style.top    = `${event.clientY - rect.top  - size / 2}px`;
  button.appendChild(ripple);
  ripple.addEventListener("animationend", () => ripple.remove());
}

function toggleTheme() {
  const isDark = document.body.classList.toggle("dark-mode");
  themeToggle.textContent = isDark ? "Light Mode" : "Dark Mode";
  localStorage.setItem("themeMode", isDark ? "dark" : "light");
  updateMascot(isDark);
  updateOperatorPreview();
  updateLogikaPreview();
  updateTransformPreviews();
}

function updateMascot(isDark) {
  const mascot = document.getElementById("mascotImg");
  if (!mascot) return;
  mascot.src = isDark
    ? "/static/gambar/mengblueberry.png"
    : "/static/gambar/mengpisang.png";
}

function applySavedTheme() {
  const isDark = localStorage.getItem("themeMode") === "dark";
  document.body.classList.toggle("dark-mode", isDark);
  themeToggle.textContent = isDark ? "Light Mode" : "Dark Mode";
  updateMascot(isDark);
}

function updateLogikaFields() {
  const isNot = logikaOperator.value === "not";
  logikaBGroup.style.display = isNot ? "none" : "block";
  logikaBGroup.querySelector("select").toggleAttribute("required", !isNot);
}

function resetTransformAccordion() {
  transformAccordionItems.forEach((item) => item.classList.remove("d-none"));
  document.querySelectorAll("#transformAccordion .accordion-collapse").forEach((collapseEl) => {
    collapseEl.classList.remove("show");
    const toggleButton = document.querySelector(`[data-bs-target="#${collapseEl.id}"]`);
    if (toggleButton) toggleButton.classList.add("collapsed");
  });
}

function showSelectedTransform(target) {
  if (!target || !transformAccordion) return;
  const collapseEl   = document.querySelector(target);
  const selectedItem = collapseEl?.closest(".accordion-item");
  if (!collapseEl || !selectedItem) return;

  transformChooser.classList.add("d-none");
  transformAccordion.classList.remove("d-none");
  transformAccordionItems.forEach((item) => {
    item.classList.toggle("d-none", item !== selectedItem);
  });

  document.querySelectorAll("#transformAccordion .accordion-collapse.show").forEach((cur) => {
    const inst = bootstrap.Collapse.getInstance(cur);
    if (inst) inst.hide();
  });

  new bootstrap.Collapse(collapseEl, { toggle: true });
  collapseEl.scrollIntoView({ behavior: "smooth", block: "center" });
}

function backToTransformChooser() {
  if (transformChooser) transformChooser.classList.remove("d-none");
  if (transformAccordion) transformAccordion.classList.add("d-none");
  document.querySelectorAll("#transformAccordion .accordion-collapse.show").forEach((collapseEl) => {
    const inst = bootstrap.Collapse.getInstance(collapseEl);
    if (inst) inst.hide();
  });
  resetTransformAccordion();
}

async function handleFormSubmit(event) {
  event.preventDefault();
  const form   = event.currentTarget;
  const apiUrl = form.dataset.api;
  const label  = form.dataset.label;
  const body   = {};
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

function showResult(data, category) {
  pendingResult = { category, data };
  const stepsHtml = data.steps
    ? `<ol class="ps-3 mb-0">${data.steps.map((s) => `<li>${s}</li>`).join("")}</ol>`
    : "";

  resultPanel.innerHTML = `
    <div class="mb-3"><span class="badge bg-info text-dark">${category}</span></div>
    <p class="mb-1"><strong>Hasil:</strong> <span id="countUpValue">0</span></p>
    <p class="mb-1"><strong>Formula:</strong> ${data.formula || "-"}</p>
    <div><strong>Langkah:</strong>${stepsHtml}</div>
  `;

  resultOverlay.classList.remove("d-none");
  resultCard.classList.remove("d-none");
  requestAnimationFrame(() => {
    resultOverlay.classList.add("show");
    resultCard.classList.add("show-popup");
  });

  const countEl     = document.getElementById("countUpValue");
  const resultValue = formatResult(data);
  setTimeout(() => {
    if (Array.isArray(data.result)) countEl.textContent = resultValue;
    else animateCountUp(countEl, resultValue);
  }, 200);

  resultSound.currentTime = 0;
  resultSound.play().catch(() => {});
}

function formatResult(data) {
  return Array.isArray(data.result) ? data.result.join(", ") : data.result;
}

function renderError(message) {
  resultPanel.innerHTML = `
    <div class="alert alert-danger mb-0" role="alert">
      <strong>Kesalahan:</strong> ${message}
    </div>
  `;
}

function closeResultCard() {
  pendingResult = null;
  resultCard.classList.remove("show-popup");
  resultOverlay.classList.remove("show");
  const hideCard = () => {
    if (!resultCard.classList.contains("show-popup")) {
      resultCard.classList.add("d-none");
      resultOverlay.classList.add("d-none");
    }
  };
  resultCard.addEventListener("transitionend", hideCard, { once: true });
  resultOverlay.addEventListener("transitionend", hideCard, { once: true });
}

function savePendingResult() {
  if (!pendingResult) return;
  addToHistory(pendingResult.category, pendingResult.data);
  closeResultCard();
}

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

function clearAllHistory() {
  history = [];
  localStorage.removeItem("calcHistory");
  renderHistory();
}