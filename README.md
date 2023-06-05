<p align="center">
    <img src="https://github.com/InfluxCommunity/influxdb3-python-cli/blob/main/python-logo.png?raw=true" alt="Your Image" width="150px">
</p>

<p align="center">
    <a href="https://pypi.org/project/influxdb3-python-cli/">
        <img src="https://img.shields.io/pypi/v/influxdb3-python-cli.svg" alt="PyPI version">
    </a>
    <a href="https://pypi.org/project/influxdb3-python-cli/">
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
This repository contains a CLI extension to the [influxdb 3.0 python client library](https://github.com/InfluxCommunity/influxdb3-python). While this code is built on officially supported APIs, the library and CLI here are not officially support by InfluxData. 

## Install
To install the CLI, enter the following command in your terminal:

```bash
python3 -m pip install influxdb3-python-cli
```


### Scope and privileges

Python provides the following methods for installing packages within a specific scope:

- To isolate the CLI (and its dependencies) to your project directory, install the CLI in a _virtual environment_. [See how to create and use a `venv` or `conda` Python virtual environment](https://docs.influxdata.com/influxdb/cloud-serverless/query-data/execute-queries/flight-sql/python/#create-a-python-virtual-environment).
- To install the client to a user-specific directory (without administrative rights), pass the `--user` flag in the `pip` command.
- To install the client in your system-wide path, use `sudo` with admin privileges.

## Add a config

To configure the CLI, do _one_ of the following:

- Use the `influx3 config` command to create or modify config--for example:

    ```bash
    influx3 config \
    --name="my-config" \
    --database="<database or bucket name>" \
    --host="us-east-1-1.aws.cloud2.influxdata.com" \
    --token="<your token>" \
    --org="<your org ID>"
    ```
    
  The output is the configuration in a `config.json` file.

- In your editor, create or edit the `config.json` file, and then save it to the directory where you're using the `influx3` command--for example:

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

If you're running the CLI against InfluxDB Cloud Serverless, replace `your-database` in the examples with your Cloud Serverless _bucket name_.

## Run as a command

```
influx3 sql "select * from anomalies"
```

```
influx3 write testmes f=7 
```

## Query and write interactively

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

## Write from a file

The InfluxDB CLI and client library can write data from a CSV file.
The CSV file must contain the following:

- A header row with column names
- A column that contains a timestamp for each row

The following CLI options specify how data is parsed:

* `--file` - The path to the csv file.
* `--time` - The name of the column containing the timestamp.
* `--measurement` - The name of the measurment to store the CSV data under. (Currently only supports user specified string)
* `--tags` - (optional) Specify an array of column names to use as tags. (Currently only supports user specified strings) for example: `--tags=host,region`

The following example shows how to write CSV data from the [`./Examples/example.csv` file](https://github.com/InfluxCommunity/influxdb3-python/blob/main/Examples/example.csv) to InfluxDB (as line protocol):

```bash
influx3 write_csv --file ./Examples/example.csv --measurement table2 --time Date --tags host,region
```

## Client library

The underlying client library is also available for use in your own code: https://github.com/InfluxCommunity/influxdb3-python

## Contribution

When developing a new feature for the CLI or the client library, make sure to test your feature in both for breaking changes.

#
