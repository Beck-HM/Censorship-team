import { tool } from "@opencode-ai/plugin";
import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const scriptsDir = path.resolve(__dirname, "..", "scripts");

export default tool({
  description: "Find source files not imported by any other project file (orphans / dead code)",
  args: {
    path: tool.schema.string().optional().describe("Project root directory (defaults to current working directory)"),
  },
  async execute(args, context) {
    const targetPath = args.path || context.directory;
    const script = path.join(scriptsDir, "find-orphans.py");
    try {
      const result = execSync(`python "${script}" "${targetPath}"`, { encoding: "utf-8", timeout: 30000 });
      return result;
    } catch (e: any) {
      return `Error: ${e.stderr || e.message}`;
    }
  },
});
