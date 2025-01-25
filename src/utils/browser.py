from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from pathlib import Path

def create_driver():
    """Selenium WebDriver'ı yapılandırır ve başlatır."""
    chrome_options = Options()
    
    # Temel ayarlar
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-popup-blocking")
    
    # Dosya indirme ayarları
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)
    
    prefs = {
        "download.default_directory": str(downloads_dir.absolute()),
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Headless mod için ayarlar (isteğe bağlı)
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--window-size=1920,1080")
    
    # WebDriver oluştur
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    
    return driver 