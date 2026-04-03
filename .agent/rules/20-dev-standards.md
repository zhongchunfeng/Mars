---
trigger: always_on
---

---
trigger: always_on
alwaysApply: true
---

## **开发规范与代码质量 (Clean Code Standard)**

- **结构化流程**: 严格遵循 **“构思方案 -> 提请审核 -> 分解为具体任务”** 的作业顺序。
- **设计模式**: 遵循 **SOLID** 原则。函数应单一职责，逻辑深度建议不超过 3 层。
- **现代化语法**: 
  - **Python**: 必须使用 Type Hints，遵循 PEP 8。
  - **TypeScript**: 严禁使用 `any`，优先使用 Interface 定义契约。
- **注释协议**: 每一份非琐碎的代码文件头部必须包含 `Module Header`。复杂算法必须解释 “Why” 而非 “What”。
- **错误处理**: 禁止静默失败。所有 `try-catch` 必须有明确的处理逻辑或上报机制。