'''
Conceptual replication of Gardner & Java (1990)

- study 60 words (1/2 words, 1/2 non-words) in random order
- 10-15 minute delay filled with a distractor task
- recognition test: items presented one at a time. Old/New judgement with old judgements
  followed by a R/K classification. Both done via click
'''

from psychopy import visual, core, event, gui, data
import random, os
from math import floor

try:
    import win32api
except:
    pass

'''
WORDS = ['ABLE', 'ADAM', 'ALEC', 'ALSO', 'AREA', 'ARMY', 'ATOM', 'AUNT', 'AUTO', 'AWAY', \
'AXIS', 'BABY', 'BACK', 'BALL', 'BAND', 'BANK', 'BARE', 'BARN', 'BASE', 'BATH', \
'BEAM', 'BEAR', 'BEAT', 'BEEF', 'BEEN', 'BEER', 'BELT', 'BEND', 'BENT', 'BEST', \
'BILL', 'BIRD', 'BLOW', 'BLUE', 'BOAT', 'BODY', 'BOLD', 'BOMB', 'BOND', 'BONE', \
'BOOK', 'BORE', 'BORN', 'BOSS', 'BOTH', 'BOWL', 'BUCK', 'BUSY', 'CADY', 'CAFE', \
'CALL', 'CALM', 'CAME', 'CAMP', 'CAPE', 'CARD', 'CARE', 'CARL', 'CASE', 'CASH']
NONWORDS = [''.join(sorted(WORDS[i])) for i in range(len(WORDS))]
'''

WORDS = ['BATH', 'BEEF', 'BIRD', 'BLUE', 'BOOK', 'CAKE', 'CALL', 'COAT', 'COLD', 'DATE', \
'DOOR', 'FACE', 'FACT', 'FEET', 'GIRL', 'GOOD', 'HALF', 'HALL', 'HAND', 'HAVE', \
'HEAD', 'HELP', 'HOLD', 'HOME', 'KISS', 'KNEE', 'LEFT', 'LIFE', 'LIKE', 'LINE', \
'LOOK', 'MAKE', 'MIND', 'NOTE', 'PAGE', 'RAIN', 'REST', 'ROAD', 'ROOM', 'SALT', \
'SEAT', 'SELF', 'SHOP', 'SKIN', 'SNOW', 'SOAP', 'SOFT', 'SONG', 'TALK', 'TIME', \
'TREE', 'WALK', 'WANT', 'WARM', 'WASH', 'WIND', 'WORK', 'YEAR', 'GATE', 'CASH']

NONWORDS = ['wuil', 'rilm', 'denc', 'zyse', 'lodd', 'chie', 'sefs', 'jauk', 'gwic', 'wone', \
'plok', 'dapt', 'rete', 'klib', 'sime', 'latt', 'swaz', 'dufe', 'wons', 'hewf', \
'menc', 'zunk', 'colv', 'clof',  'abst', 'yogg', 'dauv', 'veul', 'hoab', 'doys', \
'spiz', 'narn', 'zelf', 'yail', 'cweb', 'noge', 'wonc', 'dwek', 'zarc', 'gwuz', \
'naln', 'hesp', 'jalt', 'ufts', 'cwul', 'keph', 'myde', 'sote', 'chur', 'fomb', \
'fosk', 'truv', 'snuz', 'tasp', 'nauc', 'vabb', 'zeam', 'tuce', 'josp', 'lort']

NONWORDS = [i.upper() for i in NONWORDS]


MONITOR = 'monitor1'
WINSIZE = [1920, 1080]
INSTRTEXTSIZE=.7
TEXTSIZE=2
BACKGROUND=[.5,.5,.5]
FOREGROUND=[-1,-1,-1]
WORDCOL = [-1,-1,-1]
BUTTONCOL = [-1, .5, .5]
BUTTONPOS = [5, -5]
QUITKEY='escape'

SAVELOC = 'RKN_replication/RKN_exp1/'

### INSTRUCTIONS

study_instructions = "In this experiment you will be presented with strings of 4 letters to remember. \
Sometimes these letters will make a word (for example, CAPE), or sometimes they will be a 'non-word', which is word-like \
but has no meaning (for example, LARC). Each item (word or non-word) will be presented one at a time in the middle of the screen. \
Pay close attention to each and try to remember them. Once you have studied all of the items \
you will be given another task to do for 10 minutes. After that you will be given a recognition test. \
\n\nPress SPACE to begin."

delay_instructions = "Now you have 10 minutes to complete another task. Ask the researcher."

