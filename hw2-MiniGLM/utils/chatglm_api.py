import zhipuai
import json

zhipuai.api_key = ""


text = '''请问《天龙八部》主要讲了什么故事？'''

response = zhipuai.model_api.invoke(
    model="chatglm_pro",
    prompt=[
        {"role": "user", "content": text},
    ],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1000,
)
