import os, re


def determine_target(adapters: dict):
    target = ''
    while target not in adapters.keys():
        new_input = str(input('Which data warehouse are you using?\r\n')).lower()
        if new_input == target:
            raise ValueError(f'This script does not yet support DBT on {target}')
        target = new_input
    return target


def write_profiles(project_name: str, target:str, target_env: str, parameters: tuple):
    os.system('cp profiles_template.yml profiles.yml')
    env_details = [
        f'{project_name}:\r\n',
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
    project_config = ''
    with open('dbt_project.yml', 'r') as project_file:
        project_config += project_file.read().replace('TO_BE_REPLACED', project_name)
    with open('dbt_project.yml', 'w') as project_file:
        project_file.write(project_config)


project_name = ''
print('checking for existing profiles.yml...')
if os.path.exists(os.curdir + os.sep + 'profiles_backup.yml') and str(input('Do you want to reuse the previous profiles.yml? y/n  : ')).lower()[0] == 'y':
    with open('profiles_backup.yml', 'r') as backup_file:
        for result in re.findall(r'WAREHOUSE CONFIGURATION([#\-\s]+)([a-zA-Z_\-]+)', backup_file.read()):
            project_name = result[1]
    os.system('mkdir -p ~/.dbt && cp profiles_backup.yml ~/.dbt/profiles.yml')
else:
    project_name = str(input('What is the name of the project? Only lowercase and underscores allowed!\r\n')).lower()
    available_adapters = {
        'postgres': ('host', 'port', 'threads', 'user', 'pass', 'dbname', 'schema'),
        'snowflake': ('account', 'user', 'password', 'role', 'warehouse', 'threads', 'database', 'schema'),
        'sqlserver': ('driver', 'server', 'port', 'schema', 'user', 'password')
    }
    target = determine_target(adapters = available_adapters)
    target_env = 'dev'
    os.system(f'/usr/local/bin/python -m pip install dbt-{target}')
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
os.system('mkdir -p models/staging models/sources macros tests analyses assets')

with open('/root/.dbt/profiles.yml', 'r') as pro_file:
    for schema in re.findall(r'schema: ([a-zA-Z_\-]+)', pro_file.read(), flags = re.MULTILINE | re.IGNORECASE):
        os.system(f"dbt run-operation generate_source --args 'schema_name: {schema}' > {os.curdir}/{schema}.yml")
        with open(f'{os.curdir}/{schema}.yml', 'r') as sources:
            for result in re.findall(r'(version: 2(.*\s)+)', sources.read(), flags = re.MULTILINE | re.IGNORECASE):
                os.system(f'touch {os.curdir}/models/sources/{schema}.yml')
                with open(f'{os.curdir}/models/sources/{schema}.yml', 'w') as yml_file:
                    yml_file.write(result[0])
        os.system(f'mkdir -p {os.curdir}/models/staging/{schema}')
        os.system(f'dbt-generator generate -s ' + os.curdir + os.sep + f'models/sources/{schema}.yml -o ' + os.curdir + os.sep + f'models/staging/{schema}')

print('For more info on how to proceed from here, visit https://courses.getdbt.com/courses/fundamentals')