test_instructions1 = "Now is the memory test for the words and non-words you studied before. \
You will see a single item at a time; some of these will be from the set you studied in the \
first part of the experiment (OLD), others will be ones you did not study (NEW). \
Please work carefully through each item, indicating for each one whether you recognize \
it from the first part of the study or not. If you recognize an item, please click the OLD button. \
If you do not recognize it, plase click the NEW button.\n\nPress SPACE to continue"

test_instructions2 = "Additionally, as you make your decision about recognizing each word/ non-word, \
bear in mind the following: \
Often, when remembering a previous event or occurence, we consciously \
RECOLLECT and become aware of aspects of the previous experience. \
At other times, we simply KNOW that something has occurred \
before, but without being able consciously to recollect anything about \
its occurrence or what we experienced at the time.\n\nPress SPACE to continue"

test_instructions3 = "Thus in addition to your indicating your recognition of a word/ non-word from \
the original study set, you will be asked to click 'R' to show that \
you recollect the item consciously, or click 'K' if you feel you simply \
know that the item was in the previous study set. \
So, for each item that you recognize as OLD, please click 'R' \
if you recollect its occurrence, or 'K' if you simply know that it was \
shown in the first part of the experiment. \n\nPress SPACE to begin"

if not os.path.exists(SAVELOC):
    os.makedirs(SAVELOC)

win = visual.Window(WINSIZE, units = 'deg', allowGUI= False, color=BACKGROUND, monitor=MONITOR)

word_stim = visual.TextStim(win, color = WORDCOL, height = TEXTSIZE, pos = [0,0], wrapWidth = 20)
text_stim = visual.TextStim(win, color = FOREGROUND, height = INSTRTEXTSIZE, pos = [0,0], wrapWidth = 25)

button_1 = visual.Circle(win, radius=2, edges=64, pos=BUTTONPOS, lineColor=BUTTONCOL, fillColor=BUTTONCOL)
button_2 = visual.Circle(win, radius=2, edges=64, pos=[-BUTTONPOS[0], BUTTONPOS[1]], lineColor=BUTTONCOL, fillColor=BUTTONCOL)

button_text_1 = visual.TextStim(win, color = WORDCOL, height = 1, pos = BUTTONPOS, wrapWidth = 20)
button_text_2 = visual.TextStim(win, color = WORDCOL, height = 1, pos = [-BUTTONPOS[0], BUTTONPOS[1]], wrapWidth = 20)

buttons = [button_1, button_2]

myMouse = event.Mouse(win = win)
RT = core.Clock()

def moveMouse(x, y):
    try:
        win32api.SetCursorPos((x,y))
    except:
        pass

def pressToBegin(text = 'Press SPACE to begin', k = 'space'):
    text_stim.setText(text)
    text_stim.draw()
    win.flip()
    key = event.waitKeys(keyList = [k, QUITKEY])[0]
    if key == QUITKEY:
        core.quit()
    else:
        pass


def makeStudyTestLists(N_of_each = 30):
    if len(WORDS) != N_of_each*2 or len(NONWORDS) != N_of_each*2:
        raise(Warning("Error in makeStudyTestLists: not enough stimuli provided"))

    studied_words = random.sample(WORDS, N_of_each)
    studied_nonwords = random.sample(NONWORDS, N_of_each)

    study_list = studied_words + studied_nonwords

    random.shuffle(study_list)

    test_list = []
    for w in WORDS:
        if w in studied_words:
            test_type = 'old'
            study_pos = study_list.index(w) + 1
        else:
            test_type = 'new'
            study_pos = "NA"

        test_list.append({'item': w, 'item_type': 'word', 'test_type': test_type, 'study_pos': study_pos})

    for nw in NONWORDS:
        if nw in studied_nonwords:
            test_type = 'old'
            study_pos = study_list.index(nw) + 1
        else:
            test_type = 'new'
            study_pos = "NA"

        test_list.append({'item': nw, 'item_type': 'nonword', 'test_type': test_type, 'study_pos': study_pos})

    random.shuffle(test_list)

    return(study_list, test_list)


def countdown(duration = 10):

    duration_s = duration*60

    timer = core.CountdownTimer(duration_s)

    while timer.getTime() > 0:
        time = timer.getTime()
        mins = int(floor(time/60.0))
        secs = int(round(time % 60))

        if secs < 10:
            secs = '0' + str(secs)
        if secs == 60:
            secs = '00'
            mins += 1

        text_stim.setText('%s:%s' %(mins, secs))
        text_stim.draw()
        win.flip()

        for key in event.getKeys():
            if key == QUITKEY:
                core.quit()


