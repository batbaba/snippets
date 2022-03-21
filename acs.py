# %%
#!/usr/bin/python3

from cgitb import reset
import sys
import re
import os
from unittest.mock import patch

search=sys.argv[1].upper()
path=os.path.expanduser('~')+"/.aws/config"

with open(path) as f:
    content = f.readlines()
accounts=''.join(content)
myarray=[]


# %%
def main():
    for account in re.split("\[profile ",accounts):
        if account!='':
            account = account.replace("]", "")
            accountTolist=account.split('\n')
            mydict={'ProfileName': accountTolist[0].strip(),'AccountName':accountTolist[3].split('=')[1].strip(),'AccountId':accountTolist[4].split('=')[1].strip()}
            myarray.append(mydict)

    for item in myarray:
        for value in item.values():
            if search in value.upper():
                print("============================")
                for k, v in item.items():
                    print(k,"\t",v)
                break

main()
# %%
