import { tool } from "@opencode-ai/plugin";
import { execSync } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const scriptsDir = path.resolve(__dirname, "..", "scripts");

export default tool({
  description: "Compare source files against test files to find untested modules",
  args: {
    path: tool.schema.string().optional().describe("Project root directory (defaults to current working directory)"),
  },
  async execute(args, context) {
    const targetPath = args.path || context.directory;
    const script = path.join(scriptsDir, "test-gap.py");
    try {
      const result = execSync(`python "${script}" "${targetPath}"`, { encoding: "utf-8", timeout: 30000 });
      return result;
    } catch (e: any) {
      return `Error: ${e.stderr || e.message}`;
    }
  },
});
