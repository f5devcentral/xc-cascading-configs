import requests    
from threading import Thread, Lock
import time
import sys

class Client():
    def __init__(self, log, config):
        self.rpm = 0
        self.mutex = Lock()
        self.log = log
        self.config = config
        
        self.runBackgroundCleanRPM = True
        daemon = Thread(target=self.cleanRPM, daemon=True, name='cleanRPM')
        daemon.start()
        
        # stop background threads on exit
    def __del__(self):
        self.runBackgroundCleanRPM = False
        time.sleep(1)
        
    def getRunBackgroundCleanRPM(self):
        return self.runBackgroundCleanRPM
        
    # Reset RPM to zero every minute
    def cleanRPM(self):
        while self.getRunBackgroundCleanRPM():
            time.sleep(60)
            self.log.debug('setting RPM back to zero')
            self.mutex.acquire()
            self.rpm = 0
            self.mutex.release()
            
    def checkRPM(self, retry=0):
        if self.rpm < self.config.requestsLimit:
            self.mutex.acquire()
            self.rpm += 1
            self.mutex.release()
            return
        if retry > 6:
            self.log.error('After a minute still not allowed to send request, something is likely wrong with reset of RPM')
            sys.exit(1)
        self.log.debug('Pausing API calls until RPM is reset')
        time.sleep(10)
        retry += 1
        self.checkRPM(retry)
        
    def call(self, method, path, headers={}, payload=None, attempt=0):
        if attempt > self.config.retryCount:
            self.log.error('No more retries allowed for path: {}'.format(path))
            return
        
        if method not in ['GET', 'POST', 'PUT']:
            self.log.error('Invalid method given {}'.format(method))
            return
       
       # blocking until allowed to call request
        self.checkRPM()
       
        url = '{}{}'.format(self.config.host, path)
        self.log.debug('URL in client: {}'.format(url))
        
        headers["content-type"] = "application/json"
        headers["Authorization"] = "APIToken {}".format(self.config.apiToken)
        
        response = requests.request(method, url, headers=headers, data=payload, verify=self.config.verifySSL)
        
        if response.status_code in [429, 502, 503, 504]:
            attempt += 1
            self.log.debug('Request for path: {} failed with code: {} starting retry attempt: {}'.format(path, response.status_code, attempt))
            self.call(method, path, headers, payload, attempt)
            
        return response

