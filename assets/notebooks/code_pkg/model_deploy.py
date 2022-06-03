def model_deploy(space_uid, space_name, use_existing_space, model_to_deploy, model_name,  deployment_name, _X_train, _y_train):
    from ibm_watson_machine_learning import APIClient
    import os
    import pandas as pd
    token = os.environ['USER_ACCESS_TOKEN']
    wml_credentials = {
        "token": token,
        "instance_id" : "openshift",
        "url": os.environ['RUNTIME_ENV_APSX_URL'], "version": "4.0"}
    client = APIClient(wml_credentials)
    
    for space in client.spaces.get_details()['resources']:
        if space['entity']['name'] == space_name:
            print("Deployment space with name",space_name,"already exists . .")
            space_uid = space['metadata']['id']
        client.set.default_space(space_uid)
        if(use_existing_space==False):
            for deployment in client.deployments.get_details()['resources']:
                print("Deleting deployment",deployment['entity']['name'], "in the space",)
                deployment_id=deployment['metadata']['id']
                client.deployments.delete(deployment_id)
            print("Deleting Space ",space_name,)
            client.spaces.delete(space_uid)
            time.sleep(10)
        else:
            print("Using the existing space")
    
    if (space_uid=="" or use_existing_space==False):
        print("\nCreating a new deployment space -",space_name)
        # create the space and set it as default
        space_meta_data = {
        client.spaces.ConfigurationMetaNames.NAME : space_name}
        stored_space_details = client.spaces.store(space_meta_data)
        space_uid = stored_space_details['metadata']['id']
        client.set.default_space(space_uid)
        
    sw_spec_uid = client.software_specifications.get_uid_by_name("runtime-22.1-py3.9")

    metadata = {
        client.repository.ModelMetaNames.NAME: model_name,
        client.repository.ModelMetaNames.INPUT_DATA_SCHEMA:[{'id': '1', 'type': 'struct', 'fields': [{"name":column_name,"type":str(column_type[0])} for column_name,column_type in pd.DataFrame(_X_train.dtypes).T.to_dict('list').items()]}],
        client.repository.ModelMetaNames.TYPE: "scikit-learn_1.0",
        client.repository.ModelMetaNames.SOFTWARE_SPEC_UID: sw_spec_uid ,
        #client.repository.ModelMetaNames.TAGS: ['attrition_model_tag']
    }
    stored_model_details = client.repository.store_model(model=model_to_deploy, meta_props=metadata, training_data=_X_train, training_target=_y_train, feature_names = list(_X_train.columns))
    
    meta_props = {
    client.deployments.ConfigurationMetaNames.NAME: deployment_name,
    #client.deployments.ConfigurationMetaNames.TAGS : ['attrition_deployment_tag'],
    client.deployments.ConfigurationMetaNames.ONLINE: {},
    client.deployments.ConfigurationMetaNames.DESCRIPTION:"",
    
}

    # deploy the model
    model_uid = stored_model_details["metadata"]["id"]
    deployment_details = client.deployments.create(artifact_uid=model_uid, meta_props=meta_props)
    return deployment_details
    
