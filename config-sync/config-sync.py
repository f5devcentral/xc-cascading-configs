import argparse
import config
import sys
import runner
from pprint import pprint

sys.path.append('/../')

import utils.logger as logger

def main():

    parser = argparse.ArgumentParser(description="msp-config-sync")
    parser.add_argument('--logFile', default='config-sync.log', help='Log file, default is config-sync.log')
    parser.add_argument('--config', default='config/config.json', help='Config file location, defaults to config/config.json')
    parser.add_argument('--listTypes', action='store_true', help='Lists all available Config Types')
    parser.add_argument('--listChildTenants', action='store_true', help='Lists all available Child Tenants')
    parser.add_argument('--configType', default='', help='Which Config Type to replicate')
    parser.add_argument('--namedConfig', default='', help='Named Config to replicate to child tenants')
    parser.add_argument('--namedConfigJSON', default='', help='Local Named Config JSON file path to replicate to child tenants')
    parser.add_argument('--childTenants', default='all', help='Child Tenant(s) to replicate config to. Defaults to all. Multiples supported with comma separation.')
    args = parser.parse_args()

    log = logger.Log('Config-Sync', args.logFile)
    cfg = config.Config(log)
    cfg.readFile(args.config)
    if cfg.criticalErrorCount != 0:
        log.critical('Error creating config, cannot continue')
   
    if bool(args.listTypes) == True:
        pprint(cfg.configTypes)
        return
    
    cfg.configType = args.configType
    cfg.namedConfig = args.namedConfig
    cfg.namedConfigJSON = args.namedConfigJSON
    cfg.childTenants = args.childTenants
    
    r = runner.Runner(log, cfg)
    if bool(args.listChildTenants) == True:
        children = r.listChildTenants()
        print(children)
        return
    else:
        r.run()
    
if __name__ == "__main__":
    main()