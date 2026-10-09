# Survey of LLM Agents and Tool Use

## TL;DR
- LLM agents have evolved from passive text models into modular, autonomous systems capable of reasoning and interacting with external tools [1][2].
- Modern frameworks integrate brain (LLM), memory, and tool-action modules to handle complex, stateful task execution [1][2][3].
- Evaluation is shifting toward interactive, multi-turn, and state-aware environments that simulate real-world API interactions [4][5].
- Advanced reasoning paradigms like ReAct [6] and multi-agent collaboration [7] are critical for achieving high reliability and performance in tool-centric environments.

## Background
The field of LLM-based agents focuses on transforming large language models into autonomous entities that can perform tasks, use tools, and interact with the environment [2]. Traditional language models were primarily restricted to passive information processing. The integration of "agentic" capabilities allows models to interpret environment cues, maintain a memory of past states, and invoke external APIs or tools to complete multi-step goals [1]. A standard agent framework consists of four primary pillars: the brain (the LLM's core reasoning engine), perception modules, memory systems (for context management), and action modules (tool execution interfaces) [2].

## Core Agentic Architectures
Current architectures emphasize modularity and unified interfaces for tool interaction. Frameworks like AgentForge provide a structure for modular skill composition, enabling developers to plug in new tools without modifying the core model's architecture [1]. This modularity is a direct response to the need for scalable agent systems that can adapt to diverse toolsets and dynamic environmental changes. Central to these systems is the ability to maintain state across multi-turn interactions, ensuring that the model's decision-making reflects the accumulated outcomes of previous tool calls [2].

## Tool-Use Mechanisms and Evaluation
The efficacy of an agent is deeply dependent on its tool-use precision and grounding. Foundational work such as Toolformer demonstrated that language models can autonomously teach themselves when and how to call external APIs [8]. Early approaches relied on static, single-turn prompts, but state-of-the-art research highlights the necessity of stateful, conversational evaluation environments. Benchmarks such as ToolSandbox evaluate how agents handle implicit dependencies between tool results and conversational context [4]. Furthermore, researchers are pushing towards procedural task execution, where agents must adapt to generated states and tool outputs in closed-loop systems [5]. These approaches aim to replace simplistic benchmark datasets with more realistic, sandbox-based evaluations that mirror real-world API complexities.

## Reasoning and Multi-Agent Orchestration
Advanced reasoning and collaboration are essential for handling complex, multi-step tasks. The ReAct framework established the standard for interleaving reasoning traces with tool execution, significantly improving decision accuracy by providing a logical audit trail [6]. Building on this, modern research proposes paradigms such as the Chain-of-Agents (CoA), which leverages multi-agent distillation and agentic reinforcement learning (RL) to coordinate specialized agents for more robust problem-solving [7]. These systems allow for specialized skill sets to be distributed across agents, facilitating the management of large-scale task execution which would be intractable for a single-agent system [3].

## Trends and open problems
- **State management and Reliability:** Despite progress, agents struggle with long-horizon tasks where state persistence is key.
- **Evaluation:** Existing benchmarks often fail to capture real-world API volatility, necessitating more robust, dynamic simulation environments [4][5].
- **Agentic RL:** Optimizing decision sequences through reinforcement learning remains a major, yet compute-intensive, frontier [7].
- **Standardization:** There is an ongoing need for unified protocols (like the Model Context Protocol) to simplify how agents interface with tools at scale [5].

## References
[1] From Language to Action: A Review of Large Language Models as Autonomous Agents and Tool Users. hf-search. https://huggingface.co/papers/2508.17281 (2025-10-28)
[2] A Survey on Large Language Model based Autonomous Agents. hf-search. https://huggingface.co/papers/2308.11432 (2023-08-22)
[3] AgentLite: A Lightweight Library for Building and Advancing Task-Oriented LLM Agent System. hf-search. https://huggingface.co/papers/2402.15538 (2024-02-23)
[4] ToolSandbox: A Stateful, Conversational, Interactive Evaluation Benchmark for LLM Tool Use Capabilities. hf-search. https://huggingface.co/papers/2408.04682 (2024-08-08)
[5] WorldGuide: Goal-Directed Video World Model for Procedural Task Execution. hf-daily. https://huggingface.co/papers/2610.12459 (2026-10-08)
[6] ReAct: Synergizing Reasoning and Acting in Language Models. arxiv. https://arxiv.org/abs/2210.03629 (2022-10-06)
[7] Chain-of-Agents: End-to-End Agent Foundation Models via Multi-Agent Distillation and Agentic RL. hf-search. https://huggingface.co/papers/2508.13167 (2025-08-06)
[8] Toolformer: Language Models Can Teach Themselves to Use Tools. arxiv. https://arxiv.org/abs/2302.04761 (2023-02-09)
