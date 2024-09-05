import client
import probe.probe as probe

class Runner():
    def __init__(self, log, config):
        self.log = log
        self.config = config
        self.client = client.Client(self.log, self.config)

    def listChildTenants(self):
        p = probe.Probe(self.log, self.config, self.client)
        p.getChildren()
        return p.tenants
        
    def run(self):
        children = self.getChildTenants()
        if self.config.configType not in self.config.configTypes:
            self.log.critical('Config Type: {} not supported'.format(self.config.configType)
                              )
        p = probe.Probe(self.log, self.config, self.client)

        p.setDetails(self.config.configTypes[self.config.configType], self.config.configType)

        rootConfig = p.getRootObject()
        for ct in children:
            p.writeChildObject(ct, rootConfig)
        
    def getChildTenants(self):
        if self.config.childTenants == 'all':
            return self.listChildTenants()
        if ',' in self.config.childTenants:
            parts = self.config.childTenants.split(',')
            return parts
        return [self.config.childTenants]