# Agno

## Overview

### Features

Some features of the Agno agent framework are:

- **AgentOS**: FastAPI application that can be self-hosted
- **AgentOS UI**: UI that connects to AgentOS. Hosted by Agno.
- **AgentOS UI self-hosted**: [Self-hosted NextJS app](https://github.com/agno-agi/agent-ui). Is dependant on AgentOS.
- **Evals**: Built-in evals. Async support but not in AgentOS API endpoint

## Notes

### Evaluation through Agno

- AgentOS UI requires AgentOS, since eval does not support async tools, I will not further investigate AgentOS/AgentOS UI

### TODO:

- [ ] Implement tool calls
- [ ] Add evals
- [ ] How to observability?
- [ ] Is it possible to add own routes to AgentOS?

# Braintrust
