# MCP: Model Context Protocol

MCP stands for **Model Context Protocol**. It is an open standard that gives compatible AI applications a consistent way to connect to external tools, data sources, and services.

An AI model does not automatically have access to your GitHub repositories, computer files, databases, or other applications. To work with those systems, an AI application needs integrations with the right capabilities and permissions.

**MCP standardizes one way for AI applications to communicate with those integrations.**

For example, an AI assistant connected to a suitable GitHub MCP server might be able to search repositories, read files, inspect issues, or create an issue, provided the server exposes those tools and the connection has the necessary permission.

MCP is not an AI model, a database, or an automatic grant of access. It is a protocol that compatible applications and servers use to communicate.

## 1. Understand MCP with a Real-World Analogy

Imagine that you own several electronic devices: a keyboard, a mouse, a camera, and a storage drive. If every device used a completely different connection method, connecting and supporting them would be difficult. A shared standard makes compatible connections easier to build.

MCP plays a similar role for AI applications. It gives compatible applications and services a common protocol for discovering and using supported capabilities.

The analogy is not exact: MCP is a software protocol, not a physical connector. Each integration still needs to be implemented, configured, and authorized.

## 2. What Problem Does MCP Solve?

Suppose you want an AI assistant to work with GitHub, local documents, and a database. Each service may have its own API, data formats, authentication methods, and supported actions.

Without a common integration protocol, developers may need to build and maintain many application-specific integrations. MCP offers shared rules that compatible AI applications and MCP servers can implement.

An MCP server can act as an adapter: it exposes selected capabilities through MCP and may call an existing API, access approved files, or query another system behind the scenes.

MCP can reduce duplicated integration work, but it does not eliminate the need to implement and maintain servers, configure access, or understand the connected service.

## 3. The Three Main Parts of MCP

To understand MCP, learn these three terms: **host, client, and server**.

### 3.1 MCP Host

The **host** is the AI application you interact with. It manages the user experience and the connections to MCP servers.

Examples include compatible AI assistants, desktop AI applications, and AI coding environments.

The host controls how connections are configured and how information returned by MCP servers is made available to the model.

### 3.2 MCP Client

The **client** is the component inside the host that communicates with a particular MCP server using the MCP protocol.

A host can manage multiple MCP clients, typically with each client maintaining a connection to a server.

### 3.3 MCP Server

The **server** is a program that exposes capabilities to an MCP client. These capabilities may include tools, resources, and prompts.

An MCP server might connect to GitHub, a local folder, a database, a documentation source, or another service. It can run locally on your computer or remotely.

### Architecture at a Glance

```text
You
 |
 v
AI application (MCP host)
 |
 | manages
 v
MCP client
 |
 | communicates using MCP
 v
MCP server
 |
 | may use
 v
GitHub API, files, database, or another service
```

This diagram shows a common arrangement. The exact internal design depends on the host, server, and connected service.

## 4. How Does MCP Work in Practice?

Imagine your AI application is connected to a GitHub MCP server. You ask:

> Summarize the recent changes in my repository and suggest what I should work on next.

A simplified interaction might look like this:

1. **You submit a request.** The AI application receives your question.
2. **The AI identifies the information it needs.** It may determine that repository details and recent changes are necessary.
3. **The host makes MCP capabilities available to the model.** The model can select an appropriate tool when needed.
4. **The MCP client sends a tool request.** It communicates with the connected MCP server using the protocol.
5. **The MCP server performs the operation.** It might call a GitHub API or another configured integration to retrieve permitted information.
6. **The result returns to the AI application.** The model uses the result to produce a summary or decide what information it still needs.
7. **Another action may be requested.** For example, the assistant could offer to create an issue, subject to tool availability, permissions, and suitable confirmation.

The MCP server does not make the AI intelligent by itself. The model and host determine how to use the information and capabilities that the integration makes available.

**Important:** Mentioning GitHub in a chat does not automatically grant GitHub access. A suitable server must be connected, configured, and authorized.

## 5. What Can an MCP Server Provide?

MCP defines three important server capabilities: **tools, resources, and prompts**. Not every server needs to offer all three.

### 5.1 Tools — Perform Actions

Tools are operations that an AI application can discover and ask the server to execute.

Examples:
- Search GitHub issues.
- Read a permitted file.
- Run an approved database query.
- Create a ticket.
- Retrieve information from an external service.

Think of a tool as a function made available through the MCP server. A tool has a name, a description, and a defined input schema. The server processes a valid tool request and returns a result.

