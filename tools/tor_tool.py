#!/usr/bin/env python
# coding=utf-8
import os.path

from stem import Signal
from stem.control import Controller
from tools.log import *
from tools.config import Config
from tools.config import CrawlRuntimeException
import requests
import time
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from retry import retry
import traceback


def make_new_tor_id(port: int = 9151, proxies="", ip_link="http://icanhazip.com/") -> None or str:
    logger.info("reload tor")
    try:
        controller = Controller.from_port(port=port)
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        resp = requests.get(ip_link, proxies=proxies)
        ip = resp.text.strip()
        logger.info(f"{ip}")
        return ip
    except Exception as e:
        logger.error(f"change ip error {e}")
    finally:
        time.sleep(2)


'''

打开无头浏览器
链接驱动
使用装饰器做失败重试

'''
@retry(CrawlRuntimeException, tries=5, delay=10, logger=logger)
def connect_tor_with_retry(firefox_binary, geckodriver_path, proxies, headless=True):
    driver = open_browser_with_headless(firefox_binary, geckodriver_path, proxies, headless)
    if not driver:
        logger.error(f"failed connect tor, retry connect")
        raise CrawlRuntimeException(f"failed connect tor, retry connect")

    return driver


'''
初始化浏览器参数

'''
def open_browser_with_headless(firefox_binary, geckodriver_path, proxies, headless=True):
    logger.info("init browser option")
    firefox_options = Options()
    firefox_options.headless = headless

    # TOR_SKIP_LAUNCH=1 TOR_TRANSPROXY=1 在不连接到 Tor 的情况下启动网络浏览器。
    # 然后，您需要调整网络浏览器的网络代理设置，使其无需代理（即 Tor）即可连接到互联网。
    os.environ['TOR_SKIP_LAUNCH'] = '1'
    os.environ['TOR_TRANSPROXY'] = '1'

    binary = FirefoxBinary(firefox_binary)
    profile = FirefoxProfile()
    profile.set_preference("security.cert_pinning.enforcement_level", 0)
    profile.set_preference("network.stricttransportsecurity.preloadlist", False)
    profile.set_preference("extensions.torbutton.local_tor_check", False)
    profile.set_preference("extensions.torbutton.use_nontor_proxy", True)
    profile.set_preference("browser.startup.homepage_override.mstone", "68.8.0");

    options = {
        'proxy': proxies
    }
    try:
        driver = webdriver.Firefox(options=firefox_options,
                                   firefox_profile=profile,
                                   firefox_binary=binary,
                                   seleniumwire_options=options,
                                   executable_path=geckodriver_path,
                                   service_log_path=os.path.join(Config.log_dir, "geckodriver.log"))
    except Exception as e:
        msg = traceback.format_exc()
        logger.error(f"init firefox webdriver error{e}, traceback{msg}")
        return None

    driver.get("https://check.torproject.org/")

    # 等待对话框出现并关闭它,有可能不出现而发生异常,因此需要捕获
    logger.info(f"close alert")
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.dismiss()
    except Exception as e:
        msg = traceback.format_exc()
        logger.warning(f"auto close alter error{e}, traceback{msg}")

    try:
        logger.info(f"check page load complete")
        success_text = WebDriverWait(driver, 1200).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.on'))
        )

        # 检测是否成功连接，如果没连接，则关闭driver返回空
        if "Congratulations" in success_text.text:
            logger.info("success connect tor")
            return driver
        else:
            logger.error("failed connect tor")
            driver.quit()
            return None
    except Exception as e:
        msg = traceback.format_exc()
        logger.warning(f"get connect page info timeout,close driver {e}, trace msg{msg}")
        driver.quit()
        return None




if __name__ == "__main__":
    driver = connect_tor_with_retry("/Applications/Tor Browser.app/Contents/MacOS/firefox",
                                    "/Users/zhangchao/devops/browser-driver/geckodiver/geckodriver", {
                                        'http': 'socks5h://admin:a7dm1n@45.32.223.200:65533',
                                        'https': 'socks5h://admin:a7dm1n@45.32.223.200:65533',
                                        'connection_timeout': 10
                                    }, headless=False)
    time.sleep(5)
    driver.quit()
