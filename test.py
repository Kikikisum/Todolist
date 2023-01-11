import requests

# url = "http://127.0.0.1:5000/add"
# data = {
#     "id": "2",
#     "title": "测试",
#     "content": "哈哈哈",
#     "state": "完成",
#     "end_time": "2023-01-10 23:08:32",
#
# }

# url = "http://127.0.0.1:5000/accomplish"
# data = {
#     "id": "2",
# }

url = "http://127.0.0.1:5000/delete"
data = {
    "id": "2",
}
res = requests.post(url, json=data)
print(res.text)