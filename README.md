# AI 数据分析一键启动（中文说明）

欢迎使用 ai-data-analysis-3456：一个开源、一键启动的 AI 数据分析堆栈样板，包含 JupyterLab、MLflow（实验跟踪）、Superset（可视化），并提供 Gradio 示范与示例脚本，用于快速搭建“全历记录、走势跟踪、AI 推理”工作流。

仓库地址：https://github.com/US3456H/ai-data-analysis-3456

主要文件说明：
- Dockerfile：构建工作镜像（JupyterLab + MLflow 客户端 + Gradio + 常用数据科学库）
- docker-compose.yml：把 workspace、mlflow、superset 等服务一键启动
- .env.example：示例环境变量
- workspace/train_and_log.py：示例脚本，生成合成时间序列并记录到 MLflow
- gradio_demo.py：简易 Gradio 演示，用来展示如何对模型进行自然语言式交互（示例）

快速开始（推荐在 Linux / macOS / Codespaces / Docker Desktop 环境执行）

1) 克隆仓库（已在你的 GitHub 仓库中）
   git clone https://github.com/US3456H/ai-data-analysis-3456
   cd ai-data-analysis-3456

2) 复制 .env 示例并修改密码（强烈建议修改）
   cp .env.example .env
   # 编辑 .env 替换 DEFAULT_PASSWORD

3) 启动服务（会构建 workspace 镜像并启动 mlflow、superset）
   docker-compose up --build

4) 打开下面的界面：
   - JupyterLab: http://localhost:8888
   - MLflow UI: http://localhost:5000
   - Superset: http://localhost:8088 (首次运行需按 Superset 官方文档初始化用户)

5) 在 JupyterLab 或容器内运行示例脚本
   # 进入容器的 /workspace
   python workspace/train_and_log.py
   # 运行后会把实验记录到 MLflow，MLflow UI 可查看历史记录和模型 artifact。

注意事项：
- AutoGluon 或 H2O 非必要但推荐用于更强的 AutoML 能力；它们体积较大，可能需要大量磁盘和内存。若你希望启用 AutoGluon，请修改 Dockerfile 在构建时安装（README 中有注释），或在本地环境单独安装。
- Superset 第一次启动通常需要初始化 metadata DB 和创建管理员用户，请参考 Superset 官方文档：https://superset.apache.org/
- 本仓库提供的是“示范级”一键启动包；用于生产部署请按照最佳实践修改密码、持久化后端、HTTPS、认证等。

如果你希望我在仓库中同时添加：
- Codespace devcontainer 配置（可以直接打开 Codespaces 运行全部服务），或者
- 更完整的 Notebook 演示（含 AutoGluon / H2O 示例），请回复 "添加 Codespace" 或 "添加 更完整 Notebook"。

下一步我将把示例脚本和 Gradio 演示推送到 workspace 目录，并在这里给出如何在 Jupyter 中运行的具体命令。