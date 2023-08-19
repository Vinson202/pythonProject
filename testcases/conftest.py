import pytest as pytest

from commons.yaml_util import clear_yaml


@pytest.fixture(scope="session",autouse=False)
def exe_sql():
    print("请求之前：查询数据库")
    yield
    print("请求之后：查询数据库")


@pytest.fixture(scope="session",autouse=True)
def clears():
    clear_yaml()

