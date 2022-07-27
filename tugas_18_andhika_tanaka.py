import unittest
import time
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class MyAppventureLogin (unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))
        self.homeUrl = "https://myappventure.herokuapp.com/home"
        self.loginUrl = "https://myappventure.herokuapp.com/login"
        self.registrationUrl = "https://myappventure.herokuapp.com/registration"
    
    def test_login_with_valid_data(self):
        driver = self.driver
        driver.get(self.loginUrl)
        
        email = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        btnSubmit = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[4]/button")

        email.send_keys("andhikatanaka19@gmail.com")
        password.send_keys("passwordnew")
        btnSubmit.click()
        
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.current_url != self.loginUrl)

        expectedUrl= driver.current_url
        self.assertEqual(expectedUrl,self.homeUrl)

    def test_login_with_invalid_email(self):
        driver = self.driver
        driver.get(self.loginUrl)
        
        email = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        btnSubmit = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[4]/button")

        email.send_keys("andhikatanaka@gmail.com")
        password.send_keys("password")
        btnSubmit.click()
        time.sleep(5)

        errMessage = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[2]/p").text
        expectedMessage = "Alamat email atau kata sandi yang\nanda masukan tidak valid"
        self.assertEqual(errMessage, expectedMessage)

    def test_login_with_invalid_password(self):
        driver = self.driver
        driver.get(self.loginUrl)
        
        email = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        btnSubmit = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[4]/button")

        email.send_keys("andhikatanaka19@gmail.com")
        password.send_keys("password")
        btnSubmit.click()
        time.sleep(5)

        errMessage = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[2]/p").text
        expectedMessage = "Kata Sandi Salah"
        self.assertEqual(errMessage, expectedMessage)
    
    def test_login_with_empty_data(self):
        driver = self.driver
        driver.get(self.loginUrl)
        
        email = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        btnSubmit = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[4]/button")

        btnSubmit.click()
        time.sleep(5)

        nullEmailMessage = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[2]/div").text
        nullPasswordMessage = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[3]/div").text
        
        expectedNullEmailMessage = "diperlukan email"
        expectedNullPasswordMessage = "diperlukan kata sandi"

        self.assertEqual(email.text, "")
        self.assertEqual(password.text, "")
        self.assertEqual(nullEmailMessage, expectedNullEmailMessage)
        self.assertEqual(nullPasswordMessage, expectedNullPasswordMessage)

    def test_registration_new_user_from_login_page(self):
        letters = string.ascii_lowercase
        randUsername = ( ''.join(random.choice(letters) for i in range(10)) )
        randEmail = randUsername + '@mailinator.com'

        driver = self.driver
        driver.get(self.loginUrl)

        registrationLink = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[4]/div/p/a")
        registrationLink.click()
        
        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.current_url != self.loginUrl)

        username = driver.find_element(By.NAME, "username")
        email = driver.find_element(By.NAME, "email")
        password = driver.find_element(By.NAME, "password")
        btnRegistration = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div/form/div[5]/button")

        username.send_keys(randUsername)
        email.send_keys(randEmail)
        password.send_keys("password")
        btnRegistration.click()

        wait = WebDriverWait(driver, 10)
        wait.until(lambda driver: driver.current_url != self.registrationUrl)

        success_message = driver.find_element(By.XPATH, "//*[@id='__next']/main/div/div[2]/p").text
        expected_url= driver.current_url
        expected_message = "Selamat! Akun anda berhasil dibuat"
        self.assertEqual(expected_url, "https://myappventure.herokuapp.com/success-registration")
        self.assertEqual(expected_message, success_message)

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()