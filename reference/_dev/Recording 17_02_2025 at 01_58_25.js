const fs = require('fs');
const puppeteer = require('puppeteer'); // v22.0.0 or later

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const timeout = 5000;
    page.setDefaultTimeout(timeout);

    const lhApi = await import('lighthouse'); // v10.0.0 or later
    const flags = {
        screenEmulation: {
            disabled: true
        }
    }
    const config = lhApi.desktopConfig;
    const lhFlow = await lhApi.startFlow(page, {name: 'Recording 17/02/2025 at 01:58:25', config, flags});
    {
        const targetPage = page;
        await targetPage.setViewport({
            width: 1843,
            height: 696
        })
    }
    await lhFlow.startNavigation();
    {
        const targetPage = page;
        const promises = [];
        const startWaitingForEvents = () => {
            promises.push(targetPage.waitForNavigation());
        }
        startWaitingForEvents();
        await targetPage.goto('vscode-file://vscode-app/Applications/Cursor.app/Contents/Resources/app/out/vs/code/electron-sandbox/workbench/workbench.html');
        await Promise.all(promises);
    }
    await lhFlow.endNavigation();
    await lhFlow.startTimespan();
    {
        const targetPage = page;
        await puppeteer.Locator.race([
            targetPage.locator('div.full-input-box > div:nth-of-type(2) > div.scrollable-div-container > div > div:nth-of-type(1) > div > div'),
            targetPage.locator('::-p-xpath(//*[@id=\\"workbench.panel.composerViewPane2\\"]/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div)'),
            targetPage.locator(':scope >>> div.full-input-box > div:nth-of-type(2) > div.scrollable-div-container > div > div:nth-of-type(1) > div > div')
        ])
            .setTimeout(timeout)
            .click({
              offset: {
                x: 137.8125,
                y: 19.5843505859375,
              },
            });
    }
    {
        const targetPage = page;
        await puppeteer.Locator.race([
            targetPage.locator(`::-p-aria( Checkpoint created. Restore Image preview  volante_lokalnie.tcss Kid of works. The save notifications aren\\'t needed. THe layout of the right side is ugly, It should be Title [old] [new] Descrption [old] — Markdown [new] One under the other When I click the sorting keys: [02/17/25 01:47:50] INFO 2025-02-17 01:47:50,458 [INFO] ================================================================================ volante_lokalnie.py:247 INFO 2025-02-17 01:47:50,462 [INFO] [DB] Database Status: volante_lokalnie.toml volante_lokalnie.py:248 INFO 2025-02-17 01:47:50,463 [INFO] -------------------------------------------------------------------------------- volante_lokalnie.py:249 INFO 2025-02-17 01:47:50,464 [INFO] [DB] Total Active Offers: 285 volante_lokalnie.py:250 INFO 2025-02-17 01:47:50,466 [INFO] [DB] Total Value: 16516.00 zł volante_lokalnie.py:251 INFO 2025-02-17 01:47:50,467 [INFO] [DB] Total Views: 11634 volante_lokalnie.py:252 INFO 2025-02-17 01:47:50,468 [INFO] [DB] Pending Changes: 0 volante_lokalnie.py:253 INFO 2025-02-17 01:47:50,469 [INFO] -------------------------------------------------------------------------------- volante_lokalnie.py:280 INFO 2025-02-17 01:47:50,471 [INFO] [DB] Most Recent Offer: volante_lokalnie.py:281 INFO 2025-02-17 01:47:50,472 [INFO] • Title: Ola Mońko Wherever You Are FOLIA volante_lokalnie.py:282 INFO 2025-02-17 01:47:50,473 [INFO] • Price: 3.00 zł volante_lokalnie.py:283 INFO 2025-02-17 01:47:50,474 [INFO] • Views: 131 volante_lokalnie.py:284 INFO 2025-02-17 01:47:50,475 [INFO] • Type: Kup teraz volante_lokalnie.py:285 INFO 2025-02-17 01:47:50,477 [INFO] • Listed: 2025-02-16 23:16 volante_lokalnie.py:286 INFO 2025-02-17 01:47:50,478 [INFO] ================================================================================ volante_lokalnie.py:287 WARNING 2025-02-17 01:47:50,479 [WARNING] [DB] Database volante_lokalnie.py:292 /Users/adam/Developer/vcs/github.twardoch/pub/volante_lokalnie/src/volante_lokalnie/volante_lokalnie.toml not found, started empty. INFO 2025-02-17 01:47:50,499 [INFO] ================================================================================ volante_lokalnie.py:247 INFO 2025-02-17 01:47:50,500 [INFO] [DB] Database Status: volante_lokalnie.toml volante_lokalnie.py:248) >>>> ::-p-aria([role=\\"textbox\\"])`),
            targetPage.locator('div.aislash-editor-input'),
            targetPage.locator('::-p-xpath(//*[@id=\\"workbench.panel.composerViewPane2\\"]/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div[1])'),
            targetPage.locator(':scope >>> div.aislash-editor-input')
        ])
            .setTimeout(timeout)
            .fill('I ');
    }
    {
        const targetPage = page;
        await targetPage.keyboard.up('i');
    }
    {
        const targetPage = page;
        await puppeteer.Locator.race([
            targetPage.locator(`::-p-aria( Checkpoint created. Restore Image preview  volante_lokalnie.tcss Kid of works. The save notifications aren\\'t needed. THe layout of the right side is ugly, It should be Title [old] [new] Descrption [old] — Markdown [new] One under the other When I click the sorting keys: [02/17/25 01:47:50] INFO 2025-02-17 01:47:50,458 [INFO] ================================================================================ volante_lokalnie.py:247 INFO 2025-02-17 01:47:50,462 [INFO] [DB] Database Status: volante_lokalnie.toml volante_lokalnie.py:248 INFO 2025-02-17 01:47:50,463 [INFO] -------------------------------------------------------------------------------- volante_lokalnie.py:249 INFO 2025-02-17 01:47:50,464 [INFO] [DB] Total Active Offers: 285 volante_lokalnie.py:250 INFO 2025-02-17 01:47:50,466 [INFO] [DB] Total Value: 16516.00 zł volante_lokalnie.py:251 INFO 2025-02-17 01:47:50,467 [INFO] [DB] Total Views: 11634 volante_lokalnie.py:252 INFO 2025-02-17 01:47:50,468 [INFO] [DB] Pending Changes: 0 volante_lokalnie.py:253 INFO 2025-02-17 01:47:50,469 [INFO] -------------------------------------------------------------------------------- volante_lokalnie.py:280 INFO 2025-02-17 01:47:50,471 [INFO] [DB] Most Recent Offer: volante_lokalnie.py:281 INFO 2025-02-17 01:47:50,472 [INFO] • Title: Ola Mońko Wherever You Are FOLIA volante_lokalnie.py:282 INFO 2025-02-17 01:47:50,473 [INFO] • Price: 3.00 zł volante_lokalnie.py:283 INFO 2025-02-17 01:47:50,474 [INFO] • Views: 131 volante_lokalnie.py:284 INFO 2025-02-17 01:47:50,475 [INFO] • Type: Kup teraz volante_lokalnie.py:285 INFO 2025-02-17 01:47:50,477 [INFO] • Listed: 2025-02-16 23:16 volante_lokalnie.py:286 INFO 2025-02-17 01:47:50,478 [INFO] ================================================================================ volante_lokalnie.py:287 WARNING 2025-02-17 01:47:50,479 [WARNING] [DB] Database volante_lokalnie.py:292 /Users/adam/Developer/vcs/github.twardoch/pub/volante_lokalnie/src/volante_lokalnie/volante_lokalnie.toml not found, started empty. INFO 2025-02-17 01:47:50,499 [INFO] ================================================================================ volante_lokalnie.py:247 INFO 2025-02-17 01:47:50,500 [INFO] [DB] Database Status: volante_lokalnie.toml volante_lokalnie.py:248) >>>> ::-p-aria([role=\\"textbox\\"])`),
            targetPage.locator('div.aislash-editor-input'),
            targetPage.locator('::-p-xpath(//*[@id=\\"workbench.panel.composerViewPane2\\"]/div/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div/div/div/div[1])'),
            targetPage.locator(':scope >>> div.aislash-editor-input')
        ])
            .setTimeout(timeout)
            .fill('I am typing one two three ');
    }
    await lhFlow.endTimespan();
    const lhFlowReport = await lhFlow.generateReport();
    fs.writeFileSync(__dirname + '/flow.report.html', lhFlowReport)

    await browser.close();

})().catch(err => {
    console.error(err);
    process.exit(1);
});
