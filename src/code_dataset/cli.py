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

def refresh_data():
    ensure_config_dir()
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    for url in config['repositories']:
        repo_name = url.split('/')[-1].replace('.git', '')
        temp_dir = Path('/tmp') / repo_name
        
        # Clone or pull the repository
        if temp_dir.exists():
            repo = git.Repo(temp_dir)
            repo.remotes.origin.pull()
        else:
            git.Repo.clone_from(url, temp_dir)
        
        # Copy the data file
        source_file = temp_dir / '.auto-coder' / 'human_as_model_conversation' / 'data.jsonl'
        if source_file.exists():
            dest_dir = DATA_DIR / repo_name
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(source_file, dest_dir / 'data.jsonl')
            console.print(f"Copied data from [bold blue]{repo_name}[/bold blue] to [bold green]{dest_dir}[/bold green]")
        else:
            console.print(f"No data file found in [bold red]{repo_name}[/bold red]")
        
        # Clean up
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