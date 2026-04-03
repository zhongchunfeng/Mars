---
trigger: always_on
alwaysApply: true
---

## **运维与基础设施规范 (Ops & Infrastructure)**

- **幂等性 (Idempotency)**: 所有的基础设施脚本（Shell, Ansible, Terraform）必须具备幂等性。
- **防御式变更**: 
  - 涉及网络或核心配置变更前，必须输出 `Implementation Plan` 并进行二阶思维风险评估。
  - 脚本必须包含 `set -euo pipefail` 及其错误回滚逻辑。
- **环境隔离**: 区分生产 (Prod) 与测试 (Dev) 配置，确保 Agent 了解当前操作的环境上下文。
- **命令行精准度**: 所有的操作步骤必须提供精确到行、可直接在终端运行的命令，并注明潜在风险。