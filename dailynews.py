import asyncio
import datetime

from hoshino import Service, aiorequests
from hoshino.typing import MessageSegment, CQEvent, HoshinoBot

sv = Service('dailynews', enable_on_default=False, help_='''每日早报
启用后会在每天早上发送一份早报
[@bot 今日早报] （测试用）手动发送一份早报''')

APIS = (
    'https://60s.viki.moe/v2/60s',
    'https://60s-api.viki.moe/v2/60s',
)
IMAGE_TPL = 'https://cdn.jsdmirror.com/gh/vikiboss/60s-static-host@main/static/images/{}.png'
PNG_MAGIC = b'\x89PNG\r\n\x1a\n'


async def fetch_news_image():
    today = str(datetime.date.today())
    errs = []
    for api in APIS:
        for attempt in (1, 2):
            try:
                resp = await aiorequests.get(api, timeout=20)
                info = await resp.json()
                data = info.get('data') or {}
                if info.get('code') != 200 or not data.get('image'):
                    raise ValueError(f'异常返回: {str(info)[:120]}')
                if data.get('date') != today:
                    raise ValueError(f'图源疑似停更: 接口日期 {data.get("date")}')
                return data['image']
            except Exception as e:
                errs.append(f'{api} {type(e).__name__}: {str(e)[:80]}')
                if attempt == 1:
                    await asyncio.sleep(3)
    try:
        image_url = IMAGE_TPL.format(today)
        resp = await aiorequests.get(image_url, timeout=20)
        content = await resp.content
        if resp.status_code != 200 or len(content) < 50000 or content[:8] != PNG_MAGIC:
            raise ValueError(f'响应异常: {resp.status_code} {len(content)}B')
        return image_url
    except Exception as e:
        errs.append(f'图片兜底 {type(e).__name__}: {str(e)[:80]}')
    raise RuntimeError(' | '.join(errs))


@sv.scheduled_job('cron', hour='8', minute='40', jitter=50)
async def autonews():
    img = None
    for i, wait in enumerate((0, 120, 300)):
        if wait:
            await asyncio.sleep(wait)
        try:
            img = await fetch_news_image()
            break
        except Exception as e:
            sv.logger.error(f'daily news error (round {i + 1}): {e}')
    if img:
        await sv.broadcast(MessageSegment.image(img, cache=True), 'dailynews')


@sv.on_fullmatch('今日早报', only_to_me=True)
async def handnews(bot: HoshinoBot, ev: CQEvent):
    try:
        img = await fetch_news_image()
    except Exception as e:
        sv.logger.error(f'daily news error: {e}')
        await bot.send(ev, '早报获取失败，请稍后再试')
        return
    await bot.send(ev, MessageSegment.image(img, cache=True))
