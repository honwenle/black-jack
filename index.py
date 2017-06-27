# coding: utf-8
from wxpy import *
import random
bot = Bot(cache_path = True)
noclip = bot.friends().search('微杏')[0]
test_group = bot.groups().search('测试群')[0]

play_list = []
gameStep = -1
def deal(msg):
    global gameStep
    msg.reply('开始发牌')
    m_list = msg.chat.members
    for m in m_list:
        if m.is_friend and (m != bot.self):
            play_list.append(m)
            open_num = str(random.randint(1,10))
            dark_num = str(random.randint(1,10))
            m.open = []
            m.open.append(open_num)
            m.dark = dark_num
            m.send('你的暗牌是：' + dark_num + '，明牌是：' + open_num)
        else:
            if m != bot.self:
                m.add('加我好友才能给你发暗牌哦')
    for p in play_list:
        p.canGet = True
        msg.reply(p.name + '的明牌为：' + ''.join(p.open))
    msg.reply('开始询问(回复1要牌，回复0不要牌)')
    gameStep += 1
    msg.reply(play_list[gameStep].name + '是否要牌')

@bot.register(Group, TEXT)
def recive_group_message(msg):
    global gameStep, play_list
    try:
        print(msg.chat.name + ' > ' + msg.member.name + ' : ' + msg.text)
    except UnicodeEncodeError:
        print('有些编码没法print')
    if gameStep == -1:
        if '21' in msg.text:
            deal(msg)
    elif gameStep > -1:
        p = play_list[gameStep]
        if msg.member == p:
            choice = msg.text == '1' or msg.text == '0'
            if choice:
                if msg.text == '1':
                    open_num = str(random.randint(1,10))
                    p.open.append(open_num)
                    if sum([int(num) for num in p.open]) + int(p.dark) > 21:
                        msg.reply(p.name + ' 爆掉了')
                        gameStep = -1
                        play_list = []
                        return
                elif msg.text == '0':
                    p.canGet = False
                for item in play_list[gameStep+1:]:
                    gameStep += 1
                    if item.canGet:
                        next_p = item
                        break
                else:
                    gameStep = 0
                    next_p = play_list[0]
                msg.reply(p.name + '的明牌为：' + ' , '.join(p.open))
                msg.reply(next_p.name + '是否要牌')
            else:
                msg.reply('回复1要牌，回复0不要牌')
        else:
            msg.reply('@' + msg.member.name + ',还没轮到你，别插嘴')

embed()