A tool may read information or change something. Write operations deserve extra care because they can have real-world consequences.

### 5.2 Resources — Provide Context

Resources represent data that an MCP server can make available to a client or host.

Examples:
- Documentation.
- File contents.
- Database schemas.
- Other readable information.

Think of resources as context that can help an AI application understand a task. How resources are discovered and selected depends on the host and server implementation.

### 5.3 Prompts — Reusable Task Templates

Prompts are reusable templates that an MCP server can provide to help structure a task.

Examples:
- A template for reviewing code.
- A template for investigating a bug.
- A template for analyzing a dataset.

Think of prompts as predefined ways to guide a task. The host decides how to present and use them.

### Quick Comparison

| Capability | Main purpose | Example |
|---|---|---|
| Tools | Request an operation | Search for open GitHub issues |
| Resources | Provide information or context | Read a documentation resource |
| Prompts | Provide reusable task instructions | Start a structured code review |

An MCP server may expose a combination of these capabilities, depending on its purpose.

## 6. How Do We Use MCP?

There are two common approaches:

1. **Connect to an existing MCP server.**
2. **Build your own MCP server.**

You do not need to create a server to start learning MCP. Connecting to an existing, trusted server is usually the easiest first step.

## 7. Approach A: Use an Existing MCP Server

Follow this general process. The exact steps differ between AI applications and MCP servers.

1. **Choose an MCP-compatible AI application.** Confirm that the application supports MCP connections.
2. **Choose a server for your goal.** For example, you may need a GitHub integration, a filesystem server, or a database server.
3. **Read the server's documentation.** Check its source, prerequisites, supported operations, permissions, and security considerations.
4. **Install or configure the server.** A local server may require a runtime such as Node.js or Python. A remote server may instead require a URL and authentication.
5. **Connect it to the AI application.** Add the server through the host's supported configuration method.
6. **Set up authentication and permissions.** Provide only the access that is required.
7. **Test with a small, safe request.** Start with a read-only operation before enabling write operations.
8. **Review access periodically.** Disconnect the server when it is no longer needed.

Installing a server does not automatically make it available in every AI application. The host must support MCP and be configured to connect to that server.

### Example: Connecting an AI Assistant to GitHub

Suppose you want an assistant to inspect your repositories.

- Select a GitHub MCP server from a source you trust.
- Follow its current setup instructions.
- Authenticate using the supported method.
- Grant access only to the repositories and operations it needs.
- Connect the server to an MCP-compatible host.
- Ask it to perform a harmless read-only task, such as summarizing a repository file.
- Verify the results against GitHub.

If you later enable operations that create issues, edit files, or change repositories, understand the permissions and confirmation behavior first.

Useful official starting points:

