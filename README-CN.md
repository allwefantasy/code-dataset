
# 🚀 code_dataset

code_dataset 是一个开源的代码编程数据集项目。与其他编程数据集不同，该数据集来自实际开源项目的编程迭代，使用当前最好的模型以及经过资深研发人员的审核。这确保了数据集的质量和实用性，为研究人员和开发者提供了宝贵的学习资源。

---

## ✨ 特点

- 🌟 数据集来自实际开源项目的编程迭代
- 🤖 使用当前最先进的模型生成
- 👨‍💻 经过资深研发人员审核
- 💎 高质量、实用的代码示例

---

## 📂 数据位置和结构

收集的数据存储在 `data/libs/project_repo` 目录中，每个项目都有自己的子目录。每个项目的数据存储在 `data.jsonl` 文件中。

`data.jsonl` 文件中的每一行代表一个单独的 JSON 对象，结构如下：

```json
{
  "instruction": "任务指令",
  "conversations": [
    {
      "role": "用户或助手",
      "content": "消息内容"
    },
    ...
  ],
  "model": "用于生成的模型",
  "yaml_file": "与此数据相关的 YAML 文件"
}
```

- `instruction`: 任务指令
- `conversations`: 对话消息数组，每条消息包含 `role` 和 `content`
- `model`: 用于生成响应的 AI 模型
- `yaml_file`: 与此数据条目相关的 YAML 文件

---

## 🛠 code-dataset 命令行工具

如果你的项目使用了 [auto-coder.chat](https://auto-coder.chat) ，那么你可以使用 code-dataset 命令行工具来管理本地的编程数据集。
code-dataset 是一个方便的命令行工具，用于收集和管理本地可以提交供外部使用的编程数据集。

### 📥 安装

1. 克隆项目仓库：

```bash
git clone https://github.com/yourusername/code_dataset.git
cd code_dataset
```

2. 安装 code-dataset 工具：

```bash
pip install -e .
```

或者

```bash
pip install code-dataset
```

### 🔧 使用方法

code-dataset 工具提供了两个主要命令：

1. 添加仓库：

```bash
code-dataset add <repository_url> [--alias <alias_name>]
```

这个命令用于添加一个 Git 仓库或本地目录到配置中。你可以使用 `--alias` 参数为仓库提供一个别名。

2. 刷新数据：

```bash
code-dataset refresh
```

这个命令会从所有配置的仓库中获取最新的数据，并将其保存到本地的 `data/libs` 目录中。

### 📚 示例

1. 添加一个 Git 仓库：

```bash
code-dataset add https://github.com/example/repo.git
```

2. 添加一个带有别名的仓库：

```bash
code-dataset add https://github.com/example/repo.git --alias my-repo
```

3. 添加一个本地目录：

```bash
code-dataset add /path/to/local/repo
```

4. 刷新所有数据：

```bash
code-dataset refresh
```

5. 统计数据条目：

```bash
code-dataset count
```

这个命令会统计所有项目中的数据条目，并显示一个汇总表。



## 贡献

你就可以通过 PR 的方式将本地的编程数据集提交到 code_dataset 中

---

## 🤝 贡献

我们欢迎并鼓励社区贡献。如果您有高质量的代码示例或改进建议，请提交 Pull Request 或开启 Issue。

---

🌟 如果您觉得这个项目有帮助，请给我们一个 star！您的支持是我们持续改进的动力。
