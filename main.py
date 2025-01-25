#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from src.bot.bir_fatura_bot import BirFaturaBot
from config.credentials import EMAIL, PASSWORD

def main():
    """
    BirFatura raporlama botu ana fonksiyonu.
    """
    try:
        print("\n🤖 BirFatura Rapor Botu başlatılıyor...\n")
        
        bot = BirFaturaBot()
        
        # Önce giriş yap
        if bot.login(EMAIL, PASSWORD):
            print("\n✅ Giriş başarılı!")
            
            # Rapor oluştur
            if bot.create_report():
                print("\n✅ Rapor başarıyla oluşturuldu ve indirildi!")
                print("\n✨ İşlem tamamlandı!")
            else:
                print("\n❌ Rapor oluşturulamadı!")
                bot.take_screenshot("report_error")
        else:
            print("\n❌ Giriş başarısız!")
            bot.take_screenshot("login_error")
            
    except Exception as e:
        print(f"\n❌ Hata oluştu: {str(e)}")
        bot.take_screenshot("error")
    finally:
        bot.close()
        print("\n👋 Bot kapatılıyor...\n")

if __name__ == "__main__":
    main() 