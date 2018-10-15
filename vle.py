from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time 

def initialiseVLEConnection():
  option = webdriver.ChromeOptions()
  option.add_argument(" — incognito")
  browser = webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)

  return browser

def loginToVLE(browser):
  browser.get("https://vle.bisak.org")

  username = browser.find_element_by_id("ulogin")
  password = browser.find_element_by_id("upassword")

  username.send_keys("lsalih")
  password.send_keys("cardiff1")

  browser.find_element_by_id("submitButton").click()

def findHomeworkUrl(browser, title, form, table):
  browser.get("http://vle.bisak.org/index.php?name=Homework")
  
  xpath = "//table[@id='{0}']/tbody/tr".format(table)
  trRows = browser.find_elements_by_xpath(xpath)
  for index, trRow in enumerate(trRows):
    if index > 0:
      linkText = trRow.find_element_by_xpath('td[2]/div/a').get_attribute('text')
      linkHref = trRow.find_element_by_xpath('td[2]/div/a').get_attribute('href')
      formText = trRow.find_element_by_xpath('td[4]/a').get_attribute('text')

      if (linkText == title and formText == form):
        return linkHref

  return ""

def gotoHomework(browser, url):
  browser.get(url)
  
def loadData (browser, feedback):
  framesets = browser.find_elements_by_xpath("//*[ starts-with(@id,'uLink') ]")

  for f in framesets:
    id = f.get_attribute("id").split("_")[1]
    pupilName = f.get_attribute("text")
    print (id, ":" , pupilName, feedback[pupilName]['level'], feedback[pupilName]['feedback']  )

    #Open Feedback Form
    feedbackButtonXPath = '//div[@id = "mainPeople"]//fieldset/div/center/a[contains(@id, "{0}")]'.format(id[-3:])
    # feedbackButtonId = "//*[@id='gradeButton_8432-{0}']".format(id)
    feedbackButton = browser.find_element_by_xpath(feedbackButtonXPath)
    feedbackButton.click()
    addFeedbackForm(browser, feedback[pupilName]['level'], feedback[pupilName]['feedback'], "Computing")

def addFeedbackForm(browser, level, feedbackText, subject ):

  #Select Template
  templateSelect = Select(browser.find_element_by_xpath('//*[@id="grade_template"]'))
  templateSelect.select_by_visible_text('KS3 Levels')
  time.sleep(1)

  #Click Level Button
  id = '//*[@title="{0}"]'.format(level)
  levelsButton = browser.find_element_by_xpath(id)
  levelsButton.click()

  #Add Feedback Text
  feedbackArea = browser.find_element_by_xpath("//*[@id='g_feedback']")
  feedbackArea.send_keys(feedbackText)

  #Add linked Subject
  linkedSubject = Select(browser.find_element_by_xpath('//*[@id="mLPC_g_relatedSubjects"]'))
  linkedSubject.select_by_visible_text(subject)

  #Submit Feedback
  feedbackSubmitButton = browser.find_element_by_xpath('//*[@id="g_submitGrade"]')
  feedbackSubmitButton.click()