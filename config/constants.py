import os

# URLs
BASE_URL = "https://uygulama.birfatura.com"
LOGIN_URL = f"{BASE_URL}/UyeGirisi"
INVOICE_URL = f"{BASE_URL}/satisfaturalarigoster"
REPORTS_URL = f"{BASE_URL}/rapor"

# Paths
DOWNLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "downloads")

# Wait Times (seconds)
PAGE_LOAD_WAIT = 5     # Sayfa yüklenme bekleme süresi
MENU_LOAD_WAIT = 3      # Menü yüklenme bekleme süresi
REPORT_GENERATION_WAIT = 25  # Rapor oluşturma bekleme süresi
DOWNLOAD_WAIT = 45      # İndirme bekleme süresi 

# Element ID'leri
EMAIL_FIELD_ID = "keposta"
PASSWORD_FIELD_ID = "sifre"
LOGIN_BUTTON_ID = "lnkUyeOl"
START_DATE_ID = "baslangicTarihi"
END_DATE_ID = "bitisTarihi"
OPERATION_TYPE_ID = "islemTuru"
DOWNLOAD_BUTTON_ID = "btnIndir"

# CSS Selectors
OPERATIONS_MENU_SELECTOR = ".btn.dropdown-toggle"
BULK_CARGO_OPTION_SELECTOR = "option[value='toplu_kargo_excel']"
REPORT_MODAL_SELECTOR = ".modal-content"

# Link metinleri
DOWNLOAD_REPORT_LINK_TEXT = "Rapor İndir (Excel, XML)" 