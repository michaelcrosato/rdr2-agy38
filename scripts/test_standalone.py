from playwright.sync_api import sync_playwright

def test_standalone():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(str(err)))

        # Load directly via file:// URL with NO web server
        file_path = "/mnt/c/Users/micha/OneDrive/Desktop/Deskop/temp/dead-horizon-1899.html"
        page.goto(f"file://{file_path}")
        page.wait_for_timeout(1000)

        page.screenshot(path="/tmp/test_standalone_screenshot.png")
        print("Captured /tmp/test_standalone_screenshot.png from direct file:// loading!")

        # Test clicking Missions
        page.click("button:has-text('MISSIONS (M)')")
        page.wait_for_timeout(500)
        page.screenshot(path="/tmp/test_standalone_missions.png")
        print("Captured /tmp/test_standalone_missions.png")

        browser.close()

        print(f"Total console/page errors: {len(errors)}")
        for e in errors:
            print("  ERROR:", e)

if __name__ == "__main__":
    test_standalone()
