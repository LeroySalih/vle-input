from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import time 
import pandas as pd 
from pandas import ExcelFile 
from fpdf import FPDF, HTMLMixin

import sys 

from vle import loginToVLE, findHomeworkUrl, initialiseVLEConnection, addFeedbackForm, loadData, gotoHomework

class MyFPDF(FPDF, HTMLMixin):
      pass

spreadsheetUrl = "/Users/leroy/Dropbox/Computing Lessons/Year 7/2. Hero's Of Computing/99. Assessments/"




def getAssessmentData(sheetName):
  return pd.read_excel(spreadsheetUrl + 'Assessment Results.xlsx', sheet_name=sheetName)

def getPupilFeedback(sheetName):

  pupilFeedback = {}
  
  pupilLookupDF = pd.read_excel(spreadsheetUrl + 'Assessment Results.xlsx', sheet_name='Pupil Lookup')
  assessmentDataDF = getAssessmentData(sheetName)
  #print (assessmentDataDF.iloc[-7:, 2:]) 

  # 
  # Load Feedback
  pupilsDF = assessmentDataDF.columns.values[4:]
  
  for pupil in pupilsDF:
    DF = assessmentDataDF.iloc[-7:]
    # print (DF)
    rows = DF.shape[0]
    # print ("There are {0} rows in ".format(rows))
    #print (DF.columns.values)

    pupil_resultsDF = DF[['Title', pupil]]
    # print (DF)

    levelRow = assessmentDataDF.iloc[-8]
    level = levelRow[pupil]

    feedback = ''
    # print (DF)
    for index in range (0, rows, 1):
      #print ('**26**', DF.iloc[index])
      # print (DF.iloc[index - 1, -1])
      if (pupil_resultsDF.iloc[index, -1] == 'X'):
        feedback = feedback + ' ' + pupil_resultsDF.iloc[index, 0]

    pupilFeedback[pupil] = {'feedback': feedback, 'level': level}
    


    #Get Level

  return pupilFeedback

def parseCommands():

  print (sys.argv)

  homework = ''
  form = ''
  sheetName = ''

  index = 0
  while index < len (sys.argv):

    if sys.argv[index] == '-h':
      index = index + 1
      homework = sys.argv[index]

    if sys.argv[index] == '-f':
      index = index + 1
      form = sys.argv[index]

    if sys.argv[index] == '-s':
      index = index + 1
      sheetName = sys.argv[index]

    index = index + 1

  return (homework, form, sheetName)


def generateHTMLForPage(pupilName, pupilDF):

  level = pupilDF[pupilName][-8:-7]
  level = list(level)[0]
  html = """
  <img src="bisak_logo.png" height="30" width="138"></img>

  <h2>Heros Of Computing - {0}</h2>
  <h3>Level: {1}</h3>
  <table border="0" align="left" width="75%">
  <thead>
    <tr>
      <th width="60%" align="left">Name</th>
      <th width="20%">Evidenced</th>
      <th width="20%">Not Evidenced</th>
    </tr>
  </thead>
  <tbody>
  {2}
  </tbody>
  </table>
  <p>Date:{3}</p>
  """

  rows =  """ 
    <tr>
      <td>Evidence Item 11</td>
      <td align="center">X</td>
      <td align="center"></td>
    </tr>
  """

  rows = pupilDF[:-14].shape[0]
  
  rowsHtml = ''
  for index in range (0, rows):
    title = pupilDF.iloc[index][0]

    evidenced = pupilDF.iloc[index][1]
    print (title, evidenced, evidenced == 1)
    if (evidenced == 1):
      rowsHtml += """<tr>
                      <td width='70%'><font size='10'>{0}</font></td>
                      <td width='15%'><font size='10'>{1}</font></td>
                      <td width='15%'><font size='10'>{2}</font></td>
                    </tr>""".format(title, 'X', ' ')
      
    else:
      rowsHtml += """<tr>
                      <td width='70%'><font size='10'>{0}</font></td>
                      <td width='15%'><font size='10'>{1}</font></td>
                      <td width='15%'><font size='10'>{2}</font></td>
                    </tr>""".format(title, ' ', 'X')
  


  return html.format(pupilName, level, rowsHtml, '2018-10-15')

def generateFeedbackPDFs(feedbackDF, level, form):
  #print (feedbackDF)

  pupilNames = list(feedbackDF)[4:]
  # print (pupilNames)

  criteria_key = (list(feedbackDF)[2]) 
  
  pdf=MyFPDF()
  #First page

  for index, pupilName in enumerate(pupilNames):

    name_key = (list(feedbackDF)[4:])[index]
    pupilDF = feedbackDF[[criteria_key, name_key]]

    pdf.add_page()
    html = generateHTMLForPage(name_key, pupilDF)
    pdf.write_html(html)
  


  pdf.output(spreadsheetUrl  + form + '_feedback.pdf','F')

title, form, sheetName  = parseCommands()
print ('Loading data from {0}'.format(sheetName))

feedback = getPupilFeedback(sheetName)

generateFeedbackPDFs(getAssessmentData(sheetName), sheetName, sheetName)


browser = initialiseVLEConnection()
loginToVLE(browser)

active_url = findHomeworkUrl (browser, title, form, "homeworkList_active")
recent_url = findHomeworkUrl (browser, title, form, "homeworkList_recently_overdue")
overdue_url = findHomeworkUrl (browser, title, form, "homeworkList_overdue")
url = active_url + recent_url + overdue_url

print ("Accessing URL: {0}".format(url))

gotoHomework(browser, url)
loadData(browser, feedback)
browser.quit




  
  
