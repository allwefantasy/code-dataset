
# 🚀 code_dataset

code_dataset is an open-source project for code programming datasets. Unlike other programming datasets, this dataset comes from the programming iterations of actual open-source projects, using the best models currently available and being reviewed by senior developers. This ensures the quality and practicality of the dataset, providing valuable learning resources for researchers and developers.

---

## ✨ Features

- 🌟 Datasets come from the programming iterations of actual open-source projects
- 🤖 Generated using the most advanced models currently available
- 👨‍💻 Reviewed by senior developers
- 💎 High-quality, practical code examples

---

## 📂 Data Location and Structure

The collected data is stored in the `data/libs/project_repo` directory, with each project having its own subdirectory. The data for each project is stored in a `data.jsonl` file.

Each line in the `data.jsonl` file represents a single JSON object with the following structure:

```json
{
  "instruction": "The instruction for the task",
  "conversations": [
    {
      "role": "user or assistant",
      "content": "The content of the message"
    },
    ...
  ],
  "model": "The model used for generation",
  "yaml_file": "The YAML file associated with this data"
}
```

- `instruction`: The task instruction
- `conversations`: An array of conversation messages, each with a `role` and `content`
- `model`: The AI model used to generate the response
- `yaml_file`: The YAML file associated with this data entry

---

## 🛠 code-dataset Command Line Tool

If your project uses [auto-coder.chat](https://auto-coder.chat), you can use the code-dataset command line tool to manage your local programming datasets. code-dataset is a convenient command line tool for collecting and managing programming datasets that can be submitted for external use.

### 📥 Installation

1. Clone the project repository:

```bash
git clone https://github.com/yourusername/code_dataset.git
cd code_dataset
```

2. Install the code-dataset tool:

```bash
pip install -e .
```

or

```bash
pip install code-dataset
```

### 🔧 Usage

The code-dataset tool provides three main commands:

1. Add a repository:

```bash
code-dataset add <repository_url> [--alias <alias_name>]
```

This command is used to add a Git repository or local directory to the configuration. You can optionally provide an alias for the repository using the `--alias` parameter.

2. Refresh data:

```bash
code-dataset refresh
```

This command fetches the latest data from all configured repositories and saves it to the local `data/libs` directory.

3. Count data entries:

```bash
code-dataset count
```

This command counts the data entries in all projects and displays a summary table.

### 📚 Examples

1. Add a Git repository:

```bash
code-dataset add https://github.com/example/repo.git
```

2. Add a repository with an alias:

```bash
code-dataset add https://github.com/example/repo.git --alias my-repo
```

3. Add a local directory:

```bash
code-dataset add /path/to/local/repo
```

4. Refresh all data:

```bash
code-dataset refresh
```

5. Count data entries:

```bash
code-dataset count
```

6. Show data entries for a specific project:

```bash
code-dataset show <project_name> [-n <number_of_entries>]
```

This command displays data entries for a specific project. You can specify the number of entries to show using the `-n` parameter. If not specified, it will show 1 entry by default.

Example:
```bash
code-dataset show my-project -n 3
```
This will show 3 data entries from the 'my-project' dataset.

## Contribution

You can submit your local programming datasets to code_dataset via PR.

---

## 🤝 Contribution

We welcome and encourage community contributions. If you have high-quality code examples or improvement suggestions, please submit a Pull Request or open an Issue.

---

🌟 If you find this project helpful, please give us a star! Your support is the driving force for our continuous improvement.
