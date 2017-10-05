#Nahom Ogbazghi
# This is my code
import urllib2
import re

RE_ALL_DATA  = re.compile('<p><strong>Monday, April 25, 2016</strong></p>.*?Exam Time</strong>(.+?)\n<p>Biology', re.DOTALL)
RE_Groups_T = re.compile('<tr>\n(.+?)\n</tr>', re.DOTALL)
RE_ClassMeetingTime = re.compile('<td class="xl\w\w">\n<p>(.+?)</p>', re.DOTALL)
RE_ExamDate = re.compile('\n<td class="xl68">\n<p>(.+?)</p>\n</td>\n<td class="xl67">\n<p>(.+?)</p>', re.DOTALL)

url      = 'http://registrar.emory.edu/Students/Calendars/examcalendar/emorycollege_examcalendar.html'
request  = urllib2.Request(url)
response = urllib2.urlopen(request)
page     = response.read()
finals   = dict()

m = RE_ALL_DATA.search(page)
main = m.group(1)
titles = [(m.group(1),) for m in RE_Groups_T.finditer(main)]

def splitter (title):
    time = RE_ClassMeetingTime.search(title).group(1)
    examDate = RE_ExamDate.search(title).group(1)
    examTime = RE_ExamDate.search(title).group(2)
    t = time.split(' ')
    courseTime = t[0]
    if courseTime[0] == '0':
        courseTime = courseTime[1:]
    courseDay = t[1]
    if courseDay[0:3] == 'TTH' or courseDay[0:4] == 'TUTH' or courseDay == 'TTh':
        courseDay = "TuTh"
    if courseDay[len(courseDay)-6:] == '&#160;':
        courseDay = courseDay[:len(courseDay)-6]
    return (courseTime,courseDay),(examDate,examTime)

finalsSchedule = []
for i, title in enumerate(titles):
    (course_time_day, exam_date_time) = splitter(title[0])
    finalsSchedule.append((course_time_day[1],course_time_day[0], exam_date_time[0],exam_date_time[1]))

#Jinho's Code
RE_CLASSES_MAIN = re.compile('<div class="classes-main-toggle-buttons">(.+)</div>', re.DOTALL)
RE_CLASS_TITLE  = re.compile('<table .*?class="class-title">(.+?)</table>')
RE_CLASS_NAME   = re.compile('<td class="class-name">(.+?)</td>', re.DOTALL)
RE_CLASS_INFO   = re.compile('<td class="class-number">(.+?)</td><td class="class-location">(.+?)</td><td class="class-schedule">(.+?)</td>', re.DOTALL)

year     = 2015
term     = 2
graduate = 0
urlp      = 'http://www.mathcs.emory.edu/classes-semester.php?subject=CS&year=%d&term=%d&graduate=%d' % (year, term, graduate)

requestp  = urllib2.Request(urlp)
responsep = urllib2.urlopen(requestp)
pagep     = responsep.read()
kb       = dict()

mp = RE_CLASSES_MAIN.search(pagep)
mainp = mp.group(1)

titlesp = [(mp.group(1), mp.start(), mp.end()) for mp in RE_CLASS_TITLE.finditer(mainp)]

def splitTitle(title):
    name = RE_CLASS_NAME.search(title).group(1)
    tp = name.split(':')
    cnum = ''.join(tp[0].split())
    cdes = tp[1].strip()
    return (cnum, cdes)

coursesInfo = []
for i, titlep in enumerate(titlesp):
    (course_number, course_title) = splitTitle(titlep[0])

    start = titlep[2]
    if i+1 < len(titlesp): end = titlesp[i+1][1]
    else: end = -1

    for m1 in RE_CLASS_INFO.finditer(mainp, start, end):
        section  = m1.group(1).strip()
        if section.find("L") == -1:
            location = m1.group(2).strip()
            schedule = m1.group(3).strip()
            if course_number == 'CS130R':
                schedule = "MW "+schedule[2:]
            for t in finalsSchedule:
                if t[0] == " ".join(schedule.split()[:1]) and t[1] == (" ".join(schedule.split()[1:2]))[:-2]:
                    k = (course_number+section).upper()
                    kb[k] = (course_number,section,location, schedule, t[2], t[3])

k = ("CS1")
kb[k] = ("COURSE","SECTION","LOCATION","CLASS HOURS","FINAL DATE","FINAL HOURS")

keys = kb.keys()

keys.sort()
for k in keys:
    print('{:>8} {:>8}    {:>10}      {:>10}         {:>1}           {:>1}'.format(*kb[k]))