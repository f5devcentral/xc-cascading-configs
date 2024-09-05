
class Model():
    def __init__(self):
        self.errorLogs = []
        self.namespace = 'shared'
        self.output = ''
        
    def parse(self, inputJson, name):
        try:
            if 'spec' not in inputJson:
                self.errorLogs.append('Model parse No spec found in given data JSON, cannot build model')
                return
            d = inputJson['spec']

            self.output = {'metadata': {
                        'name': name,
                        'namespace': 'shared',},
                   'spec' : d}
        
        except Exception as e:
            self.errorLogs.append('Model parse caught error: {}'.format(e))
            return
        
        