import pyarrow.csv as csv
import pyarrow.feather as feather
import pyarrow.parquet as parquet
import pyarrow.orc as orc
import pandas as pd
import pyarrow as pa

class FileWriter:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def write_file(self, name, d):
            #TODO: Work out why we cannot convert from batch to table
            df = d.to_pandas()
            data = pa.Table.from_pandas(df)
            if name.endswith(".feather"):
                return self.write_feather(name, data, **self._kwargs)
            elif name.endswith(".parquet"):
                return self.write_parquet(name, data, **self._kwargs)
            elif name.endswith(".csv"):
                return self.write_csv(name, data, **self._kwargs)
            elif name.endswith(".json"):
                return self.write_json(name, data, **self._kwargs)
            elif name.endswith(".orc"):
                return self.write_orc(name, data, **self._kwargs)
            else:
                raise ValueError("Unsupported file type")

    def write_feather(self, name, data, **kwargs):
        try:
            feather.write_feather(df = data, dest = name, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
    def write_parquet(self,name, data, **kwargs):
        try:
            parquet.write_table(table = data, where = name, version='2.6' ,**kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        
    def write_csv(self,name, data, **kwargs):
        try:
            with csv.CSVWriter(sink = name, schema = data.schema,**kwargs) as writer:
                writer.write_table(data)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    def write_orc(self,name, data, **kwargs):
        try:
            orc.write_table(data, name, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    
    #TODO: Use pyarrow.json.read_json() instead of pandas.read_json()
    def write_json(self,name, data, **kwargs):
       try: 
            df = data.to_pandas()
            df.to_json(name, **kwargs)
       except Exception as e:
            print(f"An error occurred: {e}")
            return None

    