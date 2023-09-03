import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class SnapshotDrvier:
    def __init__(self, driverPath, picDir, timeOut=100):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--proxy-server=socks5h://localhost:9150")
        service = Service(driverPath)
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(timeOut)
        driver.set_script_timeout(timeOut)
        self.driver = driver
        self.picDir = picDir

    def __del__(self):
        self.driver.close()

    def snapshot(self, uri):
        self.driver.get(uri)
        width = self.driver.execute_script("return document.documentElement.scrollWidth")
        height = self.driver.execute_script("return document.documentElement.scrollHeight")
        self.driver.set_window_size(width, height)
        time.sleep(3)
        fileName = self.picDir + "/" + uri.replace("http://", '').replace("https://", '').replace("/", "_").replace('.',
                                                                                                                    '_').replace(
            ":", "_") + ".png"
        self.driver.get_screenshot_as_file(fileName)


if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #     print("usage: python websnapshot.py fileName sheetName")
    #     sys.exit(-1)
    # fileName = sys.argv[1]
    # sheetName = sys.argv[2]
    # df = pd.read_excel(fileName, sheet_name=sheetName)
    snapDrvier = SnapshotDrvier(conf.CHROME_DRIVER, conf.SNAP_FILE_DIR)
    # for idx, row in df.iterrows():
    # uri = row["主页URL"]
    uri = "http://xxxxxxxxxs6qbnahsbvxbghsnqh4rj6whbyblqtnmetf7vell2fmxmad.onion/"
    try:
        snapDrvier.snapshot(uri)
    except:
        print("uri=%s,timeout" % uri)
