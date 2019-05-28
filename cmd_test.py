import sys
import re


def replace_all(t, d):
    """Общая функция для подмены переменных"""
    for i, j in d.items():
        t = t.replace(i, j, 1)
    return t

def get_datex(text):
    """Извлекает из текста дату и подстроку с датой, которую нужно удалить"""
    whatdate = ''
    delwhatdate = ''
    datex = re.findall(r'\d{2}[.,-]\d{2}[.,-]\d{4}|\d{1}[.,-]\d{2}[.,-]\d{4}', text)  # ищем дату в формате 19.08.2014 или 19-08-2014 или 19,08,2014
    if datex:
        date = datex[0].replace('-', '.').replace(',', '.')  # преобразуем дату в формат 19.08.2014
        whatdate = date
        delwhatdate = datex[0]+' '
    return whatdate, delwhatdate

def get_day(text):
    """Извлекает из текста день недели и подстроку, которую нужно удалить"""
    when = ''
    delday = ''

    day = re.findall('завтра|в понедельник|во вторник|в среду|в четверг|в пятницу|в субботу|в воскресенье', text)

    daywithoutin = re.findall('понедельник|вторник|среда|четверг|пятница|суббота|воскресенье', text)
    if day:
        ind = {'завтра': 'tomorrow', 'Завтра': 'tomorrow', 'в понедельник': 'mon', 'во вторник': 'tue', 'в среду':'wed',
               'в четверг': 'thu', 'в пятницу': 'fri', 'в субботу': 'sat', 'в воскресенье': 'sun'}
        when = replace_all(day[0], ind)
        delday = day[0]+' '
    elif daywithoutin:
        ind = {'понедельник': 'mon', 'вторник': 'tue', 'среда': 'wed', 'четверг': 'thu', 'пятница': 'fri',
               'суббота': 'sat', 'воскресенье': 'sun'}
        when = replace_all(daywithoutin[0], ind)
        delday = daywithoutin[0]+' '
    return (when, delday)

def get_clock(text):
    """Извлекает из текста время и подстроку, которую нужно удалить"""
    how = ''
    delclock = ''
    clock = re.findall('минуты |часа |дня |минуту |часов |день |минут |час |дней ', text)
    if clock: # смотрим, есть ли указание на часы, минуты, дни
        clockbank = {'минут ': 'min', 'час ': 'hour', 'дней ': 'days', 'минуту ': 'min', 'часа ': 'hours',
                     'дня ': 'days', 'минуты ': 'min', 'часов ': 'hours', 'день ': 'days'}
        how = replace_all(clock[0], clockbank)
        delclock = clock[0]
    return (how, delclock)


def extract_date(str):
    get = str.lower()  # получаем текст
    text = get + ' '  # добавляем в конец пробел, чтобы отрабатывать уведомления типа "напомнить мне через 10 минут". Если бы пробела не было, параметр clock был бы пуст. В параметре clock после слова "час" тоже стоит пробел, чтобы различать поиск "час" и "часов".
    find = re.findall('ерез [0-9]+|В [0-9:-]+|в [0-9:-]+|ерез час', text)

    if not get:
        return

    if find:  # убеждаемся, указано ли время напоминания
        what = find[0].split()
        timex = what[1].replace('-', ':').replace('час', '1')
    else:
        return

    if len(timex) > 2:  # заменяет выражения типа "в 10" на "в 10:00"
        time = timex
    else:
        time = timex + ':00'

    whatdate, delwhatdate = get_datex(text)
    when, delday = get_day(text)
    how, delclock = get_clock(text)

    reps = {'ерез': 'at now + %s %s' % (timex, how), 'в': 'at %s %s %s' % (time, when, whatdate)}
    wors = {'через %s %s' % (what[1], delclock): '', 'в %s ' % what[1]: '', '%s' % delday: '', 'через час': '',
            '%s' % delwhatdate: '', }  # какие слова мы будем удалять
    x = replace_all(what[0], reps)  # это время, на которое запланировано появление напоминания
    out = replace_all(text, wors)  # это текст напоминания

    return [reps,wors,x,out]


if __name__ == "__main__":
    data = extract_date(sys.argv[1])
   # print(sys.argv[1])
    #print('###'*30)
    #print(data)

    #print('reps='+str(data[0]))
    #print('wors='+str(data[1]))
    try:
        print('when=' + str(data[2]))
        print('text=' + str(data[3]))
    except:
        print(data)
