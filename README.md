# 🚀 VinUni AI in Action (AI-20K) — Engineering Journey

<div align="center">

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Container-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com/)
[![Langfuse](https://img.shields.io/badge/Langfuse-LLMOps-black.svg?logo=langfuse&logoColor=white)](https://langfuse.com/)
[![RAGAS](https://img.shields.io/badge/RAGAS-AI%20Evaluation-orange.svg)](https://ragas.io/)
[![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-purple.svg)](https://modelcontextprotocol.io/)

**Chương trình Đào tạo Kỹ sư AI Thực chiến — VinUni AI-20K Initiative (Khóa 4 - Lớp 3A)**  
*Tác giả:* **Nguyễn Đức Phát** ([@DucPh4t](https://github.com/DucPh4t))

</div>

---

## 📖 Giới thiệu (Overview)

Kho lưu trữ này tổng hợp toàn bộ các dự án thực hành, hệ thống AI Agent, RAG Pipeline, Hạ tầng LLMOps và Đánh giá AI (Evaluation) được xây dựng xuyên suốt chương trình **AI in Action (AI-20K)** tại VinUniversity.

Dự án được cấu trúc theo từng ngày học (Day 01 đến Day 14) với độ phức tạp tăng dần: từ việc làm chủ API mô hình ngôn ngữ lớn (LLMs), xây dựng ReAct & Multi-Agent systems, tối ưu hóa RAG, bảo mật Guardrails, triển khai Cloud/Docker, giám sát với Langfuse cho đến thiết lập pipeline Benchmarking đạt chuẩn công nghiệp.

---

## 🗺️ Lộ trình & Danh mục các bài Lab (Curriculum Roadmap)

| Ngày | Dự án / Thư mục | Trọng tâm công nghệ & Kiến trúc |
| :---: | :---| :---|
| **Day 01** | [`Day01-AI-LLM-Foundation`](./Day01-AI-LLM-Foundation) | Khám phá LLM APIs, System Prompts, Tokenizer & Streaming. |
| **Day 02** | [`Day02-AI-Product-Scoping`](./Day02-AI-Product-Scoping) | Định vị bài toán AI, AI Canvas, UX Patterns & Prototyping. |
| **Day 03** | [`Day03-Chatbot-ReAct-Agent`](./Day03-Chatbot-ReAct-Agent) | ReAct Agent Pattern, Tool Calling, Function Calling & MCP. |
| **Day 04** | [`Day04-IT-Helpdesk-Agent`](./Day04-IT-Helpdesk-Agent) | Autonomous Agent giải quyết sự cố CNTT với LangChain. |
| **Day 05–06** | [`Day05-06-LearnLoop-AI-Hackathon`](./Day05-06-LearnLoop-AI-Hackathon) | **Mini Hackathon AI Product:** Sản phẩm LearnLoop hoàn chỉnh. |
| **Day 07** | [`Day07-Data-Embedding-VectorStore`](./Day07-Data-Embedding-VectorStore) | Chunking strategies, Embedding models & ChromaDB Vector Store. |
| **Day 08** | [`Day08-RAG-Pipeline`](./Day08-RAG-Pipeline) | Hệ thống RAG đa tầng: Hybrid Retrieval, Citations & Chat Interface. |
| **Day 09** | [`Day09-MultiAgent-MCP-A2A`](./Day09-MultiAgent-MCP-A2A) | Hệ thống Multi-Agent điều tra khiếu nại, MCP Evidence Gateway & A2A. |
| **Day 10** | [`Day10-DataPipeline-Observability`](./Day10-DataPipeline-Observability) | ETL Data Pipeline, Data Quality Gates & Data Observability cho RAG. |
| **Day 11** | [`Day11-Guardrails-HITL-ResponsibleAI`](./Day11-Guardrails-HITL-ResponsibleAI) | Bảo mật Agent: Input/Output Guardrails, Red-teaming & Human-in-the-Loop. |
| **Day 12** | [`Day12-Cloud-Services-Deployment`](./Day12-Cloud-Services-Deployment) | Đóng gói Docker, xây dựng API FastAPI và triển khai hạ tầng Cloud. |
| **Day 13** | [`Day13-Monitoring-LLMOps`](./Day13-Monitoring-LLMOps) | Giám sát toàn diện: Distributed Tracing Langfuse, SLOs, Metrics & Alerts. |
| **Day 14** | [`Day14-AI-Evaluation-Benchmark`](./Day14-AI-Evaluation-Benchmark) | Pipeline kiểm thử tự động: RAGAS Metrics, LLM-as-a-Judge, Golden Dataset & CI/CD Gate. |
| **Day 16** | [`Day16-Advance-Agentic-Arena`](./Day16-Advance-Agentic-Arena) | **Phase 2 — Agent Arena:** 5 lớp Middleware bảo vệ Agent ReAct (Critic, Citation, Injection, Budget, Retry). |

---

## 🛠️ Công nghệ & Frameworks sử dụng (Tech Stack)

- **AI & Agent Frameworks:** OpenAI API, DeepSeek API, Anthropic, LangChain, ReAct Pattern, Model Context Protocol (MCP).
- **RAG & Vector Search:** ChromaDB, Dense Embeddings, BM25 / Hybrid Retrieval, Reranking, Cross-Encoder.
- **Backend & Cloud:** Python 3.11+, FastAPI, Pydantic v2, Uvicorn, Docker, Docker Compose, Cloud Services.
- **LLMOps & Monitoring:** Langfuse (Tracing, Session, Generations), Prometheus metrics, Structured JSON Logging, SLO tracking.
- **Evaluation & Guardrails:** RAGAS (Faithfulness, Answer Relevance, Context Recall, Context Precision AP@K), LLM-as-a-Judge, NeMo Guardrails principles, PII Masking, Red-teaming.

---

## ⚡ Hướng dẫn cài đặt & Chạy thử (Getting Started)

Mỗi thư mục `DayXX-...` là một module độc lập có đầy đủ hướng dẫn, file mã nguồn và bài tập tương ứng:

```bash
# 1. Clone repository
git clone https://github.com/DucPh4t/AI-IN-ACTION-20K.git
cd AI-IN-ACTION-20K

# 2. Di chuyển vào thư mục bài học muốn trải nghiệm (ví dụ Day 14)
cd Day14-AI-Evaluation-Benchmark

# 3. Tạo môi trường ảo và cài đặt dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 4. Thiết lập biến môi trường (nếu cần)
cp .env.example .env
```

---

## 👤 Tác giả

- **Nguyễn Đức Phát**
- Sinh viên Khóa 4 — Lớp 3A, VinUniversity AI-20K Program
- GitHub: [@DucPh4t](https://github.com/DucPh4t)

---

⭐ *Nếu bạn thấy dự án này hữu ích cho việc tự học và tham khảo AI Engineering, hãy tặng repo một Star nhé!*
