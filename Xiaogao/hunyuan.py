import requests
import json


# 定义 API 的 URL
url = 'https://yuanqi.tencent.com/openapi/v1/agent/chat/completions'

# 定义请求头
headers = {
    'X-Source': 'openapi',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer dgAEvlwsfAemO8iIovstprFI7MEdZvT3'
}

# 定义请求体
data = {
    "assistant_id": "WhoIc3Q07Q5q",
    "user_id": "100041232419",
    "stream": False,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "你是谁？"
                }
            ]
        }
    ]
}

# 将请求体转换为 JSON 格式的字符串
json_data = json.dumps(data)

# 发送 POST 请求
# response = requests.post(url, headers=headers, json=data)  # 使用 json 参数自动设置正确的 Content-Type

test={"id":"82b4814a4abf1c15a3991b0187f4aabc","created":1740969837,"choices":[{"finish_reason":"stop","message":{"role":"assistant","content":"（笑着挥挥手）嘿，我是小高呀！一个超级热爱生活，喜欢尝试新鲜事物的人哦！美食、运动、旅行，啥都喜欢！而且啊，我还特别喜欢跟人聊天，总能找到有趣的话题，让咱们聊得开心又愉快！","steps":[{"role":"assistant","content":"（笑着挥挥手）嘿，我是小高呀！一个超级热爱生活，喜欢尝试新鲜事物的人哦！美食、运动、旅行，啥都喜欢！而且啊，我还特别喜欢跟人聊天，总能找到有趣的话题，让咱们聊得开心又愉快！","usage":{"prompt_tokens":74,"completion_tokens":48,"total_tokens":122},"time_cost":8678}]}}],"assistant_id":"WhoIc3Q07Q5q","usage":{"prompt_tokens":74,"completion_tokens":48,"total_tokens":122}}

# 打印响应内容
# print(response.text)
# print(test["choices"][0]["message"]["content"])