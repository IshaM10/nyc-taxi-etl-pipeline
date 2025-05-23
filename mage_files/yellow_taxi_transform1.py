if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd


@transformer
def transform(df1, df2, *args, **kwargs):
    
    df1['tpep_pickup_datetime'] = pd.to_datetime(df1['tpep_pickup_datetime'])
    df1['tpep_dropoff_datetime'] = pd.to_datetime(df1['tpep_dropoff_datetime'])

    df1 = df1.drop_duplicates().reset_index(drop=True)
    df1['trip_id'] = df1.index

    datetime_dim = df1[['tpep_pickup_datetime','tpep_dropoff_datetime']].reset_index(drop=True)
    datetime_dim['tpep_pickup_datetime'] = datetime_dim['tpep_pickup_datetime']
    datetime_dim['pick_hour'] = datetime_dim['tpep_pickup_datetime'].dt.hour
    datetime_dim['pick_day'] = datetime_dim['tpep_pickup_datetime'].dt.day
    datetime_dim['pick_month'] = datetime_dim['tpep_pickup_datetime'].dt.month
    datetime_dim['pick_year'] = datetime_dim['tpep_pickup_datetime'].dt.year
    datetime_dim['pick_weekday'] = datetime_dim['tpep_pickup_datetime'].dt.weekday

    datetime_dim['tpep_dropoff_datetime'] = datetime_dim['tpep_dropoff_datetime']
    datetime_dim['drop_hour'] = datetime_dim['tpep_dropoff_datetime'].dt.hour
    datetime_dim['drop_day'] = datetime_dim['tpep_dropoff_datetime'].dt.day
    datetime_dim['drop_month'] = datetime_dim['tpep_dropoff_datetime'].dt.month
    datetime_dim['drop_year'] = datetime_dim['tpep_dropoff_datetime'].dt.year
    datetime_dim['drop_weekday'] = datetime_dim['tpep_dropoff_datetime'].dt.weekday


    datetime_dim['datetime_id'] = datetime_dim.index

    # datetime_dim = datetime_dim.rename(columns={'tpep_pickup_datetime': 'datetime_id'}).reset_index(drop=True)
    datetime_dim = datetime_dim[['datetime_id', 'tpep_pickup_datetime', 'pick_hour', 'pick_day', 'pick_month', 'pick_year', 'pick_weekday',
                                'tpep_dropoff_datetime', 'drop_hour', 'drop_day', 'drop_month', 'drop_year', 'drop_weekday']]

    passenger_count_dim = df1[['passenger_count']].reset_index(drop=True)
    passenger_count_dim['passenger_count_id'] = passenger_count_dim.index
    passenger_count_dim = passenger_count_dim[['passenger_count_id','passenger_count']]

    trip_distance_dim = df1[['trip_distance']].reset_index(drop=True)
    trip_distance_dim['trip_distance_id'] = trip_distance_dim.index
    trip_distance_dim = trip_distance_dim[['trip_distance_id','trip_distance']]

    rate_code_type = {
        1:"Standard rate",
        2:"JFK",
        3:"Newark",
        4:"Nassau or Westchester",
        5:"Negotiated fare",
        6:"Group ride"
    }

    rate_code_dim = df1[['RatecodeID']].reset_index(drop=True)
    rate_code_dim['rate_code_id'] = rate_code_dim.index
    rate_code_dim['rate_code_name'] = rate_code_dim['RatecodeID'].map(rate_code_type)
    rate_code_dim = rate_code_dim[['rate_code_id','RatecodeID','rate_code_name']]

    pickup_location_dim = df1[['PULocationID']].reset_index(drop=True)
    pickup_location_dim['pickup_location_id'] = pickup_location_dim.index
    pickup_location_dim =  pd.merge(pickup_location_dim, df2, how='left',left_on='PULocationID', right_on='LocationID')
    pickup_location_dim = pickup_location_dim[['pickup_location_id','PULocationID','Zone']] 
    pickup_location_dim = pickup_location_dim.rename(columns = {'Zone':'pickup_location_name'})


    dropoff_location_dim = df1[['DOLocationID']].reset_index(drop=True)
    dropoff_location_dim['dropoff_location_id'] = dropoff_location_dim.index
    dropoff_location_dim =  pd.merge(dropoff_location_dim, df2, how='left', left_on = 'DOLocationID', right_on = 'LocationID')
    dropoff_location_dim = dropoff_location_dim[['dropoff_location_id','DOLocationID','Zone']]
    dropoff_location_dim = dropoff_location_dim.rename(columns = {'Zone':'dropoff_location_name'})

    payment_type_name = {
        1:"Credit card",
        2:"Cash",
        3:"No charge",
        4:"Dispute",
        5:"Unknown",
        6:"Voided trip"
    }
    payment_type_dim = df1[['payment_type']].reset_index(drop=True)
    payment_type_dim['payment_type_id'] = payment_type_dim.index
    payment_type_dim['payment_type_name'] = payment_type_dim['payment_type'].map(payment_type_name)
    payment_type_dim = payment_type_dim[['payment_type_id','payment_type','payment_type_name']]


    fact_table = df1.merge(passenger_count_dim, left_on='trip_id', right_on='passenger_count_id') \
                .merge(trip_distance_dim, left_on='trip_id', right_on='trip_distance_id') \
                .merge(rate_code_dim, left_on='trip_id', right_on='rate_code_id') \
                .merge(pickup_location_dim, left_on='trip_id', right_on='pickup_location_id') \
                .merge(dropoff_location_dim, left_on='trip_id', right_on='dropoff_location_id')\
                .merge(datetime_dim, left_on='trip_id', right_on='datetime_id') \
                .merge(payment_type_dim, left_on='trip_id', right_on='payment_type_id') \
                [['trip_id','VendorID', 'datetime_id', 'passenger_count_id',
                'trip_distance_id', 'rate_code_id', 'store_and_fwd_flag', 'pickup_location_id', 'dropoff_location_id',
                'payment_type_id', 'fare_amount', 'extra', 'mta_tax', 'tip_amount', 'tolls_amount',
                'improvement_surcharge', 'total_amount']]

    # data = {'fact_table': fact_table.to_dict(orient='dict'), 'datetime_dim': datetime_dim.to_dict(orient='dict'),}
    # 'passenger_count_dim': passenger_count_dim.to_dict(orient='dict'), 'trip_distance_dim': trip_distance_dim.to_dict(orient='dict'), 
    # 'rate_code_dim': rate_code_dim.to_dict(orient='dict'), 'pickup_location_dim': pickup_location_dim.to_dict(orient='dict'), 
    # 'dropoff_location_dim': dropoff_location_dim.to_dict(orient='dict'), 'payment_type_dim': payment_type_dim.to_dict(orient='dict')}

    # data = {'fact_table': fact_table, 'datetime_dim': datetime_dim}

    data_list = [[{'table_name': 'fact_table', 'data': fact_table},
    {'table_name': 'datetime_dim', 'data': datetime_dim},
    {'table_name': 'passenger_count_dim', 'data': passenger_count_dim},
    {'table_name': 'trip_distance_dim', 'data': trip_distance_dim},
    {'table_name': 'rate_code_dim', 'data': rate_code_dim},
    {'table_name': 'pickup_location_dim', 'data': pickup_location_dim},
    {'table_name': 'dropoff_location_dim', 'data': dropoff_location_dim},
    {'table_name': 'payment_type_dim', 'data': payment_type_dim}]]

    return data_list


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
