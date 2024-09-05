
class ChildTenants():
    def getChildren(self):
        self.getChildrenOneLevel(self.PARENT_API)
        for t in self.tenants:
            self.getChildrenOneLevel('{}/{}{}'.format(self.MTbase, t, self.PARENT_API))

    def getChildrenOneLevel(self, url):
        try:    
            r = self.getWrapper(url)
            if r is None:
                self.log.debug('response is None for getChildrenOneLevel with url: {}'.format(url))
                return
            
            if 'access_config' not in r:
                self.log.error('Unable to get MT children: response: {}'.format(r))
                return
            
            for mt in r['access_config']:
                if 'name' in mt:
                    nameParts = mt['name'].split('-')
                    if len(nameParts) > 1:
                        # remove last position, API adds extra id to end of name
                        myName = '-'.join(nameParts[0:-1])
                    else:
                        myName = mt['name']
                    self.tenants.append(myName)
            
        except Exception as e:
            self.log.error('getChildrenOneLevel: url: {} error: {}'.format(url, e))