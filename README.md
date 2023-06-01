<p align="center">
    <img src="https://github.com/InfluxCommunity/influxdb3-python-cli/blob/main/python-logo.png?raw=true" alt="Your Image" width="150px">
</p>

<p align="center">
    <a href="https://pypi.org/project/influxdb3-python-cli/">
        <img src="https://img.shields.io/pypi/v/influxdb3-python-cli.svg" alt="PyPI version">
    </a>
    <a href="https://pypi.org/project/your-python-package/">
        <img src="https://img.shields.io/pypi/dm/influxdb3-python-cli.svg" alt="PyPI downloads">
    </a>
    <a href="https://github.com/InfluxCommunity/influxdb3-python-cli/actions/workflows/pylint.yml">
        <img src="https://github.com/InfluxCommunity/influxdb3-python-cli/actions/workflows/pylint.yml/badge.svg" alt="Lint Code Base">
    </a>
        <a href="https://github.com/InfluxCommunity/influxdb3-python-cli/actions/workflows/python-publish.yml">
        <img src="https://github.com/InfluxCommunity/influxdb3-python-cli/actions/workflows/python-publish.yml/badge.svg" alt="Lint Code Base">
    </a>
    <a href="https://influxcommunity.slack.com">
        <img src="https://img.shields.io/badge/slack-join_chat-white.svg?logo=slack&style=social" alt="Community Slack">
    </a>
</p>

# influxdb3-python-cli
## About
This repository contains an extention to the influxdb 3.0 python client libary. While this code is built on officially supported APIs, the library and CLI here are not officially support by Influx Data. 

## Install
To install only the client:

```bash
python3 -m pip install pyinflux3
```

To install the client and CLI:

```bash
sudo python3 -m pip install "pyinflux3[cli]"
```

***Note: Use sudo if you would like to directly install the client onto your path. Otherwise use the `--user` flag.**

## Add a Config

To configure `pyinflux3` and the CLI, do one of the following:

You can drop a config file called `config.json` in the directory where you are running the `influx3` command:

```json
{
    "my-config": {
        "database": "your-database",
        "host": "your-host",
        "token": "your-token",
        "org": "your-org-id",
        "active": true
    }
}
```


- Use the `config` command to create or modify a config:

    ```
    influx3 config \
    --name="my-config" \
    --database="<database or bucket name>" \
    --host="us-east-1-1.aws.cloud2.influxdata.com" \
    --token="<your token>" \
    --org="<your org ID>"
    ```

If you are running against InfluxDB Cloud Serverless, then use the _bucket name_ as the database in your configuration.

## Run as a Command

```
influx3 sql "select * from anomalies"
```

```
influx3 write testmes f=7 
```

## Query and Write Interactively

In your terminal, enter the following command:

```
influx3
```

`influx3` displays the `(>)` interactive prompt and waits for input.

```
Welcome to my IOx CLI.

(>)
```

To query, type `sql` at the prompt.

```
(>) sql
```

At the `(sql >)` prompt, enter your query statement:

```
(sql >) select * from home
```

The `influx3` CLI displays query results in Markdown table format--for example:

```
|     |   co |   hum | room        |   temp | time                          |
|----:|-----:|------:|:------------|-------:|:------------------------------|
|   0 |    0 |  35.9 | Kitchen     |   21   | 2023-03-09 08:00:00           |
|   1 |    0 |  35.9 | Kitchen     |   21   | 2023-03-09 08:00:50           |
```

To write, type `write` at the `(>)` prompt.

```
(>) write
```

At the `(write >)` prompt, enter line protocol data.

```
(>) write 
home,room=kitchen temp=70.5,hum=80
```

To exit a prompt, enter `exit`.

## Write from a File

Both the InfluxDB CLI and Client libary support writing from a CSV file. The CSV file must have a header row with the column names. The there must be a column containing a timestamp. Here are the parse options:
* `--file` - The path to the csv file.
* `--time` - The name of the column containing the timestamp.
* `--measurement` - The name of the measurment to store the CSV data under. (Currently only supports user specified string)
* `--tags` - (optional) Specify an array of column names to use as tags. (Currently only supports user specified strings) for example: `--tags=host,region`

```bash
influx3 write_csv --file ./Examples/example.csv --measurement table2 --time Date --tags host,region
```

## Client library
The underlining client library is also available for use in your own code: https://github.com/InfluxCommunity/influxdb3-python

## Contribution
If you are working on a new feature for either the CLI or the Client Libary please make sure you test both for breaking changes. 

#