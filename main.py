from time import sleep
import re
from selenium import webdriver


class KozelPromo:
    """ Automatic form fill up in Kozel promotion using selenium and Chrome web driver """
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://sprobujdwochzczech.pl/')

    def close_cookie_popup(self):
        cookie_btn = self.driver.find_element_by_class_name('close-cookie-popup')
        if cookie_btn:
            cookie_btn.click()

    def fill_birthdate(self, b_date):
        day = self.driver.find_element_by_name('birthdate_day')
        day.send_keys(b_date[0])
        month = self.driver.find_element_by_name('birthdate_month')
        month.send_keys(b_date[1])
        year = self.driver.find_element_by_name('birthdate_year')
        year.send_keys(b_date[2])
        year.submit()
    
    def fill_promo_form(self, c, e):
        promo_code = self.driver.find_element_by_name('promo_code')
        promo_code.send_keys(c)
        email = self.driver.find_element_by_name('email')
        email.send_keys(e)

        for i in range(1, 6):
            confirm_xpath = f'//*[@id="entry_form"]/div[2]/div/div/div/label[{i}]/span/em'
            confirm = self.driver.find_element_by_xpath(confirm_xpath)
            confirm.click()
        email.submit()
        sleep(2)
        pdf_xpath = '//*[@id="sprobuj-ponownie"]/div/div/div/div/div/div/div/div[3]/div/div[1]/a'
        pdf = self.driver.find_element_by_xpath(pdf_xpath)
        pdf.click()
        sleep(2)
        home_xpath = '//*[@id="sprobuj-ponownie"]/div/div/div/div/div/div/div/div[3]/div/div[2]/a'
        home = self.driver.find_element_by_xpath(home_xpath)
        home.click()

    def close(self):
        self.driver.quit()

    @staticmethod
    def code_list(file):
        try:
            f = open(file, 'r')
            line = f.readline()
            f.close()
            return line.split(',')
        except Exception as e:
            print(f"Problem z odczytem pliku {file}: {e}")


def get_b_date():
    while True:
        b_date = input("Podaj datę urodzenia w formacie DD-MM-YYYY: ")
        pattern = '([0-9]{2}-[0-9]{2}-[0-9]{4})'
        result = re.match(pattern, b_date)
        if result:
            break
        else:
            print("Format daty nieprawidłowy!!")
    return b_date.split('-')


def get_mail():
    while True:
        mail = input("Podaj adres e-mail: ")
        pattern = '([0-9a-z.+]*@[0-9a-z]*.[0-9a-z]*)'
        result = re.match(pattern, mail)
        if result:
            break
        else:
            print("Format adresu email nieprawidłowy!!")
    return mail


def main():
    b_date = get_b_date()
    mail = get_mail()
    kp = KozelPromo()
    sleep(2)
    kp.close_cookie_popup()
    kp.fill_birthdate(b_date)
    sleep(2)
    code_list = kp.code_list('list.txt')
    if code_list:
        for code in kp.code_list('list.txt'):
            kp.fill_promo_form(code, mail)
    kp.close()


if __name__ == '__main__':
    main()
