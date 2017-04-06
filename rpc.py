import requests
class RPC:
    def __init__(self, server_address):
        self.id = 0
        self.server_address = server_address
    def __call__(self, method, params=None):
        self.id += 1
        data = {'jsonrpc':'2.0','method':'public_' + method,'id':self.id}
        if params != None: data['params'] = params
        r = requests.post(self.server_address + '/jsonrpc', json=data)
        return r.json()['result']

    def get_number_of_tasks_in_each_state(self):
        return self('get_number_of_tasks_in_each_state')
    def get_datasets_by_status(self, status):
        return self('get_datasets_by_status', {'status': status})
    def get_config(self, dataset_id):
        return self('get_config', {'dataset_id': dataset_id})

    def get_task_runtime(self, task_id):
        pass
    def get_task_ids(self, dataset_id):
        pass
    def get_task_stats(self, task_id):
        pass