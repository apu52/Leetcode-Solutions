const state = {
  payload: null,
  search: "",
  language: "all",
  selectedDate: "",
  activeSolution: null,
  theme: "light",
};

const THEME_STORAGE_KEY = "leetcode-archive-theme";

const elements = {
  liveDate: document.querySelector("#live-date"),
  themeToggle: document.querySelector("#theme-toggle"),
  repoLink: document.querySelector("#repo-link"),
  totalSolutions: document.querySelector("#total-solutions"),
  totalLanguages: document.querySelector("#total-languages"),
  repoBirthDate: document.querySelector("#repo-birth-date"),
  todayCount: document.querySelector("#today-count"),
  todayPreview: document.querySelector("#today-preview"),
  todayHighlight: document.querySelector("#today-highlight"),
  latestGrid: document.querySelector("#latest-grid"),
  datePicker: document.querySelector("#date-picker"),
  jumpToday: document.querySelector("#jump-today"),
  selectedDateSummary: document.querySelector("#selected-date-summary"),
  selectedDateTitle: document.querySelector("#selected-date-title"),
  selectedDateGrid: document.querySelector("#selected-date-grid"),
  searchInput: document.querySelector("#search-input"),
  languageFilter: document.querySelector("#language-filter"),
  resultsCount: document.querySelector("#results-count"),
  solutionsGrid: document.querySelector("#solutions-grid"),
  cardTemplate: document.querySelector("#solution-card-template"),
  codeModal: document.querySelector("#code-modal"),
  modalTitle: document.querySelector("#modal-title"),
  modalMeta: document.querySelector("#modal-meta"),
  modalLanguage: document.querySelector("#modal-language"),
  modalFileName: document.querySelector("#modal-file-name"),
  modalSourceLink: document.querySelector("#modal-source-link"),
  modalCode: document.querySelector("#modal-code"),
  modalClose: document.querySelector("#modal-close"),
  copyCode: document.querySelector("#copy-code"),
};

const KEYWORDS = new Set([
  "and", "as", "break", "case", "catch", "class", "const", "continue", "def", "default", "delete",
  "do", "elif", "else", "enum", "except", "export", "extends", "false", "finally", "for", "from",
  "function", "if", "import", "in", "interface", "lambda", "let", "match", "namespace", "new", "nil",
  "not", "null", "or", "package", "private", "protected", "public", "raise", "return", "static", "struct",
  "switch", "template", "this", "throw", "true", "try", "typedef", "typename", "using", "var", "void",
  "while", "with", "yield", "final", "override", "virtual", "constexpr", "auto", "await", "async"
]);

const TYPES = new Set([
  "bool", "char", "double", "float", "int", "list", "long", "map", "set", "string", "tuple", "vector",
  "unordered_map", "unordered_set", "TreeNode", "ListNode", "Solution", "String", "Integer"
]);

