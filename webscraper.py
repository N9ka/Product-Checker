from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import smtplib, ssl
   
    

def envia_correu(preu, cerca, url_desada, sender, password, recieve):
    port = 465
    SUBJECT = "BAIXADA DE PREU!"
    TEXT = "El preu actual del producte " + "'" + str(cerca) + "'" + " es de " + str(preu) + " euros"
    TEXT2 = "Link de compra: " + url_desada
    message = 'Subject: {}\n\n{}\n\n{}'.format(SUBJECT, TEXT, TEXT2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, recieve, message)
    driver.quit()


def llegir_fitxer_cred():
    user = passw = receiv =""
    with open("cred.txt", "r") as f:
        file = f.readlines()
        user = file[3].strip()
        passw = file[5].strip()
        receiv = file[7].strip()
    return user, passw, receiv 

def llegir_fitxer_producte():
    cerca = preu_guardat = percentatge_desc = ""
    with open("info.txt", "r") as f:
        file = f.readlines()
        cerca = file[2].strip()
        preu_guardat = file[7].strip()
        percentatge_desc = file[11].strip()
    return cerca, preu_guardat, percentatge_desc

options = Options()
options.set_headless(headless=True)
driver = webdriver.Chrome(options=options, executable_path=r'C:\Users\rgjos\chromedriver.exe')
driver.get("https://www.amazon.es/?ref=icp_country_us")
user, passw, receiv = llegir_fitxer_cred()
cerca, preu_guardat, percentatge_desc = llegir_fitxer_producte()
driver.find_element_by_id("twotabsearchtextbox").send_keys(cerca)
driver.find_element_by_id("nav-search-submit-text").click()
preu = driver.find_element_by_class_name("a-price")
preu_anterior = driver.find_element_by_class_name("a-text-price")
url_desada = driver.current_url
preu_nou = preu.text.split('€', 1)[0]
preu_nou = preu_nou.replace(",", ".")
preu_volgut = (float(preu_guardat)-(float(preu_guardat) * float(percentatge_desc)))
if float(preu_nou) <= preu_volgut:
    envia_correu(preu_nou,cerca,url_desada,user,passw,receiv)


