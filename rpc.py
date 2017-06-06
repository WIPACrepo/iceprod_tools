import requests

# Copied from iceprod/server/__init__.py
class GlobalID(object):
    """Global ID configuration and generation"""
    import string
    # never change these settings, otherwise all old ids will fail
    CHARS = string.ascii_letters+string.digits
    CHARS_LEN = len(CHARS)
    # define dict to make reverse lookup super fast
    INTS_DICT = {c:i for i,c in enumerate(CHARS)}
    IDLEN = 15
    MAXSITEID = 10**10
    MAXLOCALID = 10**15

    @classmethod
    def int2char(cls,i):
        if not isinstance(i,(int,long)) or i < 0: # only deal with positive ints
            logging.warn('bad input to int2char: %r',i)
            raise Exception('bad input to int2char')
        out = ''
        while i >= 0:
            out += cls.CHARS[i%cls.CHARS_LEN]
            i = i//cls.CHARS_LEN - 1
        return out[::-1]

    @classmethod
    def char2int(cls,c):
        if not isinstance(c,basestring) or len(c) < 1: # only deal with string
            logging.warn('bad input to char2int: %r',c)
            raise Exception('bad input to char2int')
        out = -1
        for i,cc in enumerate(reversed(c)):
            if cc not in cls.CHARS:
                raise Exception('non-char input to chars2int')
            out += (cls.INTS_DICT[cc]+1)*(cls.CHARS_LEN**i)
        return out

    @classmethod
    def siteID_gen(cls):
        """Generate a new site id"""
        import random
        return cls.int2char(random.randint(0,cls.MAXSITEID-1))

    @classmethod
    def globalID_gen(cls,id,site_id):
        """Generate a new global id given a local id and site id"""
        if isinstance(id,basestring):
            id = cls.char2int(id)
        elif not isinstance(id,(int,long)):
            raise Exception('id is not a string, int, or long')
        if isinstance(site_id,basestring):
            return cls.int2char(cls.char2int(site_id)*cls.MAXLOCALID+id)
        elif isinstance(site_id,(int,long)):
            return cls.int2char(site_id*cls.MAXLOCALID+id)
        else:
            raise Exception('Site id is not a string, int, or long')

    @classmethod
    def localID_ret(cls,id,type='str'):
        """Retrieve a local id from a global id"""
        ret = cls.char2int(id) % cls.MAXLOCALID
        if type == 'str':
            ret = cls.int2char(ret)
        return ret

    @classmethod
    def siteID_ret(cls,id,type='str'):
        """Retrieve a site id from a global id"""
        ret = cls.char2int(id) // cls.MAXLOCALID
        if type == 'str':
            ret = cls.int2char(ret)
        return ret

class RPC:
    def __init__(self, server_address):
        self.id = 0
        self.server_address = server_address
    def __call__(self, method, **params):
        self.id += 1
        data = {'jsonrpc':'2.0','method':'public_' + method,'id':self.id}
        if params != None: data['params'] = params
        r = requests.post(self.server_address + '/jsonrpc', json=data)
        if r.status_code >= 400: 
            raise Exception('HTTP request error %i' % r.status_code)
        return r.json()['result']

    def get_number_of_tasks_in_each_state(self):
        return self('get_number_of_tasks_in_each_state')
    def get_datasets_by_status(self, status):
        return self('get_datasets_by_status', status=status)
    def get_config(self, dataset_id):
        return self('get_config', dataset_id=dataset_id)
    def get_task_walltime(self, task_id):
        return self('get_task_walltime', task_id=task_id)
    def get_task_ids(self, dataset_id):
        return self('get_task_ids', dataset_id=dataset_id)
    def get_task_stats(self, task_id):
        return self('get_task_stats', task_id=task_id)
    def get_dataset_description(self, dataset_id):
        return self('get_dataset_description', dataset_id=dataset_id)
    def get_dataset_steering(self, dataset_id):
        return self('get_dataset_steering', dataset_id=dataset_id)
    def get_tasks_by_name(self, task_name):
        return self('get_tasks_by_name', task_name=task_name)
    def get_tasks_by_requirements(self, task_reqirements):
        return self('get_tasks_by_requirements', task_reqirements=task_reqirements)
    def get_dataset_completion(self, dataset_id):
        return self('get_dataset_completion', dataset_id=dataset_id)
    def dataset_number(self, dataset_id):
        return GlobalID.localID_ret(dataset_id,type='int')
