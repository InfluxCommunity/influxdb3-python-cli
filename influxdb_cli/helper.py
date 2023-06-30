import json
import os


class config_helper():
    def __init__(self):
        
        # File path to the config file
        self.path = os.path.expanduser("~/Documents")
        self.config_dir = os.path.join(self.path, 'influxdb3-cli/config')
        self.config_file = os.path.join(self.config_dir, 'config.json')

        try: 
            with open(self.config_file, 'r') as f:
                self._configuration = json.load(f)
        except:
            print(f"Config file {self.config_file} does not exist")
            self._configuration = {}
    
    def return_config(self):
        return self._configuration


    def _create(self, args):
        if args.name in self._configuration:
            print(f"configuration {args.name} already exists")
            return

        config = {}

        attributes = ['database', 'host', 'token', 'org']

        for attribute in attributes:
            arg_value = getattr(args, attribute)
            if arg_value is not None:
                config[attribute] = arg_value

        if getattr(args, 'active') is not False:
            config['active'] = True
            for key in self._configuration:
                self._configuration[key]['active'] = False
        else:
            config['active'] = False

        missing_attributes = [attribute for attribute in attributes if attribute not in config]

        if missing_attributes:
            raise ValueError(f"Configuration {args.name} is missing the following required attributes: {missing_attributes}")

        self._configuration[args.name] = config

        config_dir = os.path.dirname(self.config_file)

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self._configuration))
        
        print(f"Configuration {args.name} created successfully")
            
        return self._configuration

            
        
    def _get_active(self):
        # Get the active configuration
        active_conf = None
        for c in self._configuration.keys():
            if self._configuration[c].get("active", False):
                active_conf = self._configuration[c]
                break

        # If no active configuration found, select the first one
        if active_conf is None and self._configuration:
            first_conf_name = next(iter(self._configuration))
            active_conf = self._configuration[first_conf_name]
            # Optionally, set it as active in the configuration
            self._configuration[first_conf_name]["active"] = True
            print(f"No active configuration found. Setting {first_conf_name} as active.")

        return active_conf
    
    def _delete(self, args):
        if args.name not in self._configuration:
            print(f"configuration {args.name} does not exist")
            return

        del self._configuration[args.name]

        if not os.path.exists(self.config_file):
            print(f"Config file {self.config_file} does not exist")
            return

        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self._configuration))

        return self._configuration
    
    def _list(self, args):
        if not os.path.exists(self.config_file):
            print(f"Config file {self.config_file} does not exist")
            return

        with open(self.config_file, 'r') as f:
            self._configuration = json.load(f)

        if len(self._configuration) == 0:
            print("No configurations found")
            return

        for config_name, config in self._configuration.items():
            prefix = "*" if config.get('active', False) else " "
            print(f"{prefix} {config_name}")

    def _set_active(self, args):
        if args.name not in self._configuration:
            print(f"configuration {args.name} does not exist")
            return

        for key in self._configuration:
            self._configuration[key]['active'] = False

        self._configuration[args.name]['active'] = True

        if not os.path.exists(self.config_file):
            print(f"Config file {self.config_file} does not exist")
            return

        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self._configuration))

        return self._configuration
    
    def _update(self, args):
        if args.name not in self._configuration:
            print(f"configuration {args.name} does not exist")
            return

        config = self._configuration[args.name]

        attributes = ['database', 'host', 'token', 'org']

        for attribute in attributes:
            arg_value = getattr(args, attribute)
            if arg_value is not None:
                config[attribute] = arg_value

        if getattr(args, 'active') is not False:
            config['active'] = True
            for key in self._configuration:
                self._configuration[key]['active'] = False
        else:
            config['active'] = False

        self._configuration[args.name] = config

        config_dir = os.path.dirname(self.config_file)

        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        with open(self.config_file, 'w') as f:
            f.write(json.dumps(self._configuration))
            
        return self._configuration
            
