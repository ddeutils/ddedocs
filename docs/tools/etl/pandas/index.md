---
icon: simple/pandas
---

# Pandas

[Pandas for Data Engineers](https://towardsdatascience.com/pandas-for-data-engineers-a191965ac538)

```python
def etl(cursor):
    cursor.execute("<query>")
    for row in cursor.fetchall():
        yield row

def df_generator(cursor):
    print('Creating pandas DF using generator...')
    column_names = ['id',
                'merchant',
                'status',
                'transaction_date',
                'amount_usd']

    df = pd.DataFrame(data = etl(cursor), columns=column_names)
    print('DF successfully created!\n')
    return df

def df_create_from_batch(cursor, batch_size):
    print('Creating pandas DF using generator...')
    colnames = ['id',
               'merchant',
               'status',
               'transaction_date',
               'amount_usd']

    df = pd.DataFrame(columns=colnames)
    # execute a database query to extract data
    cursor.execute(query)
    while True:
        rows = cursor.fetchmany(batch_size)
        if not rows:
            break
        # some ETL on a chunk of data of batch_size
        batch_df = pd.DataFrame(data = rows, columns=colnames)
        df = pd.concat([df, batch_df], ignore_index=True)
    print('DF successfully created!\n')
    return df
```

```python
import boto3
import json
from datetime import datetime
import pytz
s3 = boto3.client('s3')


def upload_chunks(chunk_gen, s3_bucket, s3_file_prefix):
    """Perform Multi-part upload to AWS S3 datalake"""
    try:
        cnt = 0
        logs = []
        for chunk in chunk_gen:
            part = bytes(json.dumps(chunk), encoding='utf8')
            key = s3_file_prefix + file_key()
            s3.put_object(Body=part, Bucket=s3_bucket, Key=key)
            logs.append(f'aws s3 cp s3://{s3_bucket}/{key} ./ ')
            cnt += 1

        print(f'upload_chunks: Uploaded {cnt} chunks.')
        print('\n'.join(str(i) for i in logs))
    except Exception as e:
        print(e)

def file_key():
    """Get a file suffix, i.e. /data_pipe_1/2023/12/11/09/5234023930"""
    suffix = datetime.utcnow().replace(tzinfo=pytz.utc).strftime('%Y/%m/%d/%H/%M%S%f')
    return f'{suffix}'

def df_create_from_batch(cursor, batch_size):
     print('Creating pandas DF using generator...')
     colnames = ['id',
                'merchant',
                'status',
                'transaction_date',
                'amount_usd']

     df = pd.DataFrame(columns=colnames)
     # execute a database query to extract data
     cursor.execute(query)
     while True:
         rows = cursor.fetchmany(batch_size)
         if not rows:
             break
         # some ETL on a chunk of data of batch_size
         batch_df = pd.DataFrame(data = rows, columns=colnames)
         yield batch_df
     print('DF successfully created!\n')
     return df

s3_upload_scope = df_create_from_batch(cursor, 10000)
upload_chunks(s3_upload_scope, config.get('s3_bucket'), pipe['name'])
```

```python
def chunk_gen(itemList, chunks):
    '''Read data in chunks and yield each chunk'''
    for i in range(0, len(itemList), chunks):
        yield itemList[i:i + chunks]

def sb_batch_extract(idList_gen):
    '''Reads data generator, i.e. list of ids, and works with each batch
    to extract data from database
    '''
    try:
        step = 1
        while True:
            ids = next(idList_gen)
            logging.debug(f'> Step {step} processing ids:  {ids})')
            ids_str = ','.join(str(i) for i in ids)
            out = get_sb_data(sql, ids_str)
            logging.debug(f'> Step {step} ids used to produce : {out}')
            step += 1
            yield out
    except Exception as e:
        print(e)
    except StopIteration:
        pass
    finally:
        del idList_gen

#  Step 1: Generate user id list as generator object.
idList_gen = chunk_gen([col[0] for col in get_ids()], 250)
# Step 2: Extract in chunks from database:
extract = sb_batch_extract(idList_gen)

actual = [i for i in batch_extract_demo(idList_gen)]
```

## Practices

- [:simple-medium: Don't use `loc`/`iloc` with Loops, Instead, Use This!](https://medium.com/codex/dont-use-loc-iloc-with-loops-in-python-instead-use-this-6a7ab0b04d35)
