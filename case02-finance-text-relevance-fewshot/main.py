'''
金融文本的匹配
首先，需要构造几个文本对：
1.('股票市场今日大涨，投资者乐观。','持续上涨的时长让投资者感到满意。'),
2.('油价大幅下跌，能源公司面临挑战。','未来智能城市的建设趋势愈发明显。'),
3.('利率上升，影像房地产市场','高利率对房地产有一定给冲击。'),
我们期望模型能够帮我们识别出成对的句子中，2句话是否是有关联的。
我们期望模型输出的结果为：
['是','不是','是']
'''

from openai import OpenAI

client = OpenAI(
    base_url = "https://ws-kxxqiuowiuke0uzn.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
    #base_url = "http://localhost:11434/v1"
)

#这里先要做一个数据示例，是元组类型 示例要有结果
example_data = {
    "是":[
        ("公司ABC发布了季度财报，显示盈利增长。","财报披露，公司ABC利润上升。"),
        ("公司ITCAST发布了年度财报，显示盈利大幅增长。","财报披露，公司ITCAST更赚钱了。"),
    ],
    "不是":[
        ("黄金行情下跌，投资者抛售。","外汇市场交易额创下新高。"),
        ("央行降息，刺激经济增长。","新能源技术的创新。")
    ]
}

#问题列表
questions = [
    ('利率上升，影像房地产市场','高利率对房地产有一定给冲击。'),
    ('油价大幅下跌，能源公司面临挑战。','未来智能城市的建设趋势愈发明显。'),
    ('股票市场今日大涨，投资者乐观。','持续上涨的市场让投资者感到满意。')
]

'''
#想要得到的messages的列表内容
messages = [
    {"role":"system","content":f"你帮我完成文本匹配，我给你2个句子，被[]包围，你判断他们是否匹配，回答是或者不是，请参考如下示例："},

    {"role":"user","content":"句子1:[公司ABC发布了季度财报，显示盈利增长。]句子2:[财报披露，公司ABC利润上升。]"},
    {"role":"assistant","content":f"是"},
    {"role":"user","content":"句子1:[公司ITCAST发布了年度财报，显示盈利大幅增长。]句子2:[财报披露，公司ITCAST更赚钱了。]"},
    {"role":"assistant","content":f"是"},
    {"role":"user","content":"句子1:[黄金行情下跌，投资者抛售。]句子2:[外汇市场交易额创下新高。]"},
    {"role":"assistant","content":f"不是"},
    {"role":"user","content":"句子1:[央行降息，刺激经济增长。]句子2:[新能源技术的创新。]"},
    {"role":"assistant","content":f"不是"},
]
'''

messages = [
    {"role":"system","content":f"你帮我完成文本匹配，我给你2个句子，被[]包围，你判断他们是否匹配，回答是或者不是，请参考如下示例："}
]


#这里需要构造这个messages，通过追加的方式
for key,value in example_data.items():  #这里value就是存放的列表，列表存放着元组，元组存放两个句子
    for i in value:  #i这个临时变量去接收这个元组
        messages.append(
            {"role":"user","content":f"句子1:[{i[0]}],句子2:[{i[1]}]"}
        )
        messages.append(
            {"role":"assistant","content":key}
        )

'''
for i in messages:
    print(i)
'''

#这里要去处理模型对问题的回答,这个地方要对system包裹的角色进行处理
for q in questions:
    response = client.chat.completions.create(
        model = "qwen3.8-max",
        messages = messages + [{"role":"user","content":f"句子1:[{q[0]}],句子2:[{q[1]}]"}]
    )

    print(response.choices[0].message.content)