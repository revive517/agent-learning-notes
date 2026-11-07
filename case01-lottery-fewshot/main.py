'''
有如下5条文本，需要抽取信息：
1. 2025年第100期，开好红球22 21 06 01 03 11 篮球 07， 一等奖中奖为2注。
2. 2025101期，有3注1等奖，10注2等奖，开号篮球11，中奖红球3、5、7、11、12、16。
期待经过通过模型抽取信息得到如下结果：
1. {"期数":"2025100","中奖号码":[1,3,6,11,21,22,7],"一等奖":"2注"}
2. {"期数":"2025101","中奖号码":[3,5,7,11,12,16,11],"一等奖":"3注"}
请设计Prompt,基于FewShot，对模型做示例的提示，得到需要的结果。
'''
from openai import OpenAI
import json

client = OpenAI(
    base_url="https://ws-kxxqiuowiuke0uzn.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"   #调接口
)

#这里需要先定义一个schema去定义一个要抽取的属性
schema = ['期数','中奖号码','一等奖']
example_data = [  #这里是给的示例
    {
        "content":f"2025年第100期，开好红球22 21 06 01 03 11 篮球 07， 一等奖中奖为2注",
        "answers":{
            "期数":"2025100",
            "中奖号码":[1,3,6,11,21,22,7],
            "一等奖":"2注"
        }
    },
    {
        "content":f"2025101期，有3注1等奖，10注2等奖，开号篮球11，中奖红球3、5、7、11、12、16",
        "answers":{
            "期数":"2025101",
            "中奖号码":[3,5,7,11,12,16,11],
            "一等奖":"3注"
        }
    }
]

questions = [
    {"content":f"2025102期，开好红球09 04 17 25 02 13，篮球09，一等奖中奖为4注"},
    {"content":f"2025103期，15注2等奖，开号篮球03，中奖红球04、08、10、14、19、23"}
]

#这里开始规定系统角色，规范message  这里是一个列表中嵌套字典
messages = [
    {"role":"system","content":f"帮我按照{schema}对应去抽取文本中的三个信息，按JSON字符串格式进行输出，如果某些信息不存在，请用'原文未提及'来做表示，有以下可参考的示例"}
]

#接下来是要做这个补全这message，通过追加列表的方式来做添加,使用循环的方式来添加user以及assistant的对应描述
for example in example_data:
    messages.append(
        #这个地方要追加字典类型的 user
        {"role":"user","content":example["content"]}
    )
    #这个地方要追加字典类型的assistant,这里需要注意一下这个格式的输出是要按照JSON字符串的格式要输出，所以需要吧字典类型转化为字符串的类型作为输出
    messages.append(
        {"role":"assistant","content":json.dumps(example["answers"],ensure_ascii=False)}
    )

'''
#现在这里做一个messages的输出检查
for x in messages:
    print(x)
'''

#这里需要做的就是对用户所提的问题进行解答，要注入到messages中，这里需要循环用户的问题questions
for q in questions:
    response = client.chat.completions.create(   #要这样去提问
        model="qwen3.8-max",
        messages=messages + [{"role":"user","content":f"下面我给你几个文本，请参照以上示例，来对应抽取文本{q["content"]}的信息"}]  #这里做的是对于两个列表的加和
    )

    print(response.choices[0].message.content)
