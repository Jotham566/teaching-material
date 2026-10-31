"""Spoken-script speaker notes for the automatic slides.

Notes are what the instructor says aloud, in the first person, in plain words for 15 to 19 year olds. There are no
stage directions, no labels and no sources in them. Where a question is asked, the paragraph ends on the pause and the
answer comes in the next paragraph. Wording rotates by slide so a deck does not repeat the same stock phrase.
"""
import re

PROTECTED = {'Python', 'NumPy', 'Jupyter', 'DataFrame', 'CSV', 'Sunrise', 'Uganda', 'Kampala', 'Nakawa', 'Keras', 'Book', 'Pen', 'Juice',
             'Central', 'Campus', 'Roadside', 'UGX', 'Predict', 'Run', 'Modify', 'Make', 'Investigate', 'Block', 'Words', 'Today', 'Mondays'}


def lower_first(s):
    if not s:
        return s
    first = re.split(r'\W', s.strip(), maxsplit=1)[0]
    if first in PROTECTED or any(c.isupper() for c in first[1:]) or first.isupper():
        return s
    return s[:1].lower() + s[1:]


def pick(options, seed):
    return options[seed % len(options)]


def sentences(text):
    return [x for x in re.split(r'(?<=[.!?])\s+', text.strip()) if x]


def strip_prefix(objective):
    for pre in ('By the end: you can ', 'By the end: you '):
        if objective.startswith(pre):
            return objective[len(pre):].rstrip('.')
    return objective.rstrip('.')


LEAD_IN = ['Welcome back.', 'Good to see you.', 'Laptops open, please.', 'Let us begin.', 'Here we go.']


def title_note(ident, title, objective, question, seed):
    return (f'{pick(LEAD_IN, seed)} Today is session {int(ident[2:]) if ident[2:].isdigit() else ident} and our topic is {lower_first(title)}.\n\n'
            f'By the end of today you will be able to {strip_prefix(objective)}.\n\n'
            f'We will answer one question: {question}')


def question_note(question, seed):
    return (f'Here is the question for today. {question}\n\n'
            f'Look at the picture and tell me what you notice. We will come back to this question at the end of the session and see how much more we can say about it.')


def plan_note(parts, seed, mode='python', caption=''):
    order = ['First', 'Then', 'After that', 'Next', 'Then', 'Then', 'Last']
    total = sum(m for _, m in parts)
    out = [f'Here is how the {total // 60 if total % 60 == 0 else total} {"hours" if total % 60 == 0 else "minutes"} go. Each bar is as long as the time we spend on that part.']
    sents = []
    for i, (label, m) in enumerate(parts):
        label = label.split(':')[0] if ':' in label and len(label.split(':')[0]) > 3 and mode == 'python' else label
        lab = lower_first(label.replace(':', ',')).rstrip('.')
        sents.append(f'{order[min(i, len(order) - 1)]}, {m} minutes. {lab[:1].upper() + lab[1:]}.')
    out.append(' '.join(sents))
    if mode == 'python':
        out.append('Notice how much of the time is yours. You listen for a short while and then you do. That is on purpose, because you learn this by doing it.')
    else:
        out.append(caption + ' Ask me now if any part of the plan is unclear.')
    return '\n\n'.join(out)


WORD_INTRO = ['We need a few words today. For each one I will say what it means and give you something to picture.',
              'Here are the words for today. Listen for the picture that goes with each one.',
              'First the words, because every one of them is used in the code later.']
WORD_INTRO_2 = ['More words for today.', 'Two more words to know before we start.', 'Here are the rest of today\'s words.']
PICTURE = ['Picture this.', 'Think of a shop.', 'Here is a way to see it.', 'You have seen this before.', 'Imagine it like this.', 'A small example.', '', 'An example from everyday life.']


def words_note(words, page, pages, seed):
    out = [pick(WORD_INTRO, seed) if page == 0 else pick(WORD_INTRO_2, seed)]
    for i, (term, plain, like) in enumerate(words):
        p = pick(PICTURE, seed + i * 3 + page)
        out.append(f'{term}. {plain}' + (f' {p} {like}' if p else f' {like}'))
    return '\n\n'.join(out)


READ_FIRST = ['Look at this code with me before we run it.', 'Read this code slowly first, quietly, in your head.',
              'Let us read these lines together before anything runs.', 'Here is the code. Read it line by line.',
              'Before we run anything, read the code once through.']
GUESS = ['Now your guess.', 'Time to commit to an answer.', 'This is the part where you decide.', 'Your turn to guess.', 'Make a prediction.']
ON_PAPER = ['Write it on paper. It does not have to be right.', 'Put it on paper first. We will check it together in a moment.',
            'Put your guess on paper now, even if you are unsure.', 'Write one line on paper. I will give you a minute.', 'Jot it on paper before anyone speaks.',
            'Guess on paper first. Surprises are useful.']
PAUSE = ['Think about it for a moment, then tell the person next to you.', 'Have a go in your head first.', 'Write your answer in one line before we compare.',
         'Say it quietly to yourself before anyone answers.', 'Give it thirty seconds and then we will hear a few answers.', 'Talk it over with your neighbour for a minute.']
