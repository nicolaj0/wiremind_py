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
    global trip
    cookies = await page.cookies()

    if cookies and not trip.hasFetchedStep1:
        token = filter(lambda x: x['name'] == '__RequestVerificationToken', cookies)
        trip.setstep1()
        trip.settoken(list(token)[0]['value'])
        req.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        await req.continue_(overrides={'method': 'POST',
                                       'headers': req.headers,
                                       'url': 'https://www.transavia.com/fr-FR/reservez-un-vol/vols/deeplink',
                                       'postData': urllib.parse.urlencode(trip.data())})

    elif trip.hasResponseStep1 and not trip.hasFetchedStep2:
        trip.setstep2()
        req.headers.update({'content-type': 'application/x-www-form-urlencoded'})
        req.headers.update({'referer': 'https://www.transavia.com/fr-FR/reservez-un-vol/vols/rechercher/'})
        req.headers.update({'X-Requested-With': 'XMLHttpRequest'})
        req.headers.update({'accept': '*/*'})
        await req.continue_(overrides={'method': 'POST',
                                       'headers': req.headers,
                                       'url': 'https://www.transavia.com/fr-FR/reservez-un-vol/vols'
                                              '/SingleDayAvailability/',
                                       'postData': urllib.parse.urlencode(trip.availdataoutbound())})
    else:
        await req.continue_(overrides={'headers': req.headers})


async def resp_intercept(resp: Response):
    # text = await resp.text();
    print(resp.url)
    global trip
    if resp.url == 'https://www.transavia.com/fr-FR/reservez-un-vol/vols/rechercher/':
        trip.sethasresponsestep1()



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
    resp = await page.goto('https://www.transavia.com/fr-FR/accueil',{
                'waitUntil': 'networkidle2',
                'timeout': 3000000
            })


global page
global trip
trip = Trip()
page = None
asyncio.get_event_loop().run_until_complete(main())
