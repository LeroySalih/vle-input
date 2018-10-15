from vle import loginToVLE, findHomeworkUrl, initialiseVLEConnection, addFeedbackForm, loadData, gotoHomework
import sys

def parseCommands():

  homework = ''
  form = ''

  index = 0
  while index < len (sys.argv):

    if sys.argv[index] == '-h':
      index = index + 1
      homework = sys.argv[index]

    if sys.argv[index] == '-f':
      index = index + 1
      form = sys.argv[index]

    index = index + 1

  return (homework, form)

def clearGrades (browser):
  framesets = browser.find_elements_by_xpath("//*[ starts-with(@id,'uLink') ]")

  for f in framesets:
    id = f.get_attribute("id").split("_")[1]
    
    #Open Feedback Form
    feedbackButtonXPath = '//div[@id = "mainPeople"]//fieldset/div/center/a[contains(@id, "{0}")]'.format(id[-3:])
    # feedbackButtonId = "//*[@id='gradeButton_8432-{0}']".format(id)
    feedbackButton = browser.find_element_by_xpath(feedbackButtonXPath)
    feedbackButton.click()

    removeGradeButton = browser.find_element_by_xpath('//*[@id="g_removeGrade"]')
    removeGradeButton.click()


# feedback = getPupilFeedback()
title, form  = ('Heros of Computing', '7a/It1') # parseCommands()
print (title, form)
browser = initialiseVLEConnection()
loginToVLE(browser)



active_url = findHomeworkUrl (browser, title, form, "homeworkList_active")
recent_url = findHomeworkUrl (browser, title, form, "homeworkList_recently_overdue")
overdue_url = findHomeworkUrl (browser, title, form, "homeworkList_overdue")
url = active_url + recent_url + overdue_url
print ('Navigating to ', url)

gotoHomework(browser, url)
clearGrades(browser)

browser.quit
