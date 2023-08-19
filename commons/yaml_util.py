import os

import yaml


# 写入
def write_yaml(data):
    with open(os.getcwd()+"/extract.yaml",encoding="utf-8",mode="a+") as f:
        yaml.dump(data,stream=f,allow_unicode=True)


# 读取
def read_yaml(key):
    with open(os.getcwd()+"/extract.yaml",encoding="utf-8",mode="r") as f:
        value = yaml.load(f,yaml.FullLoader)
        return value[key]


# 清除
def clear_yaml():
    with open(os.getcwd()+"/extract.yaml",encoding="utf-8",mode="w") as f:
        f.truncate()

# 读取测试用例yaml文件
def read_testcase_yaml(yaml_name):
    with open(os.getcwd()+"/testcases"+yaml_name,mode='r',encoding='utf-8') as f:
        value = yaml.load(stream=f,Loader=yaml.FullLoader)
        return value
