import requests

def chatbotAI(api_key, api_url, message):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ],
        "model": "deepseek/deepseek-v3-0324",
    }

    response = requests.post(api_url, headers=headers, json=payload)

    # Kiểm tra nếu yêu cầu thành công
    if response.status_code == 200:
        message = response.json()["choices"][0]["message"]["content"]
        return f"__Answer__:\n\n{message}", "OK"
    else:
        return f"Error: {response.status_code} - {response.text}", "ERROR"