- [Official MCP documentation](https://modelcontextprotocol.io/)
- [MCP reference servers repository](https://github.com/modelcontextprotocol/servers)
- [MCP quickstart resources](https://github.com/modelcontextprotocol/quickstart-resources)

These links are starting points, not a guarantee that every example is suitable for every production environment. Review the current documentation for a server before installing it.

## 8. Approach B: Build Your Own MCP Server

Building a server becomes useful when you want an AI assistant to access a custom application, internal workflow, or personal knowledge base.

Imagine building an assistant for your Engineering OS repository. You might expose tools like these:

| Example tool | Purpose |
|---|---|
| `search_notes` | Search permitted learning notes |
| `get_concept` | Retrieve a concept document |
| `list_recent_builds` | List recent experiments |
| `add_question` | Save a question for later revision |

These are example tool names. You would need to implement them in your server.

A high-level development process is:

1. **Choose a programming language and MCP SDK.** Official SDKs are available for several languages, including Python and TypeScript.
2. **Create an MCP server.** Use an SDK to implement the protocol rather than inventing a custom message format.
3. **Define capabilities.** Specify the tools, resources, and prompts the server should expose.
4. **Implement the operations.** For example, make `search_notes` search only directories the server is allowed to access.
5. **Validate input.** Check parameters, handle errors, and avoid assuming that model-generated arguments are safe.
6. **Configure permissions.** Grant access only to the required files, repositories, or services.
7. **Connect the server to a compatible host.** Follow the host's current configuration instructions.
8. **Test and monitor it.** Verify valid inputs, invalid inputs, failures, permissions, and write operations.

You can explore official SDKs and guides through the [MCP documentation](https://modelcontextprotocol.io/) and the [MCP GitHub organization](https://github.com/modelcontextprotocol).

### Example: An Engineering OS MCP Server

An MCP server for a learning repository could expose tools such as `search_notes` and `get_concept`.

A possible workflow would be:

```text
You ask: "What did I learn about APIs?"
                 |
                 v
The AI selects search_notes
                 |
                 v
MCP client sends a request
                 |
                 v
Your MCP server searches approved notes
                 |
                 v
Relevant passages are returned
                 |
                 v
The AI explains the findings and links to notes
```

To save new information, a separate write tool could draft or create a Markdown file. Because writing changes your repository, add suitable validation and, where appropriate, require your approval before committing changes.

## 9. How Does MCP Relate to APIs, HTTP, and HTTPS?

These concepts work together, but they are not interchangeable.

| Concept | What it is | Main role |
|---|---|---|
| API | An interface and set of rules | Defines how software functionality or data can be accessed |
| HTTP | A communication protocol | Defines how web requests and responses are exchanged |
| HTTPS | HTTP protected by TLS | Protects web communication in transit |
| MCP | A protocol for AI-to-server integrations | Standardizes how compatible AI applications communicate with MCP servers and use their exposed capabilities |

### Example: GitHub API and GitHub MCP Server

GitHub provides APIs that developers can use to access supported repository functionality.

A GitHub MCP server can use one of those APIs behind the scenes and expose selected operations through MCP. An MCP-compatible AI host can then discover and invoke those operations through its MCP client.

The relationship looks like this:

```text
AI application
      |
      v
MCP client
      |
      | MCP protocol
      v
GitHub MCP server
      |
      | GitHub API request
      v
GitHub service
      |
      | Result
      v
GitHub MCP server
      |
      | MCP tool result
      v
AI application
```

MCP does not replace the underlying GitHub API. It provides a standardized way for a compatible AI application to interact with the integration that exposes selected GitHub operations.

MCP supports different transports. Local servers commonly communicate over standard input/output (stdio). Remote MCP servers can use Streamable HTTP. HTTPS may be used to secure remote communication, depending on deployment.

The important distinction is that MCP defines more than an HTTP URL: it defines protocol behavior for discovering capabilities and exchanging structured messages between clients and servers.

## 10. What Is MCP Useful For?

MCP is useful when an AI application needs controlled access to information or actions outside the conversation.

### AI Coding Assistants

Connect an assistant to repository information, project files, issue trackers, documentation, and supported developer tools.

### Document and Knowledge Assistants

Let an AI application search approved documents and retrieve relevant information instead of relying only on what was provided in the current conversation.

### Data and Operations

Connect an AI workflow to permitted database queries, monitoring information, or operational tools.

### AI Agents and Multistep Workflows

Provide a model with the tools it needs to complete a multistep task. The model can request tools as it works, while the host and server manage connections and enforce configured permissions.

### Personal Learning Systems

An MCP server for a learning archive could help an AI application:
- Search existing notes before drafting a new one.
- Retrieve a concept document while answering a question.
- Identify topics that have not yet been documented.
- Draft a new Markdown note.
- Save a question for later revision, with appropriate approval for write operations.

MCP enables the connection; it does not guarantee that the AI's reasoning or output will be correct. Results still need to be checked.

## 11. Is MCP Safe?

MCP is a protocol, not a guarantee that every server or integration is secure.

An MCP server may be able to read files, access private repositories, query databases, or perform write operations. A poorly designed or malicious server could misuse those permissions.

Follow these safety principles:

- **Use trusted sources.** Review the server's source, documentation, maintainer, and permissions before installing it.
- **Apply least privilege.** Give the server only the access needed for its task.
- **Protect credentials.** Do not commit API keys, passwords, access tokens, or private configuration secrets to a public repository.
- **Validate inputs.** Treat tool arguments as untrusted and validate them before taking action.
- **Treat returned content as untrusted.** A file or webpage could contain malicious instructions. Retrieved content should not automatically override the host's policies or your instructions.
- **Require approval for consequential actions.** Deleting files, editing repositories, sending messages, or making purchases can have real effects.
- **Be careful with filesystem access.** Restrict which directories a local server can read or write.
- **Understand authentication.** Know which account is connected, which credentials are used, and what permissions the server receives.
- **Review remote connections.** Use appropriate transport security and authentication when connecting to a remote server.

For production implementations, consult the security guidance in the [official MCP documentation](https://modelcontextprotocol.io/). Do not assume an installation is safe merely because it uses MCP.

## 12. Common Misconceptions

### "MCP is an AI model."

No. MCP is a protocol used by AI applications and MCP servers to communicate.

### "MCP automatically gives AI access to my computer."

No. Access depends on which servers are connected, what they expose, how they are configured, and which permissions have been granted.

### "MCP replaces APIs."

No. An MCP server can use an existing API behind the scenes and expose selected operations through MCP.

### "Every MCP server has every capability."

No. Each server exposes the tools, resources, and prompts that its developer implements.

### "I must build my own MCP server to use MCP."

No. You can connect an existing server to a compatible AI application.

### "MCP makes an AI agent automatically reliable."

No. MCP provides access to capabilities. The AI may still choose the wrong tool, misunderstand a result, or generate an incorrect answer.

### "An MCP server can only run in the cloud."

No. MCP servers can run locally or remotely. The connection method depends on the implementation and configuration.

## 13. Questions for Revision

Try answering these questions before reading the answer key.

1. What does MCP stand for?
2. What problem does MCP solve?
3. What is the difference between an MCP host, client, and server?
4. What is an MCP tool?
5. How are resources different from tools?
6. What are MCP prompts used for?
7. Does every MCP server expose all three capabilities?
8. How could an MCP server access GitHub functionality?
9. Does MCP replace the GitHub API?
10. What is the difference between MCP and HTTP/HTTPS?
11. What is the difference between a local MCP server and a remote MCP server?
12. What should you check before installing a server?
13. Why should an MCP server be given only the minimum permissions it needs?
14. Why should tool inputs and retrieved documents be treated as potentially untrusted?
15. How could MCP help your Engineering OS repository?
16. Do you need to build a server before using an existing MCP integration?

### Answer Key

1. **Model Context Protocol.**
2. It provides a common protocol for compatible AI applications to connect to external tools, data, and services.
3. The host is the AI application; the client is the component that communicates with a server; the server exposes capabilities.
4. A tool is an operation that an AI application can request an MCP server to execute.
5. Resources provide information or context; tools let the application request operations.
6. Prompts provide reusable templates for structuring tasks.
7. No. A server implements whichever capabilities it needs.
8. It could call the GitHub API or another integration behind the scenes and expose selected operations through MCP.
9. No. MCP standardizes interaction between the AI application and the MCP server; the server may use the GitHub API.
10. HTTP/HTTPS are web communication protocols; MCP defines protocol behavior for AI applications to interact with MCP servers. MCP may use stdio locally or Streamable HTTP remotely.
11. A local server runs in a local environment and commonly communicates over stdio; a remote server runs on an accessible remote service and can use a network transport.
12. Check the source, documentation, maintainer, permissions, prerequisites, authentication, and security implications.
13. Least privilege limits damage if the server is compromised or misused.
14. Tool inputs can be malformed or unsafe, and retrieved content can contain malicious instructions. Both require validation and appropriate handling.
15. It could expose safe search and retrieval tools for notes and concepts and, with suitable controls, help draft or save new learning documents.
16. No. You can start by connecting an existing MCP server to a compatible host.

## 14. What to Learn Next

A practical learning sequence is:

1. **APIs** — understand software interfaces.
2. **HTTP and HTTPS** — understand web requests, responses, and transport security.
3. **JSON** — understand structured data commonly used in API messages.
4. **MCP architecture** — learn hosts, clients, servers, and capabilities.
5. **Connect an existing MCP server** — start with a read-only use case.
6. **Build a small MCP server** — expose one or two clearly defined tools.
7. **Authentication and permissions** — control which systems and actions the server can access.
8. **AI tool use and agent workflows** — understand how a model selects tools and works with their results.
9. **Security and evaluation** — validate inputs, review side effects, and test the complete workflow.

Useful official resources:

- [MCP documentation](https://modelcontextprotocol.io/)
- [Reference servers](https://github.com/modelcontextprotocol/servers)
- [Quickstart resources](https://github.com/modelcontextprotocol/quickstart-resources)

## Key Takeaway

> **MCP (Model Context Protocol) is an open standard that lets compatible AI applications connect to external tools, information, and services through a common protocol.**

Remember this flow:

**AI application → MCP client → MCP server → External service or data → Result returned to the AI application.**

MCP provides the connection mechanism. The AI application uses the returned context to answer questions or request further actions, while the host and server enforce the configured capabilities and permissions.