function getCurrentDateKey() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function formatDate(value) {
  const date = new Date(`${value}T00:00:00`);
  return new Intl.DateTimeFormat("en", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(date);
}

function formatLiveDate() {
  return new Intl.DateTimeFormat("en", {
    weekday: "long",
    day: "2-digit",
    month: "long",
    year: "numeric",
  }).format(new Date());
}

function escapeHtml(value) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function wrapToken(className, value) {
  return `<span class="${className}">${escapeHtml(value)}</span>`;
}

function tokenizeLine(line) {
  const tokens = [];
  let index = 0;

  while (index < line.length) {
    const current = line[index];
    const next = line[index + 1] || "";

    if (current === "/" && next === "/") {
      tokens.push(wrapToken("token-comment", line.slice(index)));
      break;
    }

    if (current === "#") {
      tokens.push(wrapToken("token-comment", line.slice(index)));
      break;
    }

    if (current === '"' || current === "'") {
      let end = index + 1;
      while (end < line.length) {
        if (line[end] === "\\") {
          end += 2;
          continue;
        }
        if (line[end] === current) {
          end += 1;
          break;
        }
        end += 1;
      }
      tokens.push(wrapToken("token-string", line.slice(index, end)));
      index = end;
      continue;
    }

    if (/\d/.test(current)) {
      let end = index + 1;
      while (end < line.length && /[\d.]/.test(line[end])) {
        end += 1;
      }
      tokens.push(wrapToken("token-number", line.slice(index, end)));
      index = end;
      continue;
    }

    if (/[A-Za-z_]/.test(current)) {
      let end = index + 1;
      while (end < line.length && /[A-Za-z0-9_]/.test(line[end])) {
        end += 1;
      }
      const word = line.slice(index, end);
      if (KEYWORDS.has(word)) {
        tokens.push(wrapToken("token-keyword token-strong", word));
      } else if (TYPES.has(word)) {
        tokens.push(wrapToken("token-type token-strong", word));
      } else {
        tokens.push(escapeHtml(word));
      }
      index = end;
      continue;
    }

    tokens.push(escapeHtml(current));
    index += 1;
  }

  return tokens.join("");
}

function applySyntaxHighlight(code) {
  const normalized = code.replace(/\r/g, "");
  const lines = normalized.split("\n");

  return lines
    .map((line, index) => {
      const renderedLine = tokenizeLine(line);
      const lineNumber = String(index + 1).padStart(2, " ");
      return `<span class="code-line"><span class="line-number">${lineNumber}</span><span class="line-content">${renderedLine || " "}</span></span>`;
    })
    .join("");
}

function renderPreviewMarkup(code, maxLines = 4) {
  const lines = code.replace(/\r/g, "").split("\n").slice(0, maxLines);
  const body = lines
    .map((line) => `<span class="preview-line">${tokenizeLine(line) || " "}</span>`)
    .join("");

  return `
    <div class="preview-grid">
      <div class="preview-code">${body}</div>
      <div class="preview-fade"></div>
    </div>
  `;
}

function getPreferredTheme() {
  const storedTheme = window.localStorage.getItem(THEME_STORAGE_KEY);
  if (storedTheme === "light" || storedTheme === "dark") {
    return storedTheme;
  }

  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function applyTheme(theme) {
  state.theme = theme;
  document.documentElement.dataset.theme = theme;
  elements.themeToggle.textContent = theme === "dark" ? "Light mode" : "Dark mode";
}

function toggleTheme() {
  const nextTheme = state.theme === "dark" ? "light" : "dark";
  window.localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
  applyTheme(nextTheme);
}

function getTodaySolution() {
  const todayKey = getCurrentDateKey();

  if (!state.payload) {
    return { todayKey, todaySolutions: [], fallback: null };
  }

  const todaySolutions = state.payload.solutions.filter((solution) => solution.createdDate === todayKey);
  const fallback = state.payload.solutions.find((solution) => solution.createdDate < todayKey) || state.payload.stats.latestAddition;

  return { todayKey, todaySolutions, fallback };
}

function renderTodayHighlight() {
  const { todayKey, todaySolutions, fallback } = getTodaySolution();
  elements.todayCount.textContent = String(todaySolutions.length);

  if (todaySolutions.length > 0) {
    const latestToday = todaySolutions[0];
    elements.todayPreview.innerHTML = renderPreviewMarkup(latestToday.code, 7);
    elements.todayHighlight.innerHTML = `
      <span class="today-badge">Added today</span>
      <strong>#${latestToday.problemNumber} ${escapeHtml(latestToday.title)}</strong>
      <span>${escapeHtml(latestToday.language)}</span>
      <span>${todaySolutions.length} problem${todaySolutions.length === 1 ? "" : "s"} added on ${formatDate(todayKey)}</span>
      <button class="source-link" type="button" data-view-problem="${latestToday.problemNumber}">View code</button>
    `;
    return;
  }

  if (!fallback) {
    elements.todayPreview.innerHTML = "";
    elements.todayHighlight.innerHTML = "<strong>No solutions found yet.</strong>";
    return;
  }

  elements.todayPreview.innerHTML = renderPreviewMarkup(fallback.code, 7);
  elements.todayHighlight.innerHTML = `
    <span class="status-badge">No problem added today</span>
    <strong>#${fallback.problemNumber} ${escapeHtml(fallback.title)}</strong>
    <span class="fallback-note">Latest previous upload was on ${formatDate(fallback.createdDate)}</span>
    <button class="source-link" type="button" data-view-problem="${fallback.problemNumber}">View previous latest</button>
  `;
}

function createCard(solution, compact = false) {
  const fragment = elements.cardTemplate.content.cloneNode(true);
  const card = fragment.querySelector(".solution-card");
  const preview = fragment.querySelector(".card-preview");
  const number = fragment.querySelector(".problem-number");
  const language = fragment.querySelector(".language-pill");
  const title = fragment.querySelector(".problem-title");
  const fileName = fragment.querySelector(".file-name");
  const createdAt = fragment.querySelector(".created-at");
  const viewButton = fragment.querySelector(".view-code-button");

  if (compact) {
    card.classList.add("latest-card");
  }

  preview.innerHTML = renderPreviewMarkup(solution.code, compact ? 3 : 3);
  number.textContent = `#${solution.problemNumber}`;
  language.textContent = solution.language;
  title.textContent = solution.title;
  fileName.textContent = solution.fileName;
  createdAt.textContent = `Added ${formatDate(solution.createdDate)}`;
  viewButton.dataset.viewProblem = String(solution.problemNumber);
  viewButton.textContent = compact ? "Open code" : "View code";

  return fragment;
}

function renderCardGrid(container, solutions, emptyMessage) {
  container.innerHTML = "";

  if (!solutions.length) {
    container.innerHTML = `<div class="empty-state">${emptyMessage}</div>`;
    return;
  }

  solutions.forEach((solution) => {
    container.appendChild(createCard(solution));
  });
}

function renderLatestGrid(latestSolutions) {
  elements.latestGrid.innerHTML = "";
  latestSolutions.forEach((solution) => {
    elements.latestGrid.appendChild(createCard(solution, true));
  });
}

function getFilteredSolutions() {
  const allSolutions = state.payload?.solutions || [];
  const search = state.search.trim().toLowerCase();

  return allSolutions.filter((solution) => {
    const matchesLanguage = state.language === "all" || solution.language.toLowerCase() === state.language.toLowerCase();
    if (!matchesLanguage) {
      return false;
    }

    if (!search) {
      return true;
    }

    return [String(solution.problemNumber), solution.title, solution.fileName, solution.language, solution.createdDate]
      .join(" ")
      .toLowerCase()
      .includes(search);
  });
}

function renderSolutions() {
  const filteredSolutions = getFilteredSolutions();
  elements.resultsCount.textContent = `${filteredSolutions.length} solution${filteredSolutions.length === 1 ? "" : "s"} shown`;
  renderCardGrid(elements.solutionsGrid, filteredSolutions, "No matching solution found. Try a different title, number, date text, or language.");
}

function renderFilters(languages) {
  const options = ['<option value="all">All languages</option>'].concat(
    languages.map((language) => `<option value="${language.name}">${language.name} (${language.count})</option>`)
  );

  elements.languageFilter.innerHTML = options.join("");
}

function renderStats(payload) {
  elements.totalSolutions.textContent = String(payload.stats.totalSolutions);
  elements.totalLanguages.textContent = String(payload.stats.totalLanguages);
  elements.repoBirthDate.textContent = formatDate(payload.repoBirthDate);
  elements.repoLink.href = payload.repoUrl || "#";
  elements.liveDate.textContent = formatLiveDate();
}

function renderSelectedDate() {
  const selectedDate = state.selectedDate || getCurrentDateKey();
  const solutions = state.payload.solutions.filter((solution) => solution.createdDate === selectedDate);
  const hasSolutions = solutions.length > 0;

  elements.selectedDateTitle.textContent = hasSolutions
    ? `${formatDate(selectedDate)} archive`
    : `${formatDate(selectedDate)} has no uploads`;

  elements.selectedDateSummary.innerHTML = hasSolutions
    ? `<strong>${solutions.length} problem${solutions.length === 1 ? "" : "s"} added on ${formatDate(selectedDate)}</strong>`
    : `<strong>No files on ${formatDate(selectedDate)}</strong><span class="summary-note">The site keeps the date available so people can verify that nothing was posted that day.</span>`;

  renderCardGrid(
    elements.selectedDateGrid,
    solutions,
    `No files were added on ${formatDate(selectedDate)}. Choose another past date to see solutions from that day.`
  );
}

function openCodeModal(solution) {
  state.activeSolution = solution;
  elements.modalTitle.innerHTML = `<span class="modal-problem-id">#${solution.problemNumber}</span> ${escapeHtml(solution.title)}`;
  elements.modalMeta.textContent = `${solution.fileName} � Added ${formatDate(solution.createdDate)}`;
  elements.modalLanguage.textContent = solution.language;
  elements.modalFileName.textContent = solution.fileName;
  elements.modalSourceLink.href = solution.sourceUrl || "#";
  elements.modalCode.innerHTML = applySyntaxHighlight(solution.code);
  elements.codeModal.showModal();
}

function closeCodeModal() {
  if (elements.codeModal.open) {
    elements.codeModal.close();
  }
}

async function copyActiveCode() {
  if (!state.activeSolution) {
    return;
  }

  try {
    await navigator.clipboard.writeText(state.activeSolution.code);
    elements.copyCode.textContent = "Copied";
    window.setTimeout(() => {
      elements.copyCode.textContent = "Copy code";
    }, 1500);
  } catch {
    elements.copyCode.textContent = "Copy failed";
    window.setTimeout(() => {
      elements.copyCode.textContent = "Copy code";
    }, 1500);
  }
}

function handleViewCode(problemNumber) {
  const solution = state.payload?.solutions.find((item) => String(item.problemNumber) === String(problemNumber));
  if (solution) {
    openCodeModal(solution);
  }
}

function clampDateToAllowedRange(dateValue) {
  const todayKey = getCurrentDateKey();
  if (dateValue < state.payload.repoBirthDate) {
    return state.payload.repoBirthDate;
  }

  if (dateValue > todayKey) {
    return todayKey;
  }

  return dateValue;
}

function wireEvents() {
  elements.searchInput.addEventListener("input", (event) => {
    state.search = event.target.value;
    renderSolutions();
  });

  elements.languageFilter.addEventListener("change", (event) => {
    state.language = event.target.value;
    renderSolutions();
  });

  elements.datePicker.addEventListener("change", (event) => {
    state.selectedDate = clampDateToAllowedRange(event.target.value);
    elements.datePicker.value = state.selectedDate;
    renderSelectedDate();
  });

  elements.jumpToday.addEventListener("click", () => {
    state.selectedDate = clampDateToAllowedRange(getCurrentDateKey());
    elements.datePicker.value = state.selectedDate;
    renderSelectedDate();
  });

  elements.themeToggle.addEventListener("click", toggleTheme);

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-view-problem]");
    if (trigger) {
      handleViewCode(trigger.dataset.viewProblem);
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeCodeModal();
    }
  });

  elements.modalClose.addEventListener("click", closeCodeModal);
  elements.copyCode.addEventListener("click", copyActiveCode);
  elements.codeModal.addEventListener("close", () => {
    state.activeSolution = null;
  });
}

async function loadSolutions() {
  const response = await fetch("./assets/data/solutions.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Unable to load solution data.");
  }

  return response.json();
}

async function init() {
  applyTheme(getPreferredTheme());
  wireEvents();

  try {
    const payload = await loadSolutions();
    const todayKey = getCurrentDateKey();
    const initialDate = todayKey < payload.repoBirthDate ? payload.repoBirthDate : todayKey;

    state.payload = payload;
    state.selectedDate = initialDate;

    elements.datePicker.min = payload.repoBirthDate;
    elements.datePicker.max = todayKey;
    elements.datePicker.value = initialDate;

    renderStats(payload);
    renderTodayHighlight();
    renderLatestGrid(payload.latest);
    renderFilters(payload.languages);
    renderSelectedDate();
    renderSolutions();
  } catch (error) {
    elements.todayHighlight.textContent = error.message;
    elements.selectedDateGrid.innerHTML = '<div class="empty-state">The site data could not be loaded yet. Run the generator or wait for the GitHub Pages build.</div>';
    elements.solutionsGrid.innerHTML = '<div class="empty-state">The site data could not be loaded yet. Run the generator or wait for the GitHub Pages build.</div>';
  }
}

init();
