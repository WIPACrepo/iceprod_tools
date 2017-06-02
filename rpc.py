import requests
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

