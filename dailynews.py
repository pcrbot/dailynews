from hoshino import Service, util
from hoshino.typing import MessageSegment, CQHttpError, CQEvent, HoshinoBot
from hoshino import aiorequests
sv = Service('dailynews', enable_on_default=False, help_='''每日早报
启用后会在每天早上发送一份早报
[@bot 今日早报] （测试用）手动发送一份早报''')


@sv.scheduled_job('cron', hour='8', minute='30')
async def autonews():
    try:
        info = await aiorequests.get('http://dwz.2xb.cn/zaob')
        try:
            info = await info.json()
        except:
            print(await info.text)
            raise
        if info['msg'] == 'Success':
            await sv.broadcast(
                MessageSegment.image(info['imageUrl'], cache=True), 'dailynews')
        else:
            sv.logger.error(f'daily news error {info["msg"]}')
    except CQHttpError as e:
        sv.logger.error(f'daily news error {e}')
        raise


@sv.on_fullmatch('今日早报', only_to_me=True)
async def handnews(bot: HoshinoBot, ev: CQEvent):
    info = await aiorequests.get('http://dwz.2xb.cn/zaob')
    info = await info.json()
    if info['msg'] == 'Success':
        await bot.send(ev, MessageSegment.image(info['imageUrl'], cache=True))
    else:
        sv.logger.error(f'daily news error {info["msg"]}')
