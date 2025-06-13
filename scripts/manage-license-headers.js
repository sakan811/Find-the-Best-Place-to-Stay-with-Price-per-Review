/**
 * Script to manage license headers in source files
 * Run with: node scripts/manage-license-headers.js [add|remove|check]
 *
 * SakuYado - A web application that helps you find the best value accommodations
 * Copyright (C) 2025  Sakan Nirattisaykul
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

const fs = require("fs");
const path = require("path");
const readline = require("readline");

const LICENSE_HEADER = `/*
 * SakuYado - A web application that helps you find the best value accommodations
 * Copyright (C) 2025  Sakan Nirattisaykul
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 * 
 * along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */

`;

// File extensions to process
const EXTENSIONS = [".ts", ".tsx", ".js", ".jsx"];

// Directories to skip - use relative paths from project root
const SKIP_DIRS = [
  "node_modules",
  "__tests__",
  ".next",
  "dist",
  "build",
  "coverage",
  "out",
  ".git",
  "scripts", // Skip the scripts directory to avoid modifying this file
];

// Files to skip
const SKIP_FILES = ["next-env.d.ts", "next.config.ts"];

function shouldProcessFile(filePath) {
  const ext = path.extname(filePath);
  const fileName = path.basename(filePath);
  return EXTENSIONS.includes(ext) && !SKIP_FILES.includes(fileName);
}

function shouldSkipDirectory(dirName, fullPath, rootPath = process.cwd()) {
  // Check if directory name starts with dot
  if (dirName.startsWith(".")) {
    return true;
  }

  // Get relative path from project root
  const relativePath = path.relative(rootPath, fullPath).replace(/\\/g, "/");

  // Check against skip directories (exact path matching)
  return SKIP_DIRS.some((skipDir) => {
    const normalizedSkipDir = skipDir.replace(/\\/g, "/");

    // Exact match for the relative path
    if (relativePath === normalizedSkipDir) {
      return true;
    }

    // Check if the current path is within a skip directory
    if (relativePath.startsWith(normalizedSkipDir + "/")) {
      return true;
    }

    return false;
  });
}

function hasLicenseHeader(content) {
  return (
    content.includes("SPDX-License-Identifier") ||
    content.includes("Copyright (C)") ||
    content.includes("GNU Affero General Public License")
  );
}

function addLicenseHeader(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf8");

    if (hasLicenseHeader(content)) {
      console.log(`✓ ${filePath} (already has license header)`);
      return { skipped: true, modified: false };
    }

    const newContent = LICENSE_HEADER + content;
    fs.writeFileSync(filePath, newContent, "utf8");
    console.log(`+ ${filePath}`);
    return { skipped: false, modified: true };
  } catch (error) {
    console.error(`✗ Error processing ${filePath}:`, error.message);
    return { skipped: false, modified: false, error: true };
  }
}

function removeLicenseHeader(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf8");

    if (!hasLicenseHeader(content)) {
      console.log(`✓ ${filePath} (no license header found)`);
      return { skipped: true, modified: false };
    }

    let newContent = content;

    // Remove /* ... */ block at the beginning
    const blockCommentRegex = /^\/\*[\s\S]*?\*\/\s*/;
    if (blockCommentRegex.test(content)) {
      const match = content.match(blockCommentRegex);
      if (
        match &&
        (match[0].includes("Copyright (C)") ||
          match[0].includes("SPDX-License-Identifier") ||
          match[0].includes("Japanese Kana Flashcard App") ||
          match[0].includes("GNU Affero General Public License"))
      ) {
        newContent = content.replace(blockCommentRegex, "");
      }
    }

    // Only write if content actually changed
    if (newContent !== content) {
      newContent = newContent.replace(/^\s*\n+/, "");
      fs.writeFileSync(filePath, newContent, "utf8");
      console.log(`- ${filePath}`);
      return { skipped: false, modified: true };
    }

    return { skipped: true, modified: false };
  } catch (error) {
    console.error(`✗ Error processing ${filePath}:`, error.message);
    return { skipped: false, modified: false, error: true };
  }
}

function checkLicenseHeaders(filePath) {
  try {
    const content = fs.readFileSync(filePath, "utf8");
    const hasHeader = hasLicenseHeader(content);

    if (hasHeader) {
      console.log(`✓ ${filePath}`);
    } else {
      console.log(`✗ ${filePath}`);
    }

    return { hasHeader };
  } catch (error) {
    console.error(`✗ Error reading ${filePath}:`, error.message);
    return { hasHeader: false, error: true };
  }
}

function processDirectory(dirPath, operation, rootPath = process.cwd()) {
  const items = fs.readdirSync(dirPath);
  const stats = {
    processed: 0,
    modified: 0,
    skipped: 0,
    errors: 0,
    withHeaders: 0,
    withoutHeaders: 0,
  };

  for (const item of items) {
    const itemPath = path.join(dirPath, item);

    try {
      const stat = fs.statSync(itemPath);

      if (stat.isDirectory()) {
        if (!shouldSkipDirectory(item, itemPath, rootPath)) {
          const subStats = processDirectory(itemPath, operation, rootPath);
          stats.processed += subStats.processed;
          stats.modified += subStats.modified;
          stats.skipped += subStats.skipped;
          stats.errors += subStats.errors;
          stats.withHeaders += subStats.withHeaders;
          stats.withoutHeaders += subStats.withoutHeaders;
        } else {
          // Optional: log skipped directories for debugging
          const relativePath = path.relative(rootPath, itemPath);
          console.log(`⏭️ Skipping directory: ${relativePath}`);
        }
      } else if (stat.isFile() && shouldProcessFile(itemPath)) {
        stats.processed++;

        let result;
        if (operation === "add") {
          result = addLicenseHeader(itemPath);
        } else if (operation === "remove") {
          result = removeLicenseHeader(itemPath);
        } else if (operation === "check") {
          result = checkLicenseHeaders(itemPath);
          if (result.hasHeader) stats.withHeaders++;
          else stats.withoutHeaders++;
        }

        if (result.modified) stats.modified++;
        if (result.skipped) stats.skipped++;
        if (result.error) stats.errors++;
      }
    } catch (error) {
      console.error(`✗ Error accessing ${itemPath}:`, error.message);
      stats.errors++;
    }
  }

  return stats;
}

function printUsage() {
  console.log("Usage: node scripts/manage-license-headers.js [command]");
  console.log("");
  console.log("Commands:");
  console.log("  add     - Add license headers to files that don't have them");
  console.log("  remove  - Remove license headers from all files");
  console.log("  check   - Check which files have/don't have license headers");
  console.log("");
  console.log("Examples:");
  console.log("  node scripts/manage-license-headers.js add");
  console.log("  node scripts/manage-license-headers.js remove");
  console.log("  node scripts/manage-license-headers.js check");
}

function confirmAction(operation, callback) {
  if (operation === "check") {
    callback(true);
    return;
  }

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const messages = {
    add: "This will add license headers to files that don't have them.",
    remove:
      "⚠️  WARNING: This will remove license headers from ALL source files!\nThis action cannot be undone unless you have a backup.",
  };

  console.log(messages[operation]);
  console.log("");

  rl.question("Are you sure you want to continue? (yes/no): ", (answer) => {
    const confirmed =
      answer.toLowerCase() === "yes" || answer.toLowerCase() === "y";
    rl.close();
    callback(confirmed);
  });
}

// Main execution
const operation = process.argv[2];

if (!operation || !["add", "remove", "check"].includes(operation)) {
  printUsage();
  process.exit(1);
}

confirmAction(operation, (confirmed) => {
  if (!confirmed) {
    console.log("Operation cancelled.");
    process.exit(0);
  }

  console.log(
    `${operation === "add" ? "Adding" : operation === "remove" ? "Removing" : "Checking"} license headers...`,
  );
  console.log("");

  const stats = processDirectory(".", operation);

  console.log("");
  console.log("Summary:");
  console.log(`Files processed: ${stats.processed}`);

  if (operation === "check") {
    console.log(`With headers: ${stats.withHeaders}`);
    console.log(`Without headers: ${stats.withoutHeaders}`);
  } else {
    console.log(`Modified: ${stats.modified}`);
    console.log(`Skipped: ${stats.skipped}`);
  }

  if (stats.errors > 0) {
    console.log(`Errors: ${stats.errors}`);
  }

  console.log("Done!");
});
