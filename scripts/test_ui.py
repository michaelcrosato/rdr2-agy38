import os
import time
from playwright.sync_api import sync_playwright

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)

        page.goto("http://localhost:8089/")
        page.wait_for_timeout(1000)

        # Baseline
        page.screenshot(path="/tmp/test_01_baseline.png")
        print("Captured /tmp/test_01_baseline.png")

        # Test 1: Open Missions Browser via button click
        page.click("button:has-text('MISSIONS (M)')")
        page.wait_for_timeout(600)
        page.screenshot(path="/tmp/test_02_missions.png")
        print("Captured /tmp/test_02_missions.png")

        # Test 2: Close and Open Journal
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.click("button:has-text('JOURNAL (J)')")
        page.wait_for_timeout(600)
        page.screenshot(path="/tmp/test_03_journal.png")
        print("Captured /tmp/test_03_journal.png")

        # Test 3: Close and Open Poker
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.click("button:has-text('POKER (P)')")
        page.wait_for_timeout(600)
        page.screenshot(path="/tmp/test_04_poker.png")
        print("Captured /tmp/test_04_poker.png")

        # Test 4: Mount horse
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)
        page.click("button:has-text('MOUNT (E)')")
        page.wait_for_timeout(600)
        page.screenshot(path="/tmp/test_05_mounted.png")
        print("Captured /tmp/test_05_mounted.png")

        browser.close()
        print("Browser errors logged:", len(errors))
        for err in errors:
            print("  ERR:", err)

if __name__ == "__main__":
    run_tests()