def drawButtons(RK = True):
    '''
    RK = True = remember know response
    False = Old New response
    '''
    if RK:
        button_text_1.setText('R')
        button_text_2.setText('K')
    else:
        button_text_1.setText('OLD')
        button_text_2.setText('NEW')

    button_1.draw(); button_2.draw()
    button_text_1.draw(); button_text_2.draw()


def getClick():
    RT.reset()
    moveMouse(WINSIZE[0]/2.0, WINSIZE[1]/2.0)
    win.setMouseVisible(True)
    response_made = False
    while not response_made:
        # get mouse click + return the object clicked in
        for b in buttons:
            if myMouse.isPressedIn(b, buttons=[0]):
                choice = buttons.index(b)
                response_made = True
                # dont advance until the mouse is released
                while myMouse.getPressed()[0]:
                    pass
        for key in event.getKeys():
            if key == QUITKEY:
                core.quit()

    responseTime = RT.getTime()
    win.setMouseVisible(False)

    return(choice, responseTime)


def study(study_list, study_time=2, ISI=.5):
    for i in study_list:
        word_stim.setText(i)
        word_stim.draw()
        win.flip()
        core.wait(study_time)
        win.flip()
        core.wait(ISI)


def recognition(test_list, ID=999):
    # create the data file?

    data_file = open(SAVELOC + "P" + str(ID) + '_RKN.csv', 'w')
    data_file.write('ID, item, item_type, test_type, study_pos, ON_resp, ON_RT, RK_resp, RK_RT \n')

    for i in test_list:
        word_stim.setText(i['item'])
        word_stim.draw()
        drawButtons(RK=False)
        win.flip()
        # wait for mouse click
        oldNew_resp, oldNew_RT = getClick()
        # if old collect another click (0 = OLD, 1 = NEW)

        if oldNew_resp == 0:
            word_stim.draw()
            win.flip(); core.wait(.2)
            word_stim.draw()
            drawButtons(RK=True)
            win.flip()
            RK_resp, RK_RT = getClick()
            RK_resp = ['R', 'K'][RK_resp]
        else:
            RK_resp = 'N'
            RK_RT = "NA"

        win.flip()
        core.wait(.5)

        data_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %(ID, i['item'], i['item_type'], \
        i['test_type'], i['study_pos'],\
        ['old', 'new'][oldNew_resp], oldNew_RT, RK_resp, RK_RT))

    data_file.close()


def main():
    expInfo = {'ID' : 0, 'Gender' :'f', 'Age' : 0}
    expInfo['dateStr'] = data.getDateStr()

    dlg = gui.DlgFromDict(expInfo, title = "Participant Info", fixed = ['dateStr'], order=['ID', 'Age', 'Gender'])
    if dlg.OK:
        LogFile = "participant_info"
        infoFile = open(SAVELOC + LogFile + '.csv', 'a')
        infoFile.write('%s,%s,%s,%s\n' %(expInfo['ID'], expInfo['Gender'], expInfo['Age'], expInfo['dateStr']))
        infoFile.close()
    else:
        core.quit()

    study_list, test_list = makeStudyTestLists(N_of_each = 30)

    pressToBegin(text = study_instructions)
    win.flip(); core.wait(1)
    study(study_list = study_list)

    # delay
    pressToBegin(text = delay_instructions)
    countdown()

    pressToBegin(text = test_instructions1)
    pressToBegin(text = test_instructions2)
    pressToBegin(text = test_instructions3)
    win.flip(); core.wait(1)
    recognition(test_list = test_list, ID=expInfo['ID'])


main()

### END

# instructions from gardiner and java

'''
In this test there are four columns of words; some of these words
are from the cards you studied in the first part of the experiment, others
are not.
Please work carefully down each column, indicating for each successive
word whether you recognize it from the study cards or not. If
you recognize a word, please encircle it.
Additionally, as you make your decision about recognizing a word,
I would like you to bear in mind the following:
Often, when remembering a previous event or occurence, we consciously
recollect and become aware of aspects of the previous experience.
At other times, we simply Iarow that something has occurred
before, but without being able consciously to recollect anything about
its occurrence or what we experienced at the time.
Thus in addition to your indicating your recognition of a word from
the original study set, I would like you to write either the letter "R"
after the encircled item, to show that you recollect the word consciously,
or "K" if you feel you simply know that the word was in the previous
study set.
So, for each word that you recognize, please write "R" next to it
if you recollect its occurrence, or "K" if you simply know that it was
shown on the cards.
'''
