import model.model
import json

class Generic():
    def __init__(self):
        self.logModel = None

    def setDetails(self, baseAPI, objectName):
        self.baseAPI = baseAPI
        self.objectName = objectName

    def getRootObject(self):
        rootAPI = '{}/{}?response_format=GET_RSP_FORMAT_FOR_CREATE'.format(self.baseAPI, self.config.namedConfig)
        try:    
            if len(self.config.namedConfigJSON) == 0:
                r = self.getWrapper(rootAPI)
                if r is None:
                    self.log.debug('response is None for getRootObject get with url: {}'.format(rootAPI))
                    return
                
                self.logModel = model.model.Model()
                self.logModel.parse(r['create_form'], self.config.namedConfig )
    
                return self.logModel.output
            
        except Exception as e:
            self.log.error('getRootObject: url: {} error: {}'.format(rootAPI, e))
            
        try:
            f = open(self.config.namedConfigJSON)
            d = json.load(f)
            f.close()
            
            self.logModel = model.model.Model()
            self.logModel.parse(d, self.config.namedConfig )
            
            return self.logModel.output
            
        except Exception as e:
            self.log.error('getRootObject: configJSON: {} error: {}'.format(self.config.namedConfigJSON, e))
        
            
    def doesChildObjectExist(self, childTenant):
        childObjectAPI = '{}/{}{}/{}'.format(self.MTbase, childTenant, self.baseAPI, self.config.namedConfig) 
        
        try:    
            r = self.getWrapper(childObjectAPI, returnCodeOnly=True)
            if r is None:
                self.log.debug('response is None for doesChildObjectExist with url: {}'.format(childObjectAPI))
                return

            if r == 200:
                return True
            else:
                return False
            
        except Exception as e:
            self.log.error('doesChildObjectExist: url: {} error: {}'.format(childObjectAPI, e))
        
    def writeChildObject(self, childTenant, rootConfig):
        if self.logModel is None or len(self.logModel.errorLogs) > 0:
            self.log.error('errors in Model, cannot continue')
            return
        
        # check if exists first
        exists = self.doesChildObjectExist(childTenant)

        childObjectAPI = '{}/{}{}'.format(self.MTbase, childTenant, self.baseAPI) 
        childOverwriteObjectAPI = '{}/{}{}/{}'.format(self.MTbase, childTenant, self.baseAPI, self.config.namedConfig) 
    
        try:
            if self.config.overwrite == True and exists == True:
                r = self.putWrapperWithDict(childOverwriteObjectAPI, rootConfig)
            elif self.config.overwrite == False and exists == True:
                return
            else:    
                r = self.postWrapperWithDict(childObjectAPI, rootConfig)
            if r is None:
                self.log.debug('response is None for writeChildObject post with url: {}'.format(childObjectAPI))
                return
          
        except Exception as e:
            self.log.error('writeChildObject post: url: {} error: {}'.format(childObjectAPI, e))
                    
        