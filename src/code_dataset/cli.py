import argparse
import json
import os
import shutil
from pathlib import Path
import git
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()

CONFIG_DIR = Path.home() / '.code_dataset'
CONFIG_FILE = CONFIG_DIR / 'config.json'
DATA_DIR = Path(os.getcwd()) / 'data' / 'libs'
TEMP_DIR = Path(os.getcwd()) / 'repo_temp'

def is_git_repo(url):
    return url.endswith('.git') or ':' in url

def ensure_config_dir():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"repositories": []}, f)

def add_repository(url, alias=None):
    ensure_config_dir()
    with open(CONFIG_FILE, 'r+') as f:
        config = json.load(f)
        existing_repo = next((repo for repo in config['repositories'] if repo['url'] == url), None)
        if not existing_repo:
            new_repo = {'url': url, 'alias': alias} if alias else {'url': url}
            config['repositories'].append(new_repo)
            f.seek(0)
            json.dump(config, f, indent=2)
            f.truncate()
            console.print(f"Added repository: [bold green]{url}[/bold green]" + (f" with alias [bold blue]{alias}[/bold blue]" if alias else ""))
        else:
            console.print(f"Repository already exists: [bold yellow]{url}[/bold yellow]")

def add_to_gitignore(path):
    gitignore_path = Path(os.getcwd()) / '.gitignore'
    if not gitignore_path.exists():
        gitignore_path.touch()
    
    with open(gitignore_path, 'r+') as f:
        content = f.read()
        if path not in content:
            if content and not content.endswith('\n'):
                f.write('\n')
            f.write(f'{path}\n')
            console.print(f"Added [bold green]{path}[/bold green] to .gitignore")

def refresh_data():
    ensure_config_dir()
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)    
    
    for repo in config['repositories']:
        url = repo['url']
        repo_name = repo.get('alias') or url.split('/')[-1].replace('.git', '')
        temp_dir = TEMP_DIR / repo_name
        
        if is_git_repo(url):
            # Clone or pull the repository
            if temp_dir.exists():
                repo = git.Repo(temp_dir)
                repo.remotes.origin.pull()
            else:
                git.Repo.clone_from(url, temp_dir)
            source_dir = temp_dir
        else:
            # Local directory
            source_dir = Path(url)
            if not source_dir.exists():
                console.print(f"[bold red]Error:[/bold red] Local directory not found: {url}")
                continue
        
        # Copy the data file
        source_file = source_dir / '.auto-coder' / 'human_as_model_conversation' / 'data.jsonl'
        if source_file.exists():
            dest_dir = DATA_DIR / repo_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(source_file, dest_dir / 'data.jsonl')
            console.print(f"Copied data from [bold blue]{repo_name}[/bold blue] to [bold green]{dest_dir}[/bold green]")
        else:
            console.print(f"No data file found in [bold red]{repo_name}[/bold red]")
        
        # Clean up if it's a git repo
        if is_git_repo(url):
            shutil.rmtree(temp_dir)

def count_data():
    table = Table(title="Data Count")
    table.add_column("Project", style="cyan", no_wrap=True)
    table.add_column("Count", style="magenta")

    total_count = 0
    for project_dir in DATA_DIR.iterdir():
        if project_dir.is_dir():
            data_file = project_dir / 'data.jsonl'
            if data_file.exists():
                with open(data_file, 'r') as f:
                    count = sum(1 for _ in f)
                total_count += count
                table.add_row(project_dir.name, str(count))

    table.add_row("Total", str(total_count), style="bold")
    console.print(table)

def show_data(project_name, num_entries=1):
    project_dir = DATA_DIR / project_name
    data_file = project_dir / 'data.jsonl'
    
    if not data_file.exists():
        console.print(f"[bold red]Error:[/bold red] No data file found for project {project_name}")
        return

    with open(data_file, 'r') as f:
        for i, line in enumerate(f):
            if i >= num_entries:
                break
            
            data = json.loads(line)
            instruction = data.get('instruction', 'No instruction available')
            conversations = data.get('conversations', [])
            model = data.get('model', 'Unknown model')
            yaml_file = data.get('yaml_file', 'No YAML file specified')

            console.print(Panel(f"[bold blue]Entry {i+1}[/bold blue]"))
            console.print(Panel(instruction, title="Instruction", expand=False))
            
            for j, conv in enumerate(conversations):
                role = conv.get('role', 'Unknown')
                content = conv.get('content', 'No content')
                console.print(Panel(Syntax(content, "markdown"), title=f"Conversation {j+1} - {role}", expand=False))
            
            console.print(f"[bold green]Model:[/bold green] {model}")
            console.print(f"[bold green]YAML File:[/bold green] {yaml_file}")
            console.print("\n")

def main():
    parser = argparse.ArgumentParser(description='Code Dataset CLI')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    add_parser = subparsers.add_parser('add', help='Add a repository URL')
    add_parser.add_argument('url', type=str, help='Repository URL')
    add_parser.add_argument('--alias', type=str, help='Alias for the repository', default=None)

    subparsers.add_parser('refresh', help='Refresh data from repositories')
    subparsers.add_parser('count', help='Count data entries in all projects')

    show_parser = subparsers.add_parser('show', help='Show data entries for a specific project')
    show_parser.add_argument('project', type=str, help='Project name')
    show_parser.add_argument('-n', type=int, default=1, help='Number of entries to show')

    args = parser.parse_args()

    if args.command == 'add':
        add_repository(args.url, args.alias)
    elif args.command == 'refresh':
        refresh_data()
    elif args.command == 'count':
        count_data()
    elif args.command == 'show':
        show_data(args.project, args.n)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()