# dbt-project-quickstart
Custom Docker-container and python script for streamlining new DBT-projects.

## Designed for dbt-core development using Visual Studio Code.
> However, the script can be run if dbt is installed locally as well.

## Using VS Code
**Requires Docker**
To use this repo to quickstart a DBT-project in VS Code, you need to have the following extensions installed:
- Docker (ms-azuretools.vscode-docker)
- Remote - Containers (ms-vscode-remote.remote-containers)

Run command **Clone repository in Container Volume**
Pick this repository -> main branch and voila!

## Using local DBT installation
1. Clone repository to desired location
2. Backup any existing profiles.yml (usually at $HOME/.dbt/profiles.yml):
```bash
cp $HOME/.dbt/profiles.yml $HOME/.dbt/profiles.backup.yml
```
3. Run dbt_init.py script:
```bash
chmod +x dbt_init.py && python dbt_init.py
```
