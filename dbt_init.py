import os, subprocess
from typing import Iterable


def determine_target(adapters: dict):
    target = ''
    while target not in adapters.keys():
        new_input = str(input('Which data warehouse are you using?\r\n')).lower()
        if new_input == target:
            raise ValueError(f'This script does not yet support DBT on {target}')
        target = new_input
    return target


def install_target_adapter(target: str):
    install_command = f'-m pip install dbt-{target}'
    install_process = subprocess.Popen(
        ('/usr/local/bin/python', install_command),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return install_process


def write_profiles(project_name: str, target:str, target_env: str, parameters: Iterable):
    os.system('cp profiles_template.yml profiles.yml')
    env_details = [
        f'{project_name}\r\n',
        ' '*2 + f'target: {target_env}\r\n',
        ' '*2 + f'outputs:\r\n',
        ' '*4 + f'{target_env}:\r\n',
        ' '*6 + f'type: {target}\r\n'
    ]
    for parameter in parameters:
        parameter_value = input(f'{parameter}:\r\n')
        env_details.append(' '*6 + f'{parameter}: {parameter_value}\r\n')
    with open('profiles.yml', 'a') as dbt_profiles:
        dbt_profiles.writelines(env_details)


def write_project_config(project_name: str):
    os.system('cp dbt_project_template.yml dbt_project.yml')
    with open('dbt_project.yml', 'r') as project_file:
        project_config = project_file.read().replace('TO_BE_REPLACED', project_name)
        project_file.write(project_config)

project_name = ''
print('checking for existing profiles.yml...')
if os.path.exists(os.curdir + os.sep + 'profiles_backup.yml') and str(input('Do you want to reuse the previous profiles.yml? y/n  : ')).lower()[0] == 'y':
    os.system('mkdir -p ~/.dbt && cp profiles_backup.yml ~/.dbt/profiles.yml')
else:
    project_name = str(input('What is the name of the project?\r\n')).lower()
    available_adapters = {
        'postgres': ('host', 'port', 'threads', 'user', 'pass', 'dbname', 'schema'),
        'snowflake': ('account', 'user', 'password', 'role', 'warehouse', 'threads', 'database', 'schema')
    }
    target = determine_target(adapters = available_adapters)
    target_env = 'dev'
    adapter_installation = install_target_adapter(target = target)
    write_profiles(
        project_name = project_name,
        target = target,
        target_env = target_env,
        parameters=available_adapters[target]
    )
    os.system('cp profiles.yml profiles_backup.yml')
    os.system('mkdir -p ~/.dbt && mv ./profiles.yml ~/.dbt/profiles.yml')

write_project_config(project_name = project_name)

os.system('dbt deps')
os.system('mkdir -p models macros tests analyses assets')
print('For more info on how to proceed from here, visit https://courses.getdbt.com/courses/fundamentals')
