'''
Conceptual replication of Gardner & Java (1990)

Experiment 3:
    - Using the stimuli and instructions from
    Rajaram et al. (2002, Cogn Aff Behav Neurosci) &
    Geraci et al. (2009, Consci Cogn)
'''

from psychopy import visual, core, event, gui, data
import random, os
from math import floor

try:
    import win32api
except:
    pass

'''
Stimuli from:
    Rajaram, S., Hamilton, M., & Bolton, A. (2002). Distinguishing states of awareness
    from confidence during retrieval: Evidence from amnesia. Cognitive, Affective, &
    Behavioral Neuroscience, 2(3), 227-235.

Also include the original stimuli from Gardiner and Java (1990).
Provided by Dr Rajaram. If you use these stimuli, please cite the original articles
'''

WORDS = [
'bean', 'limb', 'gate', 'foam', 'wash', 'bomb', 'hang', 'card', 'bend', 'jump', \
'fare', 'bail', 'salt', 'bond', 'hair', 'meet', 'pain', 'king', 'tune', 'bite', \
'coat', 'iron', 'drip', 'fern', 'date', 'race', 'home', 'part', 'year', 'come', \
'sink', 'worn', 'hall', 'hear', 'desk', 'cell', 'back', 'much', 'seat', 'dear', \
'cook', 'sold', 'male', 'fool', 'safe', 'pale', 'game', 'test', 'bird', 'maid', \
'boat', 'hill', 'loaf', 'dove', 'leaf', 'silk', 'dust', 'song', 'wall', 'fine'
]

WORDS = [i.upper() for i in WORDS]

NONWORDS = [
'abst', 'igst', 'ortt', 'afth', 'farb', 'hirp', 'klib', 'slig', 'tade', 'pate', \
'inps', 'orks', 'blos', 'tras', 'josp', 'cadt', 'aelt', 'ourt', 'sote', 'pige', \
'doot', 'geel', 'hipt', 'pift', 'glaf', 'jasl', 'filt', 'nist', 'knoo', 'slee', \
'flou', 'spoa', 'gort', 'bopt', 'nost', 'lobt', 'delp', 'noph', 'ginp', 'dopt', \
'bilp', 'filk', 'ilst', 'olnd', 'nort', 'folt', 'lopt', 'nulb', 'chur', 'trob', \
'egst', 'tolr', 'ahll', 'obll', 'selb', 'tilb', 'lort', 'lont', 'inpt', 'onlt'
]

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

SAVELOC = 'RKN_replication/RKN_exp3/'

if not os.path.exists(SAVELOC):
    os.makedirs(SAVELOC)

# separate folders for the remember know (RK) and sure unsure (SU) conditions
if not os.path.exists(SAVELOC + 'RK/'):
    os.makedirs(SAVELOC + 'RK/')
#if not os.path.exists(SAVELOC + 'SU/'):
#    os.makedirs(SAVELOC + 'SU/')


def moveMouse(x, y):
    try:
        win32api.SetCursorPos((x,y))
    except:
        x = x - WINSIZE[0]/2
        y = y - WINSIZE[1]/2
        myMouse.setPos((x,y))



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


def drawButtons(bttns = "ON"):
    '''
    RK = remember know response
    ON = Old New response
    SU = sure/ unsure
    '''
    if bttns not in ['ON', 'RK', 'SU']:
        raise(Warning("Error in drawButtons: buttons must be 'ON', 'RK', or 'SU'"))

    if bttns == 'RK':
        button_text_1.setText('R')
        button_text_2.setText('K')
    if bttns == 'ON':
        button_text_1.setText('OLD')
        button_text_2.setText('NEW')
    if bttns == 'SU':
        button_text_1.setText('S')
        button_text_2.setText('U')

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

        for key in event.getKeys():
            if key == QUITKEY:
                core.quit()


def recognition(test_list, rating = "RK", ID=999):
    if rating not in ['RK', 'SU']:
        raise(Warning("Error in recognition: rating must be 'RK' or 'SU'"))

    # create the data file?
    data_file = open(SAVELOC + rating + "/P" + str(ID) + '_RKN_' + expInfo['dateStr'] + '.csv', 'w')
    data_file.write('ID, item, item_type, test_type, study_pos, ON_resp, ON_RT, rating_resp, rating_RT \n')

    acc=[]
    for i in test_list:
        word_stim.setText(i['item'])
        word_stim.draw()
        drawButtons(bttns="ON")
        win.flip()
        # wait for mouse click
        oldNew_resp, oldNew_RT = getClick()
        # if old collect another click (0 = OLD, 1 = NEW)

        # only collect rating after old response
        if oldNew_resp == 0:
            if i['test_type']=='old':
                acc.append(1)
            else:
                acc.append(0)

            if rating == 'RK':
                word_stim.draw()
                win.flip(); core.wait(.2)
                word_stim.draw()
                drawButtons(bttns=rating)
                win.flip()
                rating_resp, rating_RT = getClick()
                rating_resp = ['R', 'K'][rating_resp]
            if rating == 'SU':
                word_stim.draw()
                win.flip(); core.wait(.2)
                word_stim.draw()
                drawButtons(bttns=rating)
                win.flip()
                rating_resp, rating_RT = getClick()
                rating_resp = ['S', 'U'][rating_resp]
        else:
            rating_resp = 'N'
            rating_RT = "NA"

            if i['test_type']=='new':
                acc.append(1)
            else:
                acc.append(0)

        win.flip()
        core.wait(.5)

        data_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %(ID, i['item'], i['item_type'], \
        i['test_type'], i['study_pos'],\
        ['old', 'new'][oldNew_resp], oldNew_RT, rating_resp, rating_RT))

    return(acc)
    data_file.close()


