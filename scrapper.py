import urllib

from trip import Trip
from pyppeteer.network_manager import Request, Response

import asyncio
from pyppeteer import launch


async def req_intercept(req: Request):
    req.headers.update({'accept': 'fr-text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,'
                                  '*/*;q=0.8,application/signed-exchange;v=b3FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,'
                                  'de;q=0.6'})
    req.headers.update({'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6'})

    global page
    global hasFetched
    cookies = await page.cookies()

    if cookies and not hasFetched:
        hasFetched = True
        form = Trip().data()
        token = filter(lambda x: x['name'] == '__RequestVerificationToken', cookies)
        form["__RequestVerificationToken"] = list(token)[0]['value']

        req.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        await req.continue_(overrides={'method': 'POST',
                                       'headers': req.headers,
                                       'url': 'https://www.transavia.com/fr-FR/reservez-un-vol/vols/deeplink',
                                       'postData': urllib.parse.urlencode(form)})
    else:
        await req.continue_(overrides={ 'headers': req.headers})


async def resp_intercept(resp: Response):
    print(f"New header: {resp.request.headers}")

    text = await resp.text();
    print(text)


async def main():
    browser = await launch({'headless': True,
                            'args': [
                                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) '
                                'Chrome/75.0.3770.142 Safari/537.36',
                            ]
                            })
    global page
    page = await browser.newPage()
    await page.setRequestInterception(True)
    page.on('request', req_intercept)
    page.on('response', resp_intercept)
    resp = await page.goto('https://www.transavia.com/fr-FR/accueil')


global page
global hasFetched
hasFetched = False
page = None
asyncio.get_event_loop().run_until_complete(main())
