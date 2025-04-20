if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import pandas as pd
import gcsfs

@data_loader
def load_data(*args, **kwargs):

    # Initialize client (automatically uses attached service account)
    fs = gcsfs.GCSFileSystem()
    file_path = "gs://yellow_taxi_project_bucket/yellow_tripdata_2023-01.parquet"

    # Read CSV directly
    df = pd.read_parquet(fs.open(file_path), engine='pyarrow')
    df = df.iloc[0:1000000 * 1]

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
