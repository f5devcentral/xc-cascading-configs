import json
import os

class Config(): 
    def __init__(self, log):
        self.data = None
        self.log = log
        self.apiToken = ""
        self.retryCount = 2
        self.requestsLimit = 500
        self.overwrite = False
        self.debug = False
        self.host = ""
        self.verifySSL = True
        self.accessType = "MSP" # defaults to MSP, can be set to "DA" for direct access
        self.configTypes = {
            'app_firewall' : '/api/config/namespaces/shared/app_firewalls', 
            'service_policy' : '/api/config/namespaces/shared/service_policys', 
            'log_receiver' : '/api/config/namespaces/shared/global_log_receivers',
            'app_type' : '/api/config/namespaces/shared/app_types',
            'forward_proxy_policys' :'/api/config/namespaces/shared/forward_proxy_policys',
            'rate_limiter_policys' : '/api/config/namespaces/shared/rate_limiter_policys',
            'network_policys' : '/api/config/namespaces/shared/network_policys',
            'rate_limiter' : '/api/config/namespaces/shared/rate_limiters',
            'alert_receivers' : '/api/config/namespaces/shared/alert_receivers',
            'ip_prefix_sets' : '/api/config/namespaces/shared/ip_prefix_sets'
             }
        
        
        
        
        
        self.configType = '' # provided on script run time
        self.namedConfig = '' # provided on script run time
        self.namedConfigJSON = '' # file path to named config JSON, used instead of namedConfig
        self.childTenants = '' # provided on script run time
        self.criticalErrorCount = 0

    def readFile(self, configFile):
        if bool(os.path.isfile(configFile)) == False:
            self.log.error('{} does not exist'.format(configFile))
            return
        f = open(configFile)
        try:
            self.data = json.load(f)
        except Exception as e:
            self.log.error('json convert with error: {}'.format(e))
            f.close()
            return
        
        f.close()
        
        self.processConfig()
        
    def processConfig(self):
        if self.data is None or len(self.data) < 1:
            self.log.error('no Config content present')
            return
        
        for k, v in self.data.items():
            if k == 'RequestsLimit':
                self.requestsLimit = v
            elif k == 'RetryCount':
                self.retryCount = v
            elif k == 'APIToken':
                self.apiToken = v
            elif k == 'Debug':
                self.debug = v
            elif k == 'Host':
                self.host = v
            elif k == 'VerifySSL':
                self.verify_ssl = v
            elif k == 'Overwrite':
                self.overwrite = v
            elif k == 'AccessType':
                if v == 'MSP' or v == 'DA':
                    self.accessType = v
                else:
                    self.log.error('Unsupported Access Type of {} given.'.format(v))
                    self.criticalErrorCount += 1
                            
            else:
                self.log.error("Provided Config Option {} is not currently supported".format(k))
            
