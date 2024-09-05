# xc-cascading-configs
A Tool that enables F5 Distributed Cloud Managed Service Provider customers or customers with Delegated Access to push and maintain shared configurations to all/any of their Child Tenants. Either Delegated Access or Managed Service Provider (MSP) configuration is required to use this tool. For customers that manage multiple Child Tenants, this tool help deploy and maintain shared configurations between all Child Tenants. The tool can push out a configuration object from either the root tenant itself or from a local JSON file. The user of this tool can decide if Child Tenant configurations should be overwritten on config sync. A successful run will have no error messages. Users can check Child Tenants for confirmation the configuration was deployed. 

## Install 
1. Create a Python Virtual Environment.
   `python3 -m venv config-venv`
2. Source the new environment.
    `source config-venv/bin/activate`
3. Install required python modules.
   `python3 -m pip install -r requirements.txt`

## Config Setup Instructions

1. Ensure either Delegated Access or Managed Service Provider (MSP) is configured. This tool is intended for customers that manage multiple Child Tenants. 

Delegated Access:
https://docs.cloud.f5.com/docs-v2/delegated-access/how-tos/manage-delegated-access

Managed Service Provider  (MSP):
https://docs.cloud.f5.com/docs-v2/administration/how-tos/managed-services/config-tenant-msp-service


2. Create an API Token for the Root Tenant. 
   Sign into the F5 XC Console with Administrative privileges and navigate to Administration. Under 'Personal Management' select 'Credentials'. Then click 'Add Credentials' and populate the window. Make sure to select 'API Token' as the 'Credential Type' field. Save the generated API Token for the next step.

3. Create a configuration file.
   Under the 'config' directory, create a JSON file. Below is a sample file. Make sure to populate the correct F5 XC Console URL and API Token created in step 1. 'AccessType' defaults to MSP but can be set to 'DA' for direct access. 
```
{
    "Host" : "https://tenant-name.volterra.io",
    "APIToken" : "APITOKEN-Goes-Here",
    "VerifySSL" : false,
    "RequestsLimit" : 1000,
    "RetryCount" : 2,
    "Overwrite": true,
    "AccessType" : "MSP"
}
```


## Run Examples
First, source the virtual environment.
    `source config-venv/bin/activate`

### List Child Tenants
Listing all Child Tenants is a good way to confirm the API Token is correct and MSP or DA access is setup correctly.

`python3 config-sync/config-sync.py --config config/prod-config.json --listChildTenants`

['f5-msp-eu', 'f5-msp-uk', 'f5-msp-india', 'f5-msp-na', 'msp-customer-3']

### List Supported Config Types
To view the supported Config Types the tool can replicate to Child Tenants, run the command below.

`python3 config-sync/config-sync.py --config config/prod-config.json --listTypes`
```
{'alert_receivers': '/api/config/namespaces/shared/alert_receivers',
 'app_firewall': '/api/config/namespaces/shared/app_firewalls',
 'app_type': '/api/config/namespaces/shared/app_types',
 'forward_proxy_policys': '/api/config/namespaces/shared/forward_proxy_policys',
 'ip_prefix_sets': '/api/config/namespaces/shared/ip_prefix_sets',
 'log_receiver': '/api/config/namespaces/shared/global_log_receivers',
 'network_policys': '/api/config/namespaces/shared/network_policys',
 'rate_limiter': '/api/config/namespaces/shared/rate_limiters',
 'rate_limiter_policys': '/api/config/namespaces/shared/rate_limiter_policys',
 'service_policy': '/api/config/namespaces/shared/service_policys'}
```

### Replicate Global Log Receiver to all Child Tenants
This example syncs a config object stored in the root tenant, named 'global-template' to all Child Tenants. 

`python3 config-sync/config-sync.py --config config/prod-config.json --configType log_receiver --namedConfig 'global-template'`

### Replicate Global Log Receiver to specific Child Tenant
This example does the same as the previous example except it will only deploy the configuration to the listed Child Tenants. 

`python3 config-sync/config-sync.py --config config/prod-config.json --configType log_receiver --namedConfig 'root-test' --childTenants 'f5-msp-eu'`


### Replicate local Log Receiver to all Child Tenants
This example shows using a local JSON configuration for the object. This is helpful if a code repository is used to maintain global configs. The file could be stored in the code repository and on file change a pipeline runner could execute a variation of the command below to push the changes.

`python3 config-sync/config-sync.py --config config/prod-config.json --configType log_receiver --namedConfigJSON config/log-root.json --namedConfig 'root-test'`


The location configuration was acquired from the F5 XC console. When editing an object, there is a JSON tab. Below is an example of a log receiver object. 

```
{
    "spec": {
        "ns_current": {},
        "http_receiver": {
            "uri": "https://f5.com/rocks",
            "auth_none": {},
            "compression": {
                "compression_none": {}
            },
            "batch": {
                "timeout_seconds_default": {},
                "max_events_disabled": {},
                "max_bytes_disabled": {}
            },
            "no_tls": {}
        },
        "request_logs": {}
    }
}
```

### Replicating other objects
Below are examples of the other supported configuration Types as of the initial release of the tool. Make sure to use the 'listTypes' object to see any newly supported configurations.

`python3 config-sync/config-sync.py --config config/prod-config.json --configType app_type --namedConfig 'agility' --childTenants 'f5-msp-eu'`

`python3 config-sync/config-sync.py --config config/prod-config.json --configType forward_proxy_policys --namedConfig 'root-test' --childTenants 'f5-msp-eu'`

`python3 config-sync/config-sync.py --config config/prod-config.json --configType rate_limiter_policys --namedConfig 'root-test' --childTenants 'f5-msp-eu'`

`python3 config-sync/config-sync.py --config config/prod-config.json --configType network_policys --namedConfig 'root-test' --childTenants 'f5-msp-eu'`

`python3 config-sync/config-sync.py --config config/prod-config.json --configType alert_receivers --namedConfig 'root-test' --childTenants 'f5-msp-eu'`

`python3 config-sync/config-sync.py --config config/prod-config.json --configType rate_limiter --namedConfig 'root-test' --childTenants 'f5-msp-eu'`

`python3 config-sync/config-sync.py --config config/prod-config.json --configType ip_prefix_sets --namedConfig 'ryan-bot-test' --childTenants 'f5-msp-eu'`

