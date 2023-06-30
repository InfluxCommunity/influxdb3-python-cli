#!/usr/bin/env python3

import cmd, ast
import argparse
import json
from prompt_toolkit import PromptSession
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import SqlLexer
from influxdb_client_3 import InfluxDBClient3
import os
from config_helper import config_helper

_usage_string = """
to write data use influxdb line protocol:
> influx3 write testmes,tag1=tagvalue field1=0.0 <optional timestamp>

to read data with sql:
> influx3 sql select * from testmes where time > now() - interval'1 minute'

to enter interactive mode:
> influx3
"""

_description_string = 'CLI application for Querying IOx with arguments and interactive mode.'

class IOXCLI(cmd.Cmd):
    intro = 'Welcome to my IOx CLI.\n'
    prompt = '(>) '

    def __init__(self):
        super().__init__()
        self.config_helper = config_helper()
        self.active_config = self.config_helper._get_active()
        self._setup_client()
        self._sql_prompt_session = PromptSession(lexer=PygmentsLexer(SqlLexer))
        self._write_prompt_session = PromptSession(lexer=None)
       

    def do_sql(self, arg):
        if self.active_config == {}:
            print("can't query, no active configs")
            return
        try: 
            table = self.influxdb_client.query(query=arg, language="sql")
            print(table.to_pandas().to_markdown())
        except Exception as e:
            print(e)

    def do_influxql(self, arg):
        if self.active_config == {}:
            print("can't query, no active configs")
            return
        try: 
            table = self.influxdb_client.query(query=arg, language="influxql")
            print(table.to_pandas().to_markdown())
        except Exception as e:
            print(e)

    def do_write(self, arg):
        if self.active_config == {}:
            print("can't write, no active configs")
            return
        if arg == "":
            print("can't write, no line protocol supplied")
            return
        
        self.influxdb_client.write(record=arg)
    
    def do_write_csv(self, args):
        if self.active_config == {}:
            print("can't write, no active configs")
            return

        temp = {}
        attributes = ['file', 'measurement', 'time', 'tags']
        temp['tags'] = []

        for attribute in attributes:
            arg_value = getattr(args, attribute)
            if arg_value is not None:
                temp[attribute] = arg_value
        if isinstance(temp['tags'], str):
            temp['tags'] =  temp['tags'].split(',')


        self.influxdb_client.write_csv(csv_file=temp['file'], 
                                       measurement_name=temp['measurement'], 
                                       timestamp_column=temp['time'], 
                                       tag_columns=temp['tags'])

    def do_exit(self, arg):
        'Exit the shell: exit'
        print('\nExiting ...')
        return True

    def do_EOF(self, arg):
        'Exit the shell with Ctrl-D'
        return self.do_exit(arg)

 
    def precmd(self, line):
        if line.strip() == 'sql':
            self._run_prompt_loop('(sql >) ', self.do_sql, 'SQL mode')
            return ''
        if line.strip() == 'influxql':
            self._run_prompt_loop('(influxql >) ', self.do_influxql, 'INFLUXQL mode')
            return ''
        if line.strip() == 'write':
            self._run_prompt_loop('(write >) ', self.do_write, 'write mode')
            return ''
        return line

    def _run_prompt_loop(self, prompt, action, mode_name):
        prompt_session = self._sql_prompt_session if mode_name == 'SQL mode' else self._write_prompt_session
        while True:
            try:
                statement = prompt_session.prompt(prompt)
                if statement.strip().lower() == 'exit':
                    break
                action(statement)
            except KeyboardInterrupt:
                print(f'Ctrl-D pressed, exiting {mode_name}...')
                break
            except EOFError:
                print(f'Ctrl-D pressed, exiting {mode_name}...')
                break
    
    def create_config(self, args):
        self.config_helper._create(args)

    
    def delete_config(self, args):
        self.config_helper._delete(args)

    
    def list_config(self, args):
        self.config_helper._list(args)
    
    def use_config(self, args):
        self.config_helper._set_active(args)


    def update_config(self, args):
        self.config_helper._update(args)


        
    def _setup_client(self):
        try:
            self._database = self.active_config['database']

            self.influxdb_client = InfluxDBClient3(
                host=self.active_config['host'],
                org=self.active_config['org'],
                token=self.active_config['token'],
                database=self.active_config['database']
            )
        except Exception as e:
            print("No active config found, please run 'config' command to create a new config")


