const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const repoRoot = path.resolve(__dirname, "..");
const docsDir = path.join(repoRoot, "docs");
const dataDir = path.join(docsDir, "assets", "data");
const outputPath = path.join(dataDir, "solutions.json");

const SUPPORTED_EXTENSIONS = new Map([
  ["py", "Python"],
  ["cpp", "C++"],
  ["cc", "C++"],
  ["cxx", "C++"],
  ["c", "C"],
  ["java", "Java"],
  ["js", "JavaScript"],
  ["ts", "TypeScript"],
  ["cs", "C#"],
  ["go", "Go"],
  ["rb", "Ruby"],
  ["php", "PHP"],
  ["swift", "Swift"],
  ["kt", "Kotlin"],
  ["rs", "Rust"],
]);

function normalizeTitle(title) {
  return title.replace(/[_]+/g, " ").replace(/\s+/g, " ").replace(/\s+,/g, ",").trim();
}

function parseSolutionFile(fileName) {
  const extension = path.extname(fileName).slice(1).toLowerCase();
  if (!SUPPORTED_EXTENSIONS.has(extension)) {
    return null;
  }

  const nameWithoutExtension = path.basename(fileName, path.extname(fileName));
  const match = nameWithoutExtension.match(/^(\d+)\.\s*(.+)$/);
  if (!match) {
    return null;
  }

  return {
    fileName,
    problemNumber: Number(match[1]),
    title: normalizeTitle(match[2]),
    extension,
    language: SUPPORTED_EXTENSIONS.get(extension),
  };
}

function runGitCommand(command) {
  try {
    return execSync(command, {
      cwd: repoRoot,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
      maxBuffer: 1024 * 1024 * 20,
    }).trim();
  } catch {
    return "";
  }
}

function getMetadataOverride() {
  const metadataPath = process.env.SITE_GIT_METADATA_PATH;
  if (!metadataPath || !fs.existsSync(metadataPath)) {
    return null;
  }

  try {
    return JSON.parse(fs.readFileSync(metadataPath, "utf8").replace(/^\uFEFF/, ""));
  } catch {
    return null;
  }
}

function getRepoUrl() {
  const directResults = [
    runGitCommand("git remote get-url origin"),
    runGitCommand("git config --get remote.origin.url"),
  ].filter(Boolean);

  if (directResults[0]) {
    return directResults[0].replace(/\.git$/, "");
  }

  try {
    const gitConfig = fs.readFileSync(path.join(repoRoot, ".git", "config"), "utf8");
    const lines = gitConfig.split(/\r?\n/);
    let inOrigin = false;

    for (const rawLine of lines) {
      const line = rawLine.trim();
      if (line.startsWith("[")) {
        inOrigin = line === '[remote "origin"]';
        continue;
      }

      if (inOrigin && line.startsWith("url = ")) {
        return line.slice("url = ".length).trim().replace(/\.git$/, "");
      }
    }
  } catch {
    return "";
  }

  return "";
}

function getAddedDates() {
  const logOutput = runGitCommand("git log --diff-filter=A --name-only --format=__DATE__%aI -- .");
  if (!logOutput) {
    return new Map();
  }

  const addedDates = new Map();
  let currentDate = "";

  for (const rawLine of logOutput.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line) {
      continue;
    }

    if (line.startsWith("__DATE__")) {
      currentDate = line.replace("__DATE__", "").trim();
      continue;
    }

    if (!addedDates.has(line) && currentDate) {
      addedDates.set(line, currentDate);
    }
  }

  return addedDates;
}

function getRepoBirthDate(addedDates, fallbackSolutions) {
  const commitHistory = runGitCommand("git log --format=%aI");
  if (commitHistory) {
    const commitDates = commitHistory.split(/\r?\n/).filter(Boolean);
    return commitDates[commitDates.length - 1].slice(0, 10);
  }

  const addedDateValues = Array.from(addedDates.values()).map((value) => value.slice(0, 10));
  if (addedDateValues.length) {
    return addedDateValues.sort()[0];
  }

  const fallbackDates = fallbackSolutions.map((solution) => solution.createdDate).sort();
  return fallbackDates[0] || new Date().toISOString().slice(0, 10);
}

