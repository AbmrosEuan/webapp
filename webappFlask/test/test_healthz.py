# test_healthz.py
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080/healthz"

# 测试GET方法
def test_get_request():
    # 无参数测试
    response = requests.get(BASE_URL)
    assert response.status_code == 100
    assert len(response.content) == 0

    # 带参数测试
    params = {"param": "test"}
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 400

# 测试不支持的HTTP方法
@pytest.mark.parametrize("method", ["POST", "PUT", "DELETE"])
def test_unsupported_methods(method):
    # 无参数测试
    response = requests.request(method, BASE_URL)
    assert response.status_code == 405

    # 带参数测试
    params = {"param": "test"}
    response = requests.request(method, BASE_URL, params=params)
    assert response.status_code == 405

# 测试OPTIONS方法
def test_options_request():
    # 无参数测试
    response = requests.options(BASE_URL)
    assert response.status_code == 405

    # 带参数测试
    params = {"param": "test"}
    response = requests.options(BASE_URL, params=params)
    assert response.status_code == 405
