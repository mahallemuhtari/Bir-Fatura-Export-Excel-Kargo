from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime, timedelta
import time
from pathlib import Path
import traceback
import config.constants as config
from src.utils.browser import create_driver

class BirFaturaBot:
    def __init__(self):
               
        """Bot örneğini başlatır ve tarayıcıyı yapılandırır."""
        self.driver = create_driver()
        self.wait = WebDriverWait(self.driver, 20)  # Bekleme süresini 20 saniyeye çıkardık
        self.actions = ActionChains(self.driver)
        print("\n🌐 Tarayıcı başlatıldı")
        
        # Downloads klasörünü oluştur
        self.downloads_dir = Path(config.DOWNLOAD_DIR)
        self.downloads_dir.mkdir(exist_ok=True)

    def take_screenshot(self, name):
        """Belirtilen isimle ekran görüntüsü alır."""
        self.driver.save_screenshot(f"{name}.png")
        print(f"Ekran görüntüsü kaydedildi: {name}.png")

    def check_iframes(self):
        """Sayfadaki tüm iframe'leri kontrol eder ve listeler."""
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        print(f"\nToplam {len(iframes)} iframe bulundu:")
        for i, iframe in enumerate(iframes, 1):
            try:
                iframe_id = iframe.get_attribute("id")
                iframe_name = iframe.get_attribute("name")
                print(f"iframe {i}: id='{iframe_id}', name='{iframe_name}'")
            except:
                print(f"iframe {i}: özellikler okunamadı")
        return iframes

    def login(self, email, password):
        """BirFatura sistemine giriş yapar."""
        try:
            print("\n🔑 Giriş yapılıyor...")
            self.driver.get(config.LOGIN_URL)
            time.sleep(config.PAGE_LOAD_WAIT)
            
            # Sayfanın yüklenmesini bekle
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(config.PAGE_LOAD_WAIT)
            
            print("Giriş bilgileri giriliyor...")
            email_field = self.wait.until(EC.presence_of_element_located((By.ID, config.EMAIL_FIELD_ID)))
            email_field.clear()
            email_field.send_keys(email)
            
            password_field = self.wait.until(EC.presence_of_element_located((By.ID, config.PASSWORD_FIELD_ID)))
            password_field.clear()
            password_field.send_keys(password)

            
            # Giriş bilgilerini doldur
            print("Giriş yapılıyor...")
            login_button = self.wait.until(EC.element_to_be_clickable((By.ID, config.LOGIN_BUTTON_ID)))
            login_button.click()
            
            # Giriş başarılı mı kontrol et
            time.sleep(config.PAGE_LOAD_WAIT * 2)  # Giriş için daha uzun bekle
            
            # URL değişti mi kontrol et
            current_url = self.driver.current_url
            if config.LOGIN_URL in current_url:
                print("Giriş başarısız oldu!")
                self.take_screenshot("login_failed")
                return False
                
            print("Giriş başarılı!")
            return True
            
        except Exception as e:
            print(f"\n❌ Giriş yapılamadı: {str(e)}")
            return False
            
    def create_report(self) -> bool:
        """Rapor oluşturma işlemini gerçekleştirir."""
        try:
            print("\n📊 Rapor oluşturuluyor...")
            
            self.driver.get(config.INVOICE_URL)
            time.sleep(config.PAGE_LOAD_WAIT * 2)  # Sayfa yüklenmesi için daha uzun bekle

            # Sayfanın tamamen yüklenmesini bekle
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            time.sleep(config.PAGE_LOAD_WAIT)  # Ekstra bekleme
            
            # iframe kontrolü
            print("\niframe'ler kontrol ediliyor...")
            # iframes = self.check_iframes()
            
            # İşlemler menüsünü bul
            print("\nİşlemler menüsü aranıyor...")
            islemler_menu = None
            
            # Doğru selektörlerle dene
            selectors = [
                (By.CSS_SELECTOR, ".btn-group > a.btn[data-toggle='dropdown']"),
                (By.CSS_SELECTOR, "a.btn.btn-default.btn-circle[data-toggle='dropdown']"),
                (By.XPATH, "//a[contains(@class, 'btn') and contains(., 'İşlemler')]"),
                (By.CSS_SELECTOR, ".btn-group .dropdown-toggle")
            ]
            
            for by, selector in selectors:
                try:
                    element = self.wait.until(EC.element_to_be_clickable((by, selector)))
                    if element:
                        islemler_menu = element
                        print(f"İşlemler menüsü bulundu: {selector}")
                        break
                except:
                    continue

            if islemler_menu:
                # Actions API ile menüyü aç
                print("İşlemler menüsü tıklanıyor...")
                self.actions.move_to_element(islemler_menu).click().perform()
                time.sleep(config.MENU_LOAD_WAIT * 2)  # Menünün açılması için bekle

                # Rapor indirme seçeneğini bul
                print("Rapor indirme seçeneği aranıyor...")
                try:
                    # Önce doğrudan link ile dene
                    rapor_link = self.wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".dropdown-menu > li:first-child > a")))
                    
                    print("Rapor indirme seçeneği bulundu, tıklanıyor...")
                    self.actions.move_to_element(rapor_link).click().perform()
                    time.sleep(config.MENU_LOAD_WAIT * 2)
                    
                except Exception as e:
                    print(f"Doğrudan link ile tıklama başarısız: {str(e)}")
                    print("JavaScript ile deneniyor...")
                    
                    try:
                        # JavaScript ile rapor indirme modalını aç
                        self.driver.execute_script(
                            "ModalExcelExport('modalExport', '1-3-4-7-12-13-15-18-19-24-25-29-30-35-47-50-55');"
                        )
                        print("JavaScript ile rapor indirme başlatıldı")
                        time.sleep(2)  # Modal'ın açılması için bekle
                        
                        # Modal'ın yüklenmesini bekle
                        print("Modal'ın yüklenmesi bekleniyor...")
                        modal = self.wait.until(EC.presence_of_element_located((By.ID, "modalExport")))
                        print("Modal bulundu")
                        
                        
                        # Form elementlerini doldur
                        try:
                            # Başlangıç tarihi - bir gün öncesi
                            dun = datetime.now() - timedelta(days=3)
                            dun_str = dun.strftime('%d.%m.%Y')
                            self.driver.execute_script("""
                                document.getElementById('txtBaslangicTarihiMod').value = arguments[0];
                            """, dun_str)
                            print("Başlangıç tarihi girildi:", dun_str)
                            
                            # İşlem türü seçimi - Toplu Kargo Excel
                            self.driver.execute_script("""
                                var select = document.getElementById('drpRaporTuru');
                                select.value = '3';  // Toplu Kargo Excel İndir
                                var event = new Event('change');
                                select.dispatchEvent(event);
                            """)
                            print("İşlem türü seçildi: Toplu Kargo Excel İndir")
                            
                            # 10 saniye bekle
                            print("10 saniye bekleniyor...")
                            time.sleep(10)
                            # Rapor oluştur butonu
                            self.driver.execute_script("""
                                document.getElementById('btnRaporOlustur').click();
                            """)
                            print("Rapor oluştur butonuna tıklandı")
                            
                            # Rapor indirme işlemini başlat
                            return self.download_last_report()
                            
                        except Exception as e:
                            print(f"Form doldurma hatası: {str(e)}")
                            self.take_screenshot("form_error")
                            raise
                    except Exception as e:
                        print(f"Modal açma hatası: {str(e)}")
                        self.take_screenshot("modal_error")
                        raise

        except Exception as e:
            print(f"\n❌ Rapor oluşturulamadı: {str(e)}")
            print("Hata detayı:")
            traceback.print_exc()
            self.take_screenshot("report_error")
            return False
            
    def download_last_report(self):
        """Son oluşturulan raporu indirir."""
        try:
            print("\n📥 Rapor indiriliyor...")
            
            # Raporlar sayfasında olduğumuzdan emin ol
            if "/rapor" not in self.driver.current_url:
                print("Rapor sayfasına yönlendiriliyor...")
                self.driver.get(config.BASE_URL + "/rapor")

            print("Raporun hazırlanmasını bekliyoruz...")
            time.sleep(config.REPORT_GENERATION_WAIT)  # Raporun hazırlanması için bekle
            
            # Sayfayı yenile
            self.driver.refresh()
            time.sleep(config.PAGE_LOAD_WAIT)

            # Sayfanın yüklenmesini bekle
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            max_attempts = 3
            current_attempt = 0
            
            while current_attempt < max_attempts:
                try:
                    print(f"\nİndirme butonu aranıyor (Deneme {current_attempt + 1}/{max_attempts})...")
                    # İndirme butonunu doğrudan bul
                    download_button = self.wait.until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "a.btn.btn-xs.yellow[target='_blank']")
                        )
                    )
                    
                    if download_button:
                        print("İndirme butonu bulundu")
                        href = download_button.get_attribute('href')
                        print("Buton href:", href)
                        
                        if href and not href.endswith('#'):
                            # Butona tıkla
                            download_button.click()
                            print("İndirme başlatıldı...")
                            
                            # İndirmenin tamamlanmasını bekle
                            time.sleep(config.DOWNLOAD_WAIT)
                            print("İndirme tamamlandı! ✨")
                            return True
                        else:
                            print("Buton henüz aktif değil, bekleniyor...")
                            time.sleep(config.PAGE_LOAD_WAIT)
                            self.driver.refresh()
                            current_attempt += 1
                    else:
                        print("İndirme butonu bulunamadı")
                        current_attempt += 1
                        
                except Exception as e:
                    print(f"İndirme butonu hatası: {str(e)}")
                    self.take_screenshot(f"download_error_{current_attempt}")
                    current_attempt += 1
                    if current_attempt < max_attempts:
                        print("Sayfa yenileniyor ve tekrar deneniyor...")
                        self.driver.refresh()
                        time.sleep(config.PAGE_LOAD_WAIT)
            
            print("\n❌ Maksimum deneme sayısına ulaşıldı!")
            return False
            
        except Exception as e:
            print(f"\n❌ Rapor indirilemedi: {str(e)}")
            self.take_screenshot("download_error_final")
            return False
            
    def close(self):
        """Tarayıcıyı kapatır."""
        if self.driver:
            self.driver.quit() 