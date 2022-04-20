print("test deployment of script")

import itc_utils.flight_service as itcfs

readClient = itcfs.get_flight_client()

nb_data_request = {
    'data_name': """customer_churn.csv""",
    'interaction_properties': {
    }
}

flightInfo = itcfs.get_flight_info(readClient, nb_data_request=nb_data_request)

data_df_1 = itcfs.read_pandas_and_concat(readClient, flightInfo)
print(data_df_1.head(10))