class StoreRemainingInput(argparse.Action):
    def __call__(self, parser, database, values, option_string=None):
        setattr(database, self.dest, ' '.join(values))

def parse_args():
    parser = argparse.ArgumentParser(description= _description_string
                                     )
    subparsers = parser.add_subparsers(dest='command')

    sql_parser = subparsers.add_parser('sql', help='execute the given SQL query')
    sql_parser.add_argument('query', metavar='QUERY', nargs='*', action=StoreRemainingInput, help='the SQL query to execute')
    influxql_parser = subparsers.add_parser('influxql', help='execute the given InfluxQL query')
    influxql_parser.add_argument('query', metavar='QUERY', nargs='*', action=StoreRemainingInput, help='the INFLUXQL query to execute')

    write_parser = subparsers.add_parser('write', help='write line protocol to InfluxDB')
    write_parser.add_argument('line_protocol', metavar='LINE PROTOCOL',  nargs='*', action=StoreRemainingInput, help='the data to write')

    write_csv_parser = subparsers.add_parser('write_csv', help='write CSV data to InfluxDB')
    write_csv_parser.add_argument('--file', help='the CSV file to import', required=True)
    write_csv_parser.add_argument('--measurement', help='Define the name of the measurement', required=True)
    write_csv_parser.add_argument('--time', help='Define the name of the time column with the csv file', required=True)
    write_csv_parser.add_argument('--tags', help='(optional) array of column names which are tags. Format should be: ["tag1", "tag2"]', required=False)

    config_parser = subparsers.add_parser("config", help="configure the application")
    config_subparsers = config_parser.add_subparsers(dest='config_command')

    create_parser = config_subparsers.add_parser("create", help="create a new configuration")
    create_parser.add_argument("--name", help="Configuration name", required=True)
    create_parser.add_argument("--host", help="Host string", required=True)
    create_parser.add_argument("--token", help="Token string", required=True)
    create_parser.add_argument("--database", help="Database string", required=True)
    create_parser.add_argument("--org", help="Organization string", required=True)
    create_parser.add_argument("--active", help="Set this configuration as active", required=False, action='store_true')

        # Update command
    update_parser = config_subparsers.add_parser("update", help="update an existing configuration")
    update_parser.add_argument("--name", help="Configuration name", required=True)
    update_parser.add_argument("--host", help="Host string", required=False)
    update_parser.add_argument("--token", help="Token string", required=False)
    update_parser.add_argument("--database", help="Database string", required=False)
    update_parser.add_argument("--org", help="Organization string", required=False)
    update_parser.add_argument("--active", help="Set this configuration as active", required=False, action='store_true')

    # Use command
    use_parser = config_subparsers.add_parser("use", help="use a specific configuration")
    use_parser.add_argument("--name", help="Configuration name", required=True)

    delete_parser = config_subparsers.add_parser("delete", help="delete a configuration")
    delete_parser.add_argument("--name", help="Configuration name", required=True)

    list_parser = config_subparsers.add_parser("list", help="list all configurations")

    config_parser = subparsers.add_parser("help")

    return parser.parse_args()

def main():
    args = parse_args()
    app = IOXCLI()


    if args.command == 'sql':
        app.do_sql(args.query)
    if args.command == 'influxql':
        app.do_influxql(args.query)
    if args.command == 'write':
        app.do_write(args.line_protocol)
    if args.command == 'write_csv':
        app.do_write_csv(args)
    if args.command == 'config':
        if args.config_command == 'create':
            app.create_config(args)
        elif args.config_command == 'delete':
            app.delete_config(args)
        elif args.config_command == 'list':
            app.list_config(args)
        elif args.config_command == 'update':
            app.update_config(args)
        elif args.config_command == 'use':
            app.use_config(args)
        else:
             print(_usage_string)
    if args.command == 'help':
        print(_usage_string)
    if args.command is None:
        app.cmdloop()
    

if __name__ == '__main__':
    main()

