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

- Use the `influx3 create config` command to create or modify config--for example:

    ```bash
    influx3 create config \
    --name="my-config" \
    --database="<database or bucket name>" \
    --host="us-east-1-1.aws.cloud2.influxdata.com" \
    --token="<your token>" \
    --org="<your org ID>"
    ```
    
  The output is the configuration in a `config.json` file. This is saved within a directory called `config` located within your `Documents` folder.


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

The InfluxDB CLI and client library can write data from CSV, JSON, ORC, Parquet and Feather files.
The CSV file must contain the following:

- A header row with column names
- A column that contains a timestamp for each row

The following CLI options specify how data is parsed:

* `--file` - The path to the file.
* `--time` - The name of the column containing the timestamp.
* `--measurement` - The name of the measurement to store the data under. (Optional, will look for a measurement column in data otherwise).
* `--tags` - (optional) Specify an array of column names to use as tags. (Currently only supports user-specified strings) for example: `--tags=host,region`

The following example shows how to write CSV data from the [`./Examples/example.csv` file](https://github.com/InfluxCommunity/influxdb3-python/blob/main/Examples/example.csv) to InfluxDB (as line protocol):

```bash
influx3 write_file --file ./Examples/example.csv --measurement table2 --time Date --tags host,region
```

## Config Commands

The `config` command allows you to manage configurations for your application. It has the following subcommands: `create`, `update`, `use`, `delete`, and `list`.

### Create

The `create` subcommand creates a new configuration. It requires the `--name`, `--host`, `--token`, `--database`, and `--org` parameters. The `--active` parameter is optional and can be used to set the new configuration as the active one.

Example usage:

```bash
influx3.py config create --name="my-config" --host="us-east-1-1.aws.cloud2.influxdata.com" --token="<your token>" --database="<database or bucket name>" --org="<your org ID>" --active
```

### Update

The `update` subcommand updates an existing configuration. The `--name` parameter is required to specify which configuration to update. All other parameters (`--host`, `--token`, `--database`, `--org`, `--active`) are optional.

Example usage:

```bash
influx3.py config update --name="my-config" --host="new-host.com"
```

### Use

The `use` subcommand sets a specific configuration as the active one. The `--name` parameter is required to specify which configuration to use.

Example usage:

```bash
influx3.py config use --name="my-config"
```

### Delete

The `delete` subcommand deletes a configuration. The `--name` parameter is required to specify which configuration to delete.

Example usage:

```bash
influx3.py config delete --name="my-config"
```

### List

The `list` subcommand lists all the configurations.

Example usage:

```bash
influx3.py config list
```

Please replace `"my-config"`, `"us-east-1-1.aws.cloud2.influxdata.com"`, `"<your token>"`, `"<database or bucket name>"`, and `"<your org ID>"` with your actual values.

## (Beta) OpenAI (ChatGPT) Support
The CLI also contians a beta feature that allows you to query your data using OpenAI's ChatGPT. To use this feature, you must have an OpenAI API key. You can get one by signing up for the [OpenAI waitlist](https://share.hsforms.com/1Lfc7WtPLRk2ppXhPjcYY-A4sk30). Once you have an API key, you can set it as an environment variable called `OPENAI_API_KEY`.

To use this feature, you can use the `chatgpt` command:
```
export OPENAI_API_KEY=sk-o2Sbq3aVBp

influx3 chatgpt get average vibration grouped by machineID from machine_data
Run InfluxQL query: SELECT MEAN(vibration) AS avg_vibration FROM machine_data GROUP BY machineID
|    | iox::measurement   | time                | machineID   |   avg_vibration |
|---:|:-------------------|:--------------------|:------------|----------------:|
|  0 | machine_data       | 1970-01-01 00:00:00 | machine1    |         85.2356 |
|  1 | machine_data       | 1970-01-01 00:00:00 | machine2    |        190.273  |
|  2 | machine_data       | 1970-01-01 00:00:00 | machine3    |         85.4789 |
Press TAB to fetch next chunk of data

```


## Client library

The underlying client library is also available for use in your own code: https://github.com/InfluxCommunity/influxdb3-python

## Contribution

When developing a new feature for the CLI or the client library, make sure to test your feature in both for breaking changes.

#
