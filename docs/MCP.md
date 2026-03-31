# MCP Server Conventions

This workspace supports [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) servers for extending agent capabilities. MCP configs live in `.cursor/mcp/`.

## Directory Structure

```
.cursor/mcp/
  mcp_servers.json     # Server declarations (Cursor 2.6+ format)
```

## Server Declaration Schema

Each MCP server entry in `mcp_servers.json` should follow this structure:

```json
{
  "servers": {
    "my-server": {
      "command": "npx",
      "args": ["-y", "@my-org/mcp-server"],
      "env": {
        "API_KEY": "${env:MY_SERVER_API_KEY}"
      }
    }
  }
}
```

## Capability Allow-Listing

Tools in `manifest.json` can declare `requiresApproval` — an array of capability names that should require manual user confirmation per invocation:

| Capability | Risk Level | Description |
|------------|------------|-------------|
| `shell` | High | Executes arbitrary shell commands |
| `file:write` | Medium | Writes files outside the workspace |
| `network` | Medium | Makes outbound HTTP/WebSocket calls |
| `secrets` | High | Accesses credentials or secret stores |

Register high-risk MCP tools in manual-confirm mode. Cursor supports this via the MCP settings panel.

## Adding an MCP Server

1. Install or clone the MCP server package.
2. Add an entry to `.cursor/mcp/mcp_servers.json`.
3. If the server requires credentials, add the env var name to `.env.example` (never the actual value).
4. Add a `requiresApproval` array to the corresponding manifest entry if applicable.
5. Restart Cursor to detect the new server.

## Security Considerations

- MCP servers run with the same permissions as Cursor. A compromised server can read files, execute commands, and exfiltrate data.
- Always pin MCP server packages to specific versions.
- Use `.devcontainer/devcontainer.no-net.json` for air-gapped operation when testing untrusted servers.
- `SECURITY-LOCK.json` does NOT cover MCP server integrity — it only tracks `manifest.json` tools. MCP server verification is a manual step.
- For full isolation, run untrusted MCP servers inside a container with restricted network access.
