import json

from probe.childTenants import ChildTenants
from probe.generic import Generic

class Probe(Generic, ChildTenants):
    def __init__(self, log, config, client):
        super().__init__()
        self.log = log
        self.config = config
        self.client = client
        self.MTbase = '/managed_tenant'
        if self.config.accessType == 'MSP':
            self.PARENT_API = '/api/web/namespaces/system/partner-management/child_tenants'
        else:
            self.PARENT_API = '/api/web/namespaces/system/managed_tenants_list'
        self.tenants = []

    def putWrapper(self, path, data):
        return self.httpWrapper(path, 'PUT', data)
        
    def putWrapperWithDict(self, path, data):
        return self.httpWrapper(path, 'PUT', json.dumps(data))
    
    def postWrapper(self, path, data):
        return self.httpWrapper(path, 'POST', data)
        
    def postWrapperWithDict(self, path, data):
        return self.httpWrapper(path, 'POST', json.dumps(data))
        
    def getWrapper(self, path, returnCodeOnly=False):
        return self.httpWrapper(path, 'GET', None, returnCodeOnly)
    
    def httpWrapper(self, path, method=None, data=None, returnCodeOnly=False):
        input = 'path: {} method: {} data: {}'.format(path, method, data)
        
        r = None
        if method is None:
            self.log.debug('no method given to httpWrapper: input: {}'.format(input))
            return
        
        try:
            if method == 'GET':
                r = self.client.call('GET', path)
            elif method == 'POST':
                r = self.client.call('POST', path, {}, data)
            elif method == 'PUT':
                r = self.client.call('PUT', path, {}, data)
            else:
                self.log.error('Unsupported method to httpWrapper. method: {}'.format(method))
                return
            
            if r is None:
                self.log.debug('given resp is empty: input: {}'.format(input))
                return 
            
            if returnCodeOnly == True:
                return r.status_code
            
            if r.status_code != 200:
                self.log.debug('Received a non 200 error code. Error: {} resp: {} input: {}'.format(r.status_code, r.text, input))
                return

            data = r.json()
            return data
        
        except Exception as e:
            self.log.error('httpWrapper error {} input: {}'.format(e, input))
    