function getFileAddedDate(fileName, addedDates) {
  if (addedDates.has(fileName)) {
    return addedDates.get(fileName);
  }

  const escapedFileName = fileName.replace(/"/g, '\\"');
  const fileHistory = runGitCommand(`git log --diff-filter=A --format=%aI -- "${escapedFileName}"`);
  if (!fileHistory) {
    return "";
  }

  const createdAt = fileHistory.split(/\r?\n/).filter(Boolean)[0] || "";
  if (createdAt) {
    addedDates.set(fileName, createdAt);
  }

  return createdAt;
}

function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

function buildSourceUrl(repoUrl, fileName) {
  if (!repoUrl) {
    return fileName;
  }

  return `${repoUrl}/blob/main/${encodeURIComponent(fileName).replace(/%2F/g, "/")}`;
}

function main() {
  const metadataOverride = getMetadataOverride();
  const repoUrl = metadataOverride?.repoUrl || getRepoUrl();
  const addedDates = metadataOverride?.addedDates ? new Map(Object.entries(metadataOverride.addedDates)) : getAddedDates();

  const solutionFiles = fs
    .readdirSync(repoRoot, { withFileTypes: true })
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name)
    .map(parseSolutionFile)
    .filter(Boolean);

  const solutions = solutionFiles
    .map((solution) => {
      const fullPath = path.join(repoRoot, solution.fileName);
      const stats = fs.statSync(fullPath);
      const createdAt = getFileAddedDate(solution.fileName, addedDates) || stats.mtime.toISOString();
      const createdDate = createdAt.slice(0, 10);

      return {
        ...solution,
        fileSize: stats.size,
        createdAt,
        createdDate,
        code: fs.readFileSync(fullPath, "utf8"),
        sourceUrl: buildSourceUrl(repoUrl, solution.fileName),
      };
    })
    .sort((left, right) => {
      const timeDiff = new Date(right.createdAt).getTime() - new Date(left.createdAt).getTime();
      if (timeDiff !== 0) {
        return timeDiff;
      }

      return right.problemNumber - left.problemNumber;
    });

  const languages = Array.from(
    solutions.reduce((map, solution) => {
      map.set(solution.language, (map.get(solution.language) || 0) + 1);
      return map;
    }, new Map())
  )
    .sort((left, right) => right[1] - left[1] || left[0].localeCompare(right[0]))
    .map(([name, count]) => ({ name, count }));

  const solutionsByDate = solutions.reduce((map, solution) => {
    if (!map[solution.createdDate]) {
      map[solution.createdDate] = [];
    }

    map[solution.createdDate].push({
      fileName: solution.fileName,
      problemNumber: solution.problemNumber,
      title: solution.title,
      language: solution.language,
    });

    return map;
  }, {});

  const generatedAt = new Date().toISOString();
  const generatedDate = generatedAt.slice(0, 10);
  const todaySolutions = solutions.filter((solution) => solution.createdDate === generatedDate);
  const latestAddition = solutions[0] || null;
  const latestBeforeToday = solutions.find((solution) => solution.createdDate < generatedDate) || latestAddition;

  const payload = {
    generatedAt,
    generatedDate,
    repoBirthDate: metadataOverride?.repoBirthDate || getRepoBirthDate(addedDates, solutions),
    repoUrl,
    stats: {
      totalSolutions: solutions.length,
      totalLanguages: languages.length,
      latestAddition,
      todaySolutionsCount: todaySolutions.length,
      latestBeforeToday,
    },
    languages,
    latest: solutions.slice(0, 6),
    solutionsByDate,
    solutions,
  };

  ensureDir(dataDir);
  fs.writeFileSync(outputPath, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  console.log(`Generated ${solutions.length} solutions into ${path.relative(repoRoot, outputPath)}`);
}

main();
