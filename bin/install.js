#!/usr/bin/env node
const fs = require("fs");
const path = require("path");

const packageDir = path.resolve(__dirname, "..");
const dirsToCopy = ["agents", "skills", "tools", "scripts"];

function findConfigDir() {
  const home = process.env.HOME || process.env.USERPROFILE;
  const candidates = [
    process.env.OPENCODE_CONFIG_DIR,
    home ? path.join(home, ".config", "opencode") : null,
    process.env.OPENCODE_PROJECT_DIR
      ? path.join(process.env.OPENCODE_PROJECT_DIR, ".opencode")
      : null,
    path.join(process.cwd(), ".opencode"),
  ].filter(Boolean);

  for (const dir of candidates) {
    if (fs.existsSync(dir)) return dir;
  }

  // Fallback: check common OS-specific locations
  if (process.platform === "win32") {
    const appData = process.env.APPDATA;
    if (appData) {
      const p = path.join(appData, "opencode");
      if (fs.existsSync(p)) return p;
    }
  }

  return null;
}

function copyDirs(targetDir) {
  console.log("");
  for (const dir of dirsToCopy) {
    const src = path.join(packageDir, dir);
    const dest = path.join(targetDir, dir);
    if (!fs.existsSync(src)) {
      console.log(`  ✗ ${dir}/  (not found in package)`);
      continue;
    }
    fs.cpSync(src, dest, { recursive: true, force: true });
    console.log(`  ✓ ${dir}/`);
  }
}

function prompt(question) {
  return new Promise((resolve) => {
    process.stdout.write(question);
    process.stdin.once("data", (data) => {
      resolve(data.toString().trim());
    });
  });
}

async function main() {
  console.log("");
  console.log("  censorship-team  v1.0.0");
  console.log("  ─────────────────────────────");
  console.log("");

  let targetDir = findConfigDir();

  if (!targetDir) {
    console.log("  Could not detect opencode config directory automatically.");
    const input = await prompt(
      "  Enter the target path (or press Enter to use current directory): "
    );
    targetDir = input.trim() || process.cwd();
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }
  }

  console.log(`  Target: ${targetDir}\n`);

  // Check if target is a project .opencode/ or global config
  const isGlobal = targetDir.includes(".config") || targetDir.includes("AppData");

  if (!isGlobal) {
    // For project installs, check if .opencode/ is expected
    if (!targetDir.endsWith(".opencode")) {
      const nested = path.join(targetDir, ".opencode");
      if (!fs.existsSync(nested)) {
        const answer = await prompt(
          "  Target is not an opencode directory. Create .opencode/ inside? (Y/n): "
        );
        if (answer.toLowerCase() !== "n") {
          fs.mkdirSync(nested, { recursive: true });
          targetDir = nested;
          console.log(`  Created: ${nested}\n`);
        }
      } else {
        targetDir = nested;
      }
    }
  }

  console.log("  Copying:\n");
  copyDirs(targetDir);

  console.log("\n  ─────────────────────────────");
  console.log("  Done.");
  console.log("");

  if (isGlobal) {
    console.log("  Next steps:");
    console.log("  1. Navigate to your project directory");
    console.log("  2. Start opencode");
    console.log("  3. Run:  @installer configure skill models");
  } else {
    console.log("  Next steps:");
    console.log("  1. Start opencode in this project");
    console.log("  2. Run:  @installer configure skill models");
  }

  console.log("");
  process.exit(0);
}

main().catch((err) => {
  console.error("  Install failed:", err.message);
  process.exit(1);
});