INSTRUCTION = re.compile(r'\b(press|click|open|type|shift|enter|run the|save)\b', re.I)


def predict_note(intro, predict, seed):
    keep = [s for s in sentences(intro) if not INSTRUCTION.search(s)]
    body = ' '.join(keep[:2]) if keep else pick(READ_FIRST, seed)
    return f'{body}\n\n{pick(GUESS, seed + 1)} {predict} {pick(ON_PAPER, seed + 2)}'


RUN_LEAD = ['Now we run it.', 'Let us see what happens.', 'I will run it, and you compare with your guess.', 'Running it now.', 'Watch the output as it appears.']
RUN_CLOSE = ['Tell the person next to you whether your guess matched.', 'If your guess was off, find the line that surprised you.',
             'Which line of the output matches which line of the code? Point to each pair.', 'Check your paper. Were you close?', 'Keep your guess. We use it in the next step.']


def run_note(shows, seed):
    return f'{pick(RUN_LEAD, seed)} Match each line of the output with the line of code that made it.\n\n{shows}\n\n{pick(RUN_CLOSE, seed + 1)}'


ANSWER = ['Here is how I would answer it. {a}', 'The answer is this. {a}', 'What I would say is this. {a}', '{a}', 'Let me answer it. {a}']


def investigate_note(idea, qa, seed):
    paras = [f'Now we look closely at {lower_first(idea)}. I have {"two" if len(qa) == 2 else "three"} questions for you.']
    for i, (q, a) in enumerate(qa):
        paras.append(f'Question {["one", "two", "three"][i]}. {q} {pick(PAUSE, seed + i)}')
        paras.append(pick(ANSWER, seed + i * 2 + 1).format(a=a))
    return '\n\n'.join(paras)


MOD_LEAD = ['Now it is your turn to change something.', 'Change one thing and watch what happens.', 'Time to experiment.', 'Make one small change.', 'Your hands on the keyboard now.']
MOD_TELL = ['When you have run it, tell your neighbour what changed and how you know.', 'Then explain to your neighbour what the change did.',
            'After you run it, say in one sentence what changed and how you checked.', 'Run it, then tell someone what you saw.']
MOD_ANS = ['What you should find: {a}', 'Here is what happens. {a}', 'The result: {a}', 'You should see this. {a}']


def modify_note(instruction, answer, seed):
    return f'{pick(MOD_LEAD, seed)} {instruction} {pick(MOD_TELL, seed + 1)}\n\n{pick(MOD_ANS, seed + 2).format(a=answer)}'


def make_note(ident, task, seed, part=0, parts=1):
    if parts == 1 or part == 0:
        lead = pick(['This is your own task for today. Take it one step at a time.', 'Now you do the real work yourself. Start with the first step.',
                     'This task is yours. Run your code after every step so you can see where a problem begins.'], seed)
        return (f'{lead} If you get stuck for a few minutes, read your error message, check the error card, and then ask me.\n\n'
                f'Save it as {ident}. I will come round to each of you and ask what you changed and how you checked it.' + ('\n\nThe rest of the brief is on the next slide.' if parts > 1 else ''))
    return 'Here is the rest of the brief. Take your time, and save your work as you go, because a saved file is the only thing I can mark.'


def errors_note(errors, seed):
    paras = [pick(['Everyone meets errors, including me. Two are likely today, so let us meet them now.', 'Two things are likely to go wrong today. It helps to know them before they happen.',
                   'Here are two errors from this session, so you recognise them when they appear.'], seed)]
    intros = ['This is the first one.', 'The next one.', 'Another to watch for.']
    for i, (see, means, fix) in enumerate(errors):
        paras.append(f'{intros[min(i, 2)]} You will see: {see}. It means this: {lower_first(means).rstrip(".")}. To fix it, {lower_first(fix).rstrip(".")}.')
    paras.append(pick(['When you are stuck, read the last line of the message first.', 'Keep this slide in mind when something stops working.', 'If you meet one of these, fix it and carry on. It happens to everyone.'], seed + 1))
    return '\n\n'.join(paras)


EXIT_LEAD = ['We are nearly done. Remember the question from the start of the session:', 'Before we finish, go back to the question we began with:', 'Last step. Our question for today was:']
EXIT_DO = ['Finish this sentence in your notebook, in your own words.', 'Write this sentence in your notebook and finish it your own way.', 'Copy this sentence into your notebook and make it yours.']


def exit_note(exit_ticket, question, seed):
    return (f'{pick(EXIT_LEAD, seed)} {question}\n\n'
            f'{pick(EXIT_DO, seed + 1)} {exit_ticket}\n\n'
            f'Then save your notebook, close it and open it again to check it saved.')


def break_note(minutes, nxt, seed):
    return (f'Break time. {minutes} minutes away from your screens. Stand up, drink some water and tell someone what you guessed in the first half.\n\n'
            f'When we come back we start {lower_first(nxt)}.')
