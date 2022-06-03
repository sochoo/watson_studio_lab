import json, subprocess

def promoteToProject(project_id, notebook_name, environment_name):
    query_string = "(resources[?entity.environment.display_name == '{}'].metadata.asset_id)[0]".format(environment_name)
    #result = ! cpdctl environment list --project-id {project_id} --output json -j "{query_string}" --raw-output
    bashCommand = "cpdctl environment list --project-id " + project_id + " --output json -j"
    bashCommand = bashCommand.split()
    bashCommand = bashCommand + [query_string] + ["--raw-output"]
    process = subprocess.run(bashCommand, stdout=subprocess.PIPE, text=True)
    env_id = process.stdout[:-1]
    remote_file_path = "notebook/" + notebook_name
    local_file_path = notebook_name
    #print(local_file_path)
    #! cpdctl asset file upload --path {remote_file_path} --file {local_file_path} --project-id {project_id}
    bashCommand = "cpdctl asset file upload --path {} --file {} --project-id {}".format(remote_file_path, local_file_path, project_id)
    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, text=True)
    print(process.stdout)
    print("Notebook has been uploaded!")
    print("Creating notebook asset...")
    file_name = notebook_name.replace(".ipynb", "")
    runtime = {
    'environment': env_id}
    runtime_json = json.dumps(runtime)
    originate = {'type': 'blank'}
    originate_json = json.dumps(originate)
    #result = ! cpdctl notebook create --file-reference {remote_file_path} --name {file_name} --project {project_id} --runtime '{runtime_json}' --originates-from '{originate_json}' --output json -j "metadata.asset_id" --raw-output
    #notebook_id = result.s
    bashCommand = "cpdctl notebook create --file-reference {} --name {} --project {} ".format(remote_file_path, file_name, project_id)
    bashCommand = bashCommand.split() + ['--runtime'] + [runtime_json] + ['--originates-from'] + [originate_json] + ['--output'] + ["json"] + ['-j'] + ["metadata.asset_id"]
    process = subprocess.run(bashCommand, stdout=subprocess.PIPE, text=True)
    notebook_id = process.stdout[1:-2]
    print("Notebook {} has been promoted to project with notebook id: {}".format(notebook_name, notebook_id))
    
def promoteToSpace(space_id, notebook_name, environment_name):
    query_string = "(resources[?entity.environment.display_name == '{}'].metadata.asset_id)[0]".format(environment_name)
    #result = ! cpdctl environment list --space-id {space_id} --output json -j "{query_string}" --raw-output
    bashCommand = "cpdctl environment list --space-id " + space_id + " --output json -j"
    bashCommand = bashCommand.split()
    bashCommand = bashCommand + [query_string] + ["--raw-output"]
    process = subprocess.run(bashCommand, stdout=subprocess.PIPE, text=True)
    env_id = process.stdout[:-1]
    #env_id = result.s
    remote_file_path = "notebook/" + notebook_name
    local_file_path = notebook_name
    #! cpdctl asset file upload --path {remote_file_path} --file {local_file_path} --space-id {space_id}
    bashCommand = "cpdctl asset file upload --path {} --file {} --space-id {}".format(remote_file_path, local_file_path, space_id)
    process = subprocess.run(bashCommand.split(), stdout=subprocess.PIPE, text=True)
    print(process.stdout)
    print("Notebook has been uploaded!")
    print("Creating notebook asset...")
    file_name = notebook_name.replace(".ipynb", "")
    runtime = {
    'environment': env_id}
    runtime_json = json.dumps(runtime)
    #result = ! cpdctl notebook create --file-reference {remote_file_path} --name {file_name} --space {space_id} --runtime '{runtime_json}' --output json -j "metadata.asset_id" --raw-output
    #notebook_id = result.s
    bashCommand = "cpdctl notebook create --file-reference {} --name {} --space {} ".format(remote_file_path, file_name, space_id)
    bashCommand = bashCommand.split() + ['--runtime'] + [runtime_json] + ['--output'] + ["json"] + ['-j'] + ["metadata.asset_id"]
    process = subprocess.run(bashCommand, stdout=subprocess.PIPE, text=True)
    notebook_id = process.stdout[1:-2]
    
    print("Notebook {} has been promoted to Space with notebook id: {}".format(notebook_name, notebook_id))
    