import pandas as pd
import json

def transform_users(**kwargs):
    """
    Transform the users data from the API to a pandas dataframe.
    """
    # Get the data from the XCOM variables from Airflow
    ti = kwargs['ti']
    users = ti.xcom_pull(key='return_value', task_ids='get_users')

    # Create a dataframe from the users data
    df_users = pd.DataFrame.from_dict(users)

    ## Handles certain columns, which are not in the correct format (needs to be expanded, as they are dicts)
    df_address = df_users['address'].apply(pd.Series)
    df_geo = df_address['geo'].apply(pd.Series)
    df_company = df_users['company'].apply(pd.Series)

    ## Drop the additional column from df_address
    df_address = df_address.drop(['geo'], axis=1)

    ## Then drop the other columns from df_users
    df_users = df_users.drop(['address', 'company'], axis=1)

    ## Concatenate the dataframes
    df_users[[i for i in df_address.columns]] = df_address
    df_users[[i for i in df_geo.columns]] = df_geo
    df_users[[i for i in df_company.columns]] = df_company

    ## Convert the dataframe to a dictionary
    users_json = df_users.to_dict('records')

    ## Transforms the dictionary to a json string
    users_json = json.dumps(users_json)

    ## Send the transformed data to the XCOM variable
    ti.xcom_push(key='users_json', value=users_json)
