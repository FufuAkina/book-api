# 📚 BookAPI - 图书管理系统

基于FastAPI的RESTful图书管理API学习项目

## 🎯 项目目标

通过构建这个项目来学习：
- Python 核心语法（类、装饰器、生成器、上下文管理器）
- FastAPI 核心概念（路由、Pydantic、依赖注入、async）
- Git 工作流（branch、merge、PR）
- pytest 测试框架（fixture、parametrize）

## ✨ 功能特性

- [ ] 图书 CRUD 操作（增删改查）
- [ ] 数据验证（Pydantic）
- [ ] PostgreSQL 数据库存储
- [ ] pytest 单元测试（覆盖率 >80%）
- [ ] Docker 容器化部署
- [ ] API 自动文档

## 🚀 快速开始

### 环境要求
- Python 3.11+
- PostgreSQL 15+
- Docker Desktop

### 安装步骤（Windows）

1. **克隆项目**
   ```bash
   git clone <你的仓库地址>
   cd book-api
创建虚拟环境


python -m venv venv
venv\Scripts\activate
安装依赖


pip install -r requirements.txt
配置环境变量


copy .env.example .env
# 编辑 .env 文件，修改数据库配置
启动数据库


docker-compose up -d
运行应用


uvicorn app.main:app --reload
访问 API 文档

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
🧪 运行测试

# 运行所有测试
pytest

# 查看覆盖率
pytest --cov=app --cov-report=html

# 打开覆盖率报告（Windows）
start htmlcov/index.html
🛠️ 技术栈
Web 框架: FastAPI 0.104+
数据库: PostgreSQL 15
ORM: SQLAlchemy 2.0
数据验证: Pydantic 2.5
测试: pytest 7.4
容器化: Docker & Docker Compose
📁 项目结构

book-api/
├── app/                # 应用代码
│   ├── main.py         # FastAPI 应用入口
│   ├── database.py     # 数据库配置
│   ├── models.py       # SQLAlchemy 模型
│   ├── schemas.py      # Pydantic 模型
│   ├── crud.py         # 数据库操作
│   └── config.py       # 配置管理
├── tests/              # 测试代码
│   ├── conftest.py     # pytest 配置
│   └── test_books.py   # 测试用例
├── docs/               # 文档
├── .env                # 环境变量（不提交）
├── .env.example        # 环境变量模板
├── requirements.txt    # Python 依赖
├── pytest.ini          # pytest 配置
└── docker-compose.yml  # Docker 配置

📚 学习资源
项目开发过程中的学习笔记和资源整理在 docs/ 目录下。

## 🔄 开发进度
✅ 阶段0: 项目初始化
✅ 阶段1: 基础路由
⏳ 阶段2: Pydantic 模型
⏳ 阶段3: 数据库集成
⏳ 阶段4: 单元测试
⏳ 阶段5: Docker 部署
⏳ 阶段6: 文档完善

📝 Git 工作流
从 dev 创建功能分支


git checkout dev
git checkout -b feature/xxx
开发并提交


git add .
git commit -m "feat: 添加xxx功能"
推送到远程


git push origin feature/xxx
在 GitHub 创建 Pull Request，合并到 dev