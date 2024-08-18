import argparse
import json
import os
import shutil
from pathlib import Path
import git
from rich.console import Console

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

def add_repository(url):
    ensure_config_dir()
    with open(CONFIG_FILE, 'r+') as f:
        config = json.load(f)
        if url not in config['repositories']:
            config['repositories'].append(url)
            f.seek(0)
            json.dump(config, f, indent=2)
            f.truncate()
            console.print(f"Added repository: [bold green]{url}[/bold green]")
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
    
    for url in config['repositories']:
        repo_name = url.split('/')[-1].replace('.git', '')
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

def main():
    parser = argparse.ArgumentParser(description='Code Dataset CLI')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    add_parser = subparsers.add_parser('add', help='Add a repository URL')
    add_parser.add_argument('url', type=str, help='Repository URL')

    subparsers.add_parser('refresh', help='Refresh data from repositories')

    args = parser.parse_args()

    if args.command == 'add':
        add_repository(args.url)
    elif args.command == 'refresh':
        refresh_data()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()