def main():
    global expInfo
    expInfo = {'ID' : 0, 'Gender' :'m/f', 'Age' : 0, 'Condition': ['RK']} # 'Condition': ['RK','SU']}
    # condition RK = remember/know, no sure/unsure in this experiment
    expInfo['dateStr'] = data.getDateStr()

    dlg = gui.DlgFromDict(expInfo, title = "Participant Info", fixed = ['dateStr'], order=['ID', 'Age', 'Gender', 'Condition'])
    if dlg.OK:
        cond = expInfo['Condition']
        LogFile = "participant_info"
        infoFile = open(SAVELOC + LogFile + '.csv', 'a')
        infoFile.write('%s,%s,%s,%s,%s\n' %(expInfo['ID'], expInfo['Gender'], expInfo['Age'], expInfo['dateStr'], cond))
        infoFile.close()
    else:
        core.quit()

    global win
    win = visual.Window(WINSIZE, units = 'pix', allowGUI= True, color=BACKGROUND, monitor=MONITOR, fullscr=True)

    global word_stim, text_stim, button_1, button_2, button_text_1, button_text_2, buttons
    global myMouse, RT
    word_stim = visual.TextStim(win, color = WORDCOL, height = TEXTSIZE, units = 'deg', pos = [0,0], wrapWidth = 20)
    text_stim = visual.TextStim(win, color = FOREGROUND, height = INSTRTEXTSIZE, units = 'deg', pos = [0,0], wrapWidth = 25)

    button_1 = visual.Circle(win, radius=2, edges=64, pos=BUTTONPOS, units = 'deg', lineColor=BUTTONCOL, fillColor=BUTTONCOL)
    button_2 = visual.Circle(win, radius=2, edges=64, pos=[-BUTTONPOS[0], BUTTONPOS[1]], units = 'deg', lineColor=BUTTONCOL, fillColor=BUTTONCOL)

    button_text_1 = visual.TextStim(win, color = WORDCOL, height = 1, pos = BUTTONPOS, units = 'deg', wrapWidth = 20)
    button_text_2 = visual.TextStim(win, color = WORDCOL, height = 1, pos = [-BUTTONPOS[0], BUTTONPOS[1]], units = 'deg', wrapWidth = 20)

    buttons = [button_1, button_2]

    myMouse = event.Mouse(win = win)
    RT = core.Clock()

    ### INSTRUCTIONS
    study_instructions = "In this experiment you will be presented with strings of 4 letters to remember. \
Sometimes these letters will make a word (for example, CAPE), or sometimes they will be a 'non-word', which is word-like \
but has no meaning (for example, LARC). Each item (word or non-word) will be presented one at a time in the middle of the screen. \
Pay close attention to each and try to remember them. Once you have studied all of the items \
you will be given another task to do for 10 minutes. After that you will be given a recognition test. \
\n\nPress SPACE to continue."

    delay_instructions = "Now you have 10 minutes to complete another task. Ask the researcher.\n\nThey will begin the 10 minute timer."

    test_instructions1 = "The researcher will now read the instructions for the memory test to you.\n\nPress SPACE when finished"
    # researcher then reads instructions adapted from Geraci et al. (2009) experiment 1

    if cond == 'RK':
        test_instructions2 = "Remember, if you recognize the item click 'OLD' and if you do not recognize the item \
click 'NEW'.\n\nAfter an 'OLD' response click 'R' if you remember the item or click 'K' if you know the item.\n\nPress SPACE to begin"

    if cond == 'SU':
        # this condition is not run in this experiment
        pass
        '''
        test_instructions2 = "After you decide an item is old, we would like you to tell us \
how sure you are in your decision.  If you are very sure it is old, that is you might even \
bet a lot of money on it, hit the 'S' button for 'sure'.  If you are not quite this sure, \
that is, you wouldn't want to bet on it, hit the 'U' button for 'unsure.'\n\nPress SPACE to begin"
        '''

    study_list, test_list = makeStudyTestLists(N_of_each = 30)

    pressToBegin(text = study_instructions)
    pressToBegin(text = "You will now study the words and non-words. Focus on each item as it appears and try to remember it.\n\nPress SPACE when you are ready to begin.")
    win.flip(); core.wait(1)
    study(study_list = study_list)

    # delay
    pressToBegin(text = delay_instructions)
    countdown()

    pressToBegin(text = test_instructions1)
    pressToBegin(text = test_instructions2)
    #pressToBegin(text = "Researcher Instructions")
    #pressToBegin(text = "We will now begin the test\n\nPress SPACE when you are ready to begin")
    win.flip(); core.wait(1)
    acc=recognition(test_list = test_list, rating=cond, ID=expInfo['ID'])
    pressToBegin(text = "End of Experiment!\n\nYou got %i out of %i correct!\n\nPlease let the researcher know you are done." %(sum(acc), len(acc)))


main()
