# Sources for Session 11 (checked 6 November 2026)

Vendor and project sources only. No statistics are taken from them.

| Fact used on a slide | Source | Checked |
|---|---|---|
| MCP is an open-source standard for connecting AI applications to external systems; "Think of MCP like a USB-C port for AI applications" | https://modelcontextprotocol.io/docs/getting-started/intro | 6 Nov 2026 |
| An MCP host (the AI application) creates one MCP client per MCP server; a server is a program that provides context | https://modelcontextprotocol.io/docs/learn/architecture | 6 Nov 2026 |
| Servers expose three core primitives: tools (actions), resources (context data), prompts (reusable templates) | https://modelcontextprotocol.io/docs/learn/architecture | 6 Nov 2026 |
| Clients can expose elicitation: a server can ask the user for input or confirmation of an action | https://modelcontextprotocol.io/docs/learn/architecture | 6 Nov 2026 |
| MCP was announced by Anthropic as an open standard on 25 November 2024 | https://www.anthropic.com/news/model-context-protocol | 6 Nov 2026 |
| Agents are "typically just LLMs using tools based on environmental feedback in a loop"; they get ground truth from tool results at each step; they can pause for human feedback at checkpoints; stopping conditions such as a cap on iterations; test in sandboxed environments with guardrails (post dated 19 December 2024) | https://www.anthropic.com/engineering/building-effective-agents | 6 Nov 2026 |
| Prompt injection is ranked first in the OWASP Top 10 for LLM Applications 2025 | COURSE_BIBLE section 5 (researched 1 Nov 2026); re-check at https://genai.owasp.org the week of teaching | not re-fetched today |

Left out (not verified today): who governs MCP now, adoption numbers, which products support MCP beyond the names on the MCP introduction page. The slides name no product as supporting MCP.
