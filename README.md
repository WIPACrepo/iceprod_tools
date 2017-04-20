# iceprod_tools

## Example Usage

1. Import RPC class
```
from rpc import RPC
```
2. Create an rpc instance using the server's URL
```
rpc = RPC('http://localhost:8888')
```
3. Now you can call remote functions directly on the rpc object. E.g.
```
datasets = rpc.get_datasets_by_status('processing')
```
