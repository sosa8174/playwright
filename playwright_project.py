from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # 1. Open the site
    page.goto("https://www.globalsqa.com/demo-site/draganddrop/")

    # 2. Drag 3 images to trash
    frame = page.frame_locator("iframe.demo-frame").nth(0)
    frame.locator("li.ui-widget-content").nth(0).wait_for()
    trash = frame.locator("#trash")
    for i in range(3):
        frame.locator("li.ui-widget-content").nth(i).drag_to(trash)

    time.sleep(5)

    # 3. Click on Cheatsheets link
    page.wait_for_selector('//*[@id="menu-item-6898"]/a').click()
    page.wait_for_timeout(5000)


    # 4. Go back and forward
    page.go_back()
    page.wait_for_load_state("load")
    page.go_forward()
    page.wait_for_load_state("load")
    page.wait_for_timeout(5000)

    # 5. Click on Pandas Cheat Sheet link and wait for new tab
    with context.expect_page() as new_page_info:
        page.locator('text=Pandas Cheat Sheet').click()

    new_tab = new_page_info.value
    new_tab.wait_for_load_state("load")

    print("✅ New tab opened:", new_tab.url)

    # 6. Scroll to the bottom of the new tab
    previous_height = 0
    while True:
        current_height = new_tab.evaluate("""
            () => {
                window.scrollBy(0, 500);
                return document.documentElement.scrollTop + window.innerHeight;
            }
        """)
        total_height = new_tab.evaluate("() => document.documentElement.scrollHeight")
        if current_height >= total_height:
            break
        time.sleep(0.3)

    print("✅ Scrolled to the bottom.")

    time.sleep(5)
    ss=new_tab.screenshot(path='ss.png',full_page=True)
    browser.close()
