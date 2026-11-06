"""Course Handbook: the take-home reading handed out at the end of Session 0 (Introduction).

Run from Build/:  python3 kit/make_handbook.py
Writes 03 Learner Materials/Course Handbook.docx and .pdf. Uses the KLAi Word kit and the drawn diagrams in kit/diagrams.py.
Writing rules: COURSE_BIBLE section 7 (plain words, no em dashes, no X-not-Y, no price, no exam language).
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BUILD / 'templates_gen'))
from docx_kit import *  # noqa: E402,F401,F403
import diagrams as DG  # noqa: E402

W = CONTENT_CM
BODY_SIZE = 10.5


def page_break(doc):
    p = doc.add_paragraph(); fmt(p, 0, 0)
    p.paragraph_format.page_break_before = True
    p.paragraph_format.line_spacing = Pt(1)
    r = p.add_run(''); r.font.size = Pt(1)


def to_pdf(path):
    subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_docs', '--headless', '--convert-to', 'pdf', '--outdir', str(path.parent), str(path)], capture_output=True)


def bullets(d, items, size=BODY_SIZE, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5)
        p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True)
            add_run(p, it[1], size)
        else:
            add_run(p, it, size)


def body(d, text, after=6, size=BODY_SIZE):
    return para(d, text, size, after=after)


def fig(d, data, h_in, w_in=13.0, caption=None):
    try:
        path = DG.render(data, w_in, h_in * w_in / 6.3)
    except KeyError as e:
        print('SKIPPED FIGURE', data['kind'], e)
        return
    if d.paragraphs:
        d.paragraphs[-1].paragraph_format.keep_with_next = True
    p = d.add_paragraph(); fmt(p, 2, 2 if caption else 6, keep=bool(caption))
    p.add_run().add_picture(str(path), width=Cm(16.0))
    if caption:
        para(d, caption, 8.5, italic=True, color='595959', after=8)


def section(d, num, text, new_page=True):
    if new_page:
        page_break(d)
    if not new_page:
        spacer(d, 14)
    para(d, f'Part {num}', 9.5, True, color=RED, after=0, keep=True)
    para(d, text, 18, True, after=6, keep=True)


def build():
    name = 'Course Handbook'
    d = new_doc(name)

    # ---------------------------------------------------------------- cover block and contents
    title(d, 'Course Handbook', 'Applied AI and Automation for Executives  |  KLAi Professional Learning, Kampala  |  Instructor: Jotham Martin Wambi')
    body(d, 'This handbook is yours to keep. It gives you the words and the pictures behind the course, so that you arrive at Session 1 able to follow every idea, and so that you can come back to it whenever a term needs a reminder. Read it in any order. Parts 3 to 15 explain how AI works and how to judge it. Part 16 tells you what to bring. Part 17 is a glossary. Part 18 is the fourteen sessions on one page.')
    h2(d, 'What is inside')
    grid(d, [
        ['1', 'Welcome and how the course works'],
        ['2', 'Why this introduction matters'],
        ['3', 'AI, machine learning, deep learning and generative AI'],
        ['4', 'How machines learn'],
        ['5', 'How a model is trained'],
        ['6', 'Data: the fuel and the risk'],
        ['7', 'Language models and generative AI'],
        ['8', 'Where AI is used in industry, and what suits it'],
        ['9', 'How we know a model is good'],
        ['10', 'Benchmarks'],
        ['11', 'Training and inference'],
        ['12', 'What happens when you press send'],
        ['13', 'Foundation models, open models, fine-tuning and cost'],
        ['14', 'Is our data ready for AI?'],
        ['15', 'From model to working product: workflows, agents and tools'],
        ['16', 'What to bring to Session 1'],
        ['17', 'Glossary'],
        ['18', 'The fourteen sessions at a glance'],
    ], [1.2, W - 1.2], header=['Part', 'Title'], size=10, label_cols=(0,))
    spacer(d, 6)
    box(d, 'A note on simplification', [
        'This handbook explains ideas in plain words. Where it simplifies, it says so with the word "simplified". The simple version is correct enough to make good decisions. Specialists add detail that you do not need for the work of this course.',
        'All company names and figures in examples are fictional or general. The handbook contains no statistics.'])

    # ---------------------------------------------------------------- 1 welcome
    section(d, 1, 'Welcome and how the course works')
    body(d, 'The course has fourteen sessions of two hours each, 28 hours in all. You choose the dates and the place with the instructor: in person, online or at your workplace. The group is small, from one to five executives, so the time is spent on the work you do.')
    h2(d, 'Two kinds of session')
    body(d, 'Sessions 1 to 11 explain how AI works, one idea at a time: how a machine sees, how it learns from examples, how a model is measured, how words become numbers, how language models, foundation models and open models work, how to prompt and check them, and how agents act. In each of these sessions the instructor runs live demonstrations while you watch, and you may join in on your own laptop. Each session also has a short paper exercise that needs no computer. There is no coding.')
    body(d, 'Sessions 12 to 14 are practicals. You work on your own organisation, with the instructor beside you: you map one workflow and work out the hours it could save, you write a first AI use policy and a vendor question list, and you assess how ready your information is and plan the next 90 days.')
    h2(d, 'Nothing to prepare')
    body(d, 'There is nothing to prepare before Session 1 except reading this handbook. Bring a laptop and an AI assistant account you already use, so that you can join the demonstrations if you wish. Use invented or sample information only.')
    h2(d, 'No tests and no marks')
    body(d, 'There are no tests and no required homework. Anything you do between sessions is optional. You show progress by what you understand and what you keep.')
    h2(d, 'What you keep')
    bullets(d, ['A one-page take-away sheet from every session, such as a distance cheat sheet, a decision tree for giving a model your knowledge and a boundary sheet for agents.',
                'From the practicals: your workflow map and a costed business case, a first AI use policy, a risk register and a vendor question list.',
                'A readiness scorecard, a data roadmap and a 90-day plan.',
                'The confidence to question a vendor and to supervise a pilot.'])
    h2(d, 'Automation tools', before=8)
    body(d, 'The course shows two example automations at work on the same twelve customer messages: one that routes them by plain rules, and one where an AI assistant sorts them and a person checks. You do not build either. Other tools exist and Part 15 describes some of them as options, so that you can choose well when the time comes.')
    h2(d, 'After the course')
    body(d, 'The instructor follows up with you at 30, 60 and 90 days. You return a one-page check-in form and a results tracker. The follow-up asks what is running, how much time it saves and what changed in your policy.')
    h2(d, 'How a session runs')
    fig(d, {'kind': 'bars', 'unit': ' min', 'items': [{'label': 'Recall', 'value': 10}, {'label': 'The ideas', 'value': 35}, {'label': 'Demonstrations', 'value': 25}, {'label': 'Break', 'value': 5}, {'label': 'Paper exercise', 'value': 25, 'hl': True}, {'label': 'What it means for your work', 'value': 15}, {'label': 'Close', 'value': 5}]}, 2.6, caption='The usual shape of a two-hour session in Sessions 1 to 11. In the practicals, Sessions 12 to 14, about 55 minutes go to your own work.')

    # ---------------------------------------------------------------- 2 why
    section(d, 2, 'Why this introduction matters')
    body(d, 'You cannot judge a claim, a vendor or a result unless you have the words and a picture of how the thing works. A vendor who says "our model learns from your data" or "the agent acts on its own" is saying something specific. With the picture in your head you can ask what data, learns how, and acts on what. Without the picture you can only nod.')
    body(d, 'This handbook gives you that picture once. Every idea in it comes back later in the course, taught in more depth.')
    grid(d, [
        ['Training, error and adjusting', 'Sessions 1 and 2: how a network and a tree learn from examples'],
        ['Training, validation and test data', 'Session 3: honest scores and overfitting'],
        ['Data types and data quality', 'Session 14: your information inventory and readiness scorecard'],
        ['Privacy and bias', 'Session 13: risk register and policy; Session 14: sensitive data'],
        ['Language models, tokens, context window', 'Session 5: tokens and next-word probability; Session 8: prompting'],
        ['Hallucination and retrieval', 'Session 9: giving a model your documents; Session 10: checking answers'],
        ['Prompt injection', 'Sessions 10 and 11: limits on what an agent may do'],
        ['Workflow, trigger and human in the loop', 'Session 12: mapping a workflow'],
        ['Agents and limits', 'Session 11: the Tool Boundary Sheet'],
        ['Baseline, pilot and ROI', 'Session 12: the hours-saved estimate and the business case'],
        ['Vendor and model terms', 'Sessions 6 and 7: model families and open weights; Session 13: questions for vendors'],
    ], [6.4, W - 6.4], header=['Idea in this handbook', 'Where it returns'], size=9.5, label_cols=(0,))

    # ---------------------------------------------------------------- 3 nested
    section(d, 3, 'AI, machine learning, deep learning and generative AI')
    body(d, 'These four terms are often used as if they mean the same thing. They do not. Each is a smaller part of the one before, like boxes that sit inside each other.')
    fig(d, {'kind': 'stack', 'layers': [
        {'head': 'Artificial intelligence', 'text': 'Any computer system that does something we would call intelligent', 'icon': 'gear'},
        {'head': 'Machine learning', 'text': 'Systems that learn patterns from examples', 'icon': 'bars'},
        {'head': 'Deep learning', 'text': 'Machine learning with many layers (neural networks)', 'icon': 'grid'},
        {'head': 'Generative AI', 'text': 'Deep learning that creates text, images, sound or code', 'icon': 'robot'}]}, 3.3, caption='The nested picture. Each layer is part of the one above it. Simplified: the boundaries are fuzzy in practice.')
    grid(d, [
        ['Artificial intelligence (AI)', 'A set of written rules that approves a mobile money transfer only if the amount is under a limit and the account is verified. This is old-style AI: people wrote the rules.'],
        ['Machine learning (ML)', 'A fraud detector that has studied thousands of past transactions marked "fraud" or "fine" and learned which patterns tend to go with fraud. Nobody wrote the rules by hand.'],
        ['Deep learning', 'A system that reads a photo of a maize leaf and tells you which disease it has. It uses a neural network with many layers, which suits photos, sound and language.'],
        ['Generative AI', 'An assistant that drafts a reply to a customer, summarises a board meeting or writes a first version of a policy. It generates something new each time.'],
    ], [4.4, W - 4.4], header=['Term', 'A business example'], size=10, label_cols=(0,))
    spacer(d, 6)
    body(d, 'Most of what you will use in this course is generative AI, built on deep learning, which is a kind of machine learning, which is a part of AI. When a vendor says "AI", ask which of the four they mean.', after=4)

    # ---------------------------------------------------------------- 4 how machines learn
    section(d, 4, 'How machines learn')
    body(d, 'A machine learns from experience, which for a machine means data. There are four main ways of learning. Each suits a different business problem.')
    grid(d, [
        ['Supervised learning', 'The machine studies examples that come with the right answer (a label). It learns to give the right answer for new cases.',
         'Classification: sort invoices into "fine" or "needs checking".\nRegression: predict next month\'s sales of cooking oil from the past.'],
        ['Unsupervised learning', 'No right answers are given. The machine looks for structure and finds groups on its own.',
         'Grouping 300 shops into types of buyer by how and when they order, so that each type gets a different offer.'],
        ['Reinforcement learning', 'The machine tries actions and receives a reward or a penalty. Over many tries it learns which actions pay off.',
         'Choosing delivery routes: each route that saves fuel and arrives on time earns a reward.'],
        ['Self-supervised learning', 'The machine makes its own exercise out of raw data by hiding part of it and guessing it. For text, the hidden part is the next word.',
         'The base of language models. Reading huge amounts of text and guessing the next word, again and again, is how they learn language.'],
    ], [3.6, 6.6, W - 10.2], header=['Way of learning', 'In plain words', 'A business example'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'Two words you will meet often')
    bullets(d, [('Classification', 'gives a category as the answer: spam or not spam, fraud or fine, urgent or routine.'),
                ('Regression', 'gives a number as the answer: next week\'s demand, the likely delivery time, the price.'),
                ('Clustering', 'is the unsupervised cousin: it makes the groups itself, without being told the categories.')])
    body(d, 'Simplified: real systems often mix these ways. A language model, for example, learns by self-supervised learning first and is then improved with other methods (Part 7).', after=0)

    # ---------------------------------------------------------------- 5 training
    section(d, 5, 'How a model is trained')
    body(d, 'A model is a program whose behaviour comes from numbers it has learned. No person typed in the rules. Training is the process of finding good numbers. It follows one loop, repeated millions of times.')
    fig(d, {'kind': 'cycle', 'items': ['Guess', 'Measure the error', 'Adjust', 'Repeat'], 'center': 'Training loop'}, 3.0,
        caption='The training loop. The error has a technical name, the loss. A smaller loss means better guesses.')
    h2(d, 'Parameters and weights')
    body(d, 'The numbers a model learns are called parameters. Many of them are called weights: each weight says how strongly one piece of information should influence the answer, like the volume knob on one input. A small model may have thousands of weights. The large language models behind today\'s assistants have billions. Training sets all of them.')
    h2(d, 'Gradient descent: walking downhill in fog')
    body(d, 'Imagine you stand on a hill in thick fog and want to reach the lowest point. You cannot see the valley. You feel the slope under your feet and take a small step downhill. Then you feel the slope again and take another step. Eventually the ground stops falling and you are at a low point. Gradient descent does exactly this. The "hill" is the error. The "step" is a small change to the weights. Each step makes the error a little smaller.')
    fig(d, {'kind': 'descent', 'labels': ['Start: a big error', 'Each step: adjust a little', 'Bottom']}, 2.9,
        caption='Gradient descent. At the bottom the error is the smallest the model has found. Simplified: the real hill has millions of directions, and the lowest point found is usually a good one rather than the best possible.')
    h2(d, 'Backpropagation: sharing out the blame')
    body(d, 'A neural network has layers, and an answer passes forward through all of them. When the answer is wrong, which weight is to blame? Backpropagation works that out. It starts from the error at the output and moves backward through the layers, sharing out the blame: weights that contributed more to the mistake get changed more, weights that contributed less get changed less. Then the next guess is made with the adjusted weights.')
    fig(d, {'kind': 'network'}, 3.0, caption='Forward the network guesses. Backward it shares out the blame and adjusts every connection.')
    h2(d, 'Why training needs data and computing power')
    body(d, 'The model improves only by seeing many examples, so it needs a lot of data. Each guess, error measure and adjustment is a calculation, and a large model needs a huge number of them. That takes powerful specialised computers running for days or weeks. This is why only a few organisations train the largest models, and why most companies use a model someone else trained.')
    h2(d, 'Training, validation and test data')
    body(d, 'You do not judge a model on the examples it studied. You split the data into three parts.')
    grid(d, [
        ['Training data', 'The examples the model learns from. Most of the data goes here.'],
        ['Validation data', 'Examples set aside while building. The builder uses them to compare versions and to tune settings, and they are not used for learning.'],
        ['Test data', 'A locked set, used once at the end to see how the final model does on cases it has never met. Nobody tunes the model on it, because then it would no longer be a fair check.'],
    ], [3.6, W - 3.6], header=['Part', 'What it is for'], size=10, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'Overfitting: a model that memorises')
    body(d, 'A student who memorises last year\'s answers does well on last year\'s paper and badly on a new one. A model can do the same. It can learn the training examples so closely, including their accidents and noise, that it has not learned the general pattern. This is overfitting.')
    body(d, 'This is why a model that is 99 percent right on its training data can still fail on new data. The 99 percent only says it remembers what it saw. The test data answers the real question: how does it do on cases it has not seen? A fair result on the locked test data means more than any score on the training data. Keep this in mind when anyone shows you a very high accuracy figure: ask which data it was measured on.', after=0)

    # ---------------------------------------------------------------- 6 data
    section(d, 6, 'Data: the fuel and the risk', new_page=False)
    body(d, 'Every AI system depends on data. Knowing what kind of data you hold, and how good it is, decides what AI can do for you.')
    h2(d, 'Kinds of data')
    grid(d, [
        ['Structured', 'Fits neatly in rows and columns with fixed fields.', 'A sales sheet, an invoice register, a stock list'],
        ['Semi-structured', 'Has some labels or layout but no fixed table.', 'Emails with sender, date and subject; forms; many exported files'],
        ['Unstructured', 'Free-form content without a table.', 'Photos of damaged goods, voice recordings of calls, contracts, WhatsApp messages'],
        ['Time series', 'Values recorded in time order. The order matters.', 'Daily sales, truck fuel readings, temperature sensor readings in a cold store'],
    ], [3.4, 6.2, W - 9.6], header=['Kind', 'What it looks like', 'In a company'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    body(d, 'Data can also be labelled or unlabelled. Labelled data carries the right answer: an email marked "complaint", an invoice marked "wrong total". Unlabelled data has no answer attached. Labelled data is needed for supervised learning and is usually costly, because a person has to do the marking.')
    h2(d, 'Data quality: five questions')
    fig(d, {'kind': 'icons', 'items': [
        {'icon': 'check', 'head': 'Complete', 'text': 'Nothing important is missing'},
        {'icon': 'magnifier', 'head': 'Correct', 'text': 'Values are accurate'},
        {'icon': 'calendar', 'head': 'Current', 'text': 'Up to date'},
        {'icon': 'gear', 'head': 'Consistent', 'text': 'Same format everywhere'},
        {'icon': 'people', 'head': 'Representative', 'text': 'Covers the cases you care about'}]}, 2.1)
    body(d, 'A tool fed with poor data gives poor answers, quickly and with confidence. A simple example: sales data where half the shops write "Mbale" and half write "MBL" will be counted as two places.')
    h2(d, 'Bias and where it enters')
    body(d, 'A model reflects the data it learned from. Bias means a systematic tilt that treats some cases or groups unfairly. It can enter at four points:')
    bullets(d, [('In the data collected.', 'If past hiring favoured one kind of candidate, a model trained on it will too.'),
                ('In the labels.', 'If people marked past cases unfairly, the model copies the marks.'),
                ('In who is missing.', 'If few rural customers are in the data, the model serves them badly.'),
                ('In how the result is used.', 'A sensible score used for a purpose it was not built for can still do harm.')])
    h2(d, 'Privacy and the law in Uganda', before=8)
    body(d, 'Data about identifiable people (names, phone numbers, ID numbers, health or pay details) is personal data. In my understanding, the Data Protection and Privacy Act 2019 applies to personal data, including when it goes into an AI tool; confirm your company\'s duties with a lawyer. Sessions 13 and 14 turn this into practical rules for your company.', after=0)

    # ---------------------------------------------------------------- 7 language models
    section(d, 7, 'Language models and generative AI')
    body(d, 'The assistants you use, such as ChatGPT, Claude, Gemini and Copilot, are built on large language models. A language model is a model trained on a very large amount of text to predict what comes next.')
    h2(d, 'Tokens and the next-word idea')
    body(d, 'A model does not read whole words. It splits text into small pieces called tokens. A token may be a short word, part of a long word or a punctuation mark. Given the tokens so far, the model works out which token is most likely to come next, adds it, and repeats. An answer of a hundred words is built one token at a time. Simplified: it chooses among likely tokens with a little controlled randomness, which is why the same question can give different answers.')
    h2(d, 'How a language model gets built')
    fig(d, {'kind': 'flow', 'steps': [
        {'head': 'Read', 'text': 'Learn from huge amounts of text by guessing the next token', 'icon': 'book'},
        {'head': 'Tune', 'text': 'Practise on examples of following instructions', 'icon': 'notebook'},
        {'head': 'Improve', 'text': 'People rate answers and the model is adjusted toward the good ones', 'icon': 'people'}]}, 1.9, caption='Three stages in plain words. The third is often called human feedback. Simplified: companies combine several methods.')
    h2(d, 'Context window')
    body(d, 'The context window is how much text the model can keep in view at once: your question, any files you give it, and its own answer so far. It is like the desk the model works on. If a document is larger than the desk, parts fall off, and the model may miss or mix them up. Windows are now large, but a bigger desk does not guarantee that the model attends to every part equally well.')
    h2(d, 'Why a model can sound sure and be wrong')
    body(d, 'The model is built to produce text that reads well and fits the pattern. It is not built to check facts. When it lacks the information, it can still write a smooth, confident sentence that is false. This is called a hallucination. It can include invented figures, names, quotes and sources. The tone does not tell you whether it is right. This is why the course teaches you to ask for sources, to check, and to test a tool on your own work (Session 10).')
    h2(d, 'What changes with search, files and memory')
    body(d, 'On its own, a model answers from what it learned in training, which stops at a date and knows nothing about your company. Assistants can add three things.')
    bullets(d, [('Search.', 'The assistant looks up the web and writes from what it found. You can open the sources.'),
                ('Files.', 'You give it a document and it answers from that document.'),
                ('Memory.', 'Some assistants keep notes about you between chats. Check what is kept and who can see it.')])
    body(d, 'Giving the model the right passages from your own documents before it answers is called retrieval. Think of an open-book answer: the assistant finds the relevant pages first and then writes from them. This cuts down mistakes, but does not remove them: the retrieval can fetch the wrong page, and the model can still misread the right one. Always check the answer against the source.', after=0)

    # ---------------------------------------------------------------- 8 industry
    section(d, 8, 'Where AI is used in industry')
    body(d, 'AI is used wherever there is a lot of data, a repeated decision and a cost to getting it wrong or slow. These are general examples of where it is used. They contain no statistics.')
    grid(d, [
        ['Banking and mobile money', 'Spotting unusual transactions that may be fraud; estimating the risk that a borrower will not repay; answering customer questions.'],
        ['Agriculture', 'Recognising crop diseases and pests from photos; forecasting yield and market prices; advising farmers by message.'],
        ['Retail and distribution', 'Forecasting demand for each product and shop; planning delivery routes; setting reorder points.'],
        ['Health administration', 'Scheduling and reminders; sorting and coding records; drafting letters. Clinical decisions stay with clinicians.'],
        ['Human resources', 'Sorting applications and drafting job adverts. Screening carries a bias risk, so a person must review the outcome.'],
        ['Customer service', 'Sorting incoming messages, drafting replies, finding the right policy page for the agent.'],
        ['Finance and accounting', 'Matching invoices to purchase orders; flagging duplicates and wrong totals; drafting management commentary.'],
    ], [4.6, W - 4.6], header=['Sector', 'Typical uses'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'What suits AI and what does not')
    body(d, 'Work comes in four kinds. Knowing which kind you have tells you which tool to reach for.')
    fig(d, {'kind': 'icons', 'items': [
        {'icon': 'gear', 'head': 'Rules', 'text': 'Same input, same output. Use ordinary software or a formula.'},
        {'icon': 'chart', 'head': 'Patterns', 'text': 'Find regularities in data. Use machine learning.'},
        {'icon': 'doc', 'head': 'Drafting', 'text': 'Produce a first version. Use generative AI, then check.'},
        {'icon': 'person', 'head': 'Judgement', 'text': 'Weigh people, risk and values. Keep it with a person.'}]}, 3.6)
    body(d, 'A good first task for AI is one with a clear pattern or a draft to produce, where a person can check the result quickly and a mistake is cheap to catch. A poor first task has a high cost of error, little data and nobody to check. Session 12 gives you a scorecard for this choice. A rule is often better done with a formula, which is cheaper, faster and always the same.', after=0)

    h2(d, 'The fields of AI', before=8)
    body(d, 'AI is not one skill. It is a set of fields, and each one suits a different business problem. A vendor who says they do AI should be able to say which field they work in.')
    grid(d, [
        ['Natural language processing (NLP)', 'Reads and writes human language: summarising, sorting, translating, answering.', 'Summarise emails, sort enquiries, draft replies.'],
        ['Computer vision', 'Understands images and video.', 'Read invoices, check goods in photos, count stock.'],
        ['Speech', 'Turns speech into text and text into speech.', 'Transcribe meetings and calls.'],
        ['Forecasting (time series)', 'Predicts numbers over time from past values.', 'Demand, cash flow, prices.'],
        ['Recommendation', 'Suggests what a person may want next.', 'Product suggestions, next best offer.'],
        ['Anomaly detection', 'Spots what does not fit the usual pattern.', 'Fraud alerts, faulty machines.'],
        ['Deep learning', 'A family of methods using large neural networks, behind most progress in language, vision and speech.', 'Inside most of the tools above.'],
        ['Generative AI', 'Creates new text, images, audio or code.', 'Draft reports, replies and code.'],
        ['Reinforcement learning', 'Learns by trial and reward.', 'Route planning, dynamic pricing, robots.']],
         [4.4, 7.0, W - 11.4], header=['Field', 'What it does', 'In a company'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'The jobs behind AI work', before=8)
    body(d, 'Titles vary between companies, and in a small company one person often does several of these jobs. This is the usual division.')
    grid(d, [
        ['Data engineer', 'Builds and runs the pipes that bring clean data in.', 'Session 14'],
        ['Data analyst', 'Explains what happened, with tables and charts.', 'Session 12'],
        ['Data scientist', 'Builds and tests models that predict or classify.', 'Sessions 2 and 3'],
        ['Machine learning engineer', 'Turns a model into a reliable product; deploys and monitors it.', 'Sessions 7 and 11'],
        ['MLOps engineer', 'Builds the systems that train, release and monitor models.', 'Session 7'],
        ['Applied AI engineer', 'Builds products from ready-made models with prompts, retrieval, automations and agents.', 'Sessions 8 to 11'],
        ['AI researcher', 'Invents new methods, usually in universities or large labs.', 'Not needed to start'],
        ['Data steward or information manager', 'Owns the quality and the rights of the data: who may use it, how it is kept and how it is corrected.', 'Session 14'],
        ['Product owner or AI governance lead', 'Chooses use cases, sets the rules and checks the value.', 'Sessions 12 to 14: your seat']],
         [4.6, 8.0, W - 12.6], header=['Role', 'What they do', 'Where you meet it'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    fig(d, {'kind': 'flow', 'steps': [
        {'head': 'Data engineer', 'text': 'Collects and cleans the data', 'icon': 'folder'}, {'head': 'Data analyst', 'text': 'Finds patterns and measures', 'icon': 'chart'},
        {'head': 'Data scientist', 'text': 'Trains and tests a model', 'icon': 'magnifier'}, {'head': 'ML engineer', 'text': 'Deploys and monitors it', 'icon': 'gear'},
        {'head': 'You', 'text': 'Own the question and the decision', 'icon': 'shield'}], 'highlight': 4}, 3.4,
        caption='The roles hand work along a line. At every step a leader owns the question, the rules and the decision. If your company has none of these people, you can still do useful work with ready-made tools, which is what the practicals show.')

    # ---------------------------------------------------------------- 9 measuring
    section(d, 9, 'How we know a model is good')
    body(d, 'Every vendor quotes a number: "95 percent accurate", "an AUC of 0.9". This part gives you the words to read those numbers and the questions to ask about them. All figures in this part are illustrative.')
    h2(d, 'Accuracy, and why it can mislead')
    body(d, 'Accuracy is the share of all cases the model got right. It sounds like the whole story, and for rare events it is not. If one transaction in a hundred is fraud, a model that calls every transaction "fine" is right 99 times in 100 and catches no fraud at all. A high accuracy can hide a useless model, so we look at the kinds of right and wrong.')
    h2(d, 'The confusion matrix')
    body(d, 'For a model that sorts cases into two groups, such as fraud and fine, every case lands in one of four boxes. The table of the four boxes is the confusion matrix.')
    grid(d, [
        ['True positive (TP)', 'The model says fraud, and it is fraud. A catch.'],
        ['False positive (FP)', 'The model says fraud, and it is fine. A false alarm.'],
        ['False negative (FN)', 'The model says fine, and it is fraud. A miss.'],
        ['True negative (TN)', 'The model says fine, and it is fine. A correct pass.'],
    ], [4.4, W - 4.4], header=['Box', 'What it means'], size=10, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'One worked example (illustrative)')
    body(d, 'A fraud model checks 1,000 transactions. In truth, 10 are fraud. The model raises 20 alerts. Of the 20 alerts, 8 are real fraud and 12 are false alarms. It misses the other 2 frauds. The remaining 978 are correctly passed. These numbers are made up to show the arithmetic.')
    fig(d, {'kind': 'confusion', 'tp': 8, 'fp': 12, 'fn': 2, 'tn': 978}, 3.0, caption='Illustrative confusion matrix for a fraud model on 1,000 transactions.')
    grid(d, [
        ['Accuracy', 'Right answers out of all cases', '(8 + 978) / 1,000 = 986 / 1,000', '98.6 percent'],
        ['Precision', 'Of the alerts raised, how many were real', '8 / (8 + 12) = 8 / 20', '40 percent'],
        ['Recall', 'Of the real frauds, how many were caught', '8 / (8 + 2) = 8 / 10', '80 percent'],
        ['F1', 'One number that balances precision and recall', '2 x 0.40 x 0.80 / (0.40 + 0.80) = 0.64 / 1.20', 'about 53 percent'],
    ], [2.6, 5.4, 6.0, W - 14.0], header=['Measure', 'The question it answers', 'Arithmetic', 'Result'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    body(d, 'The accuracy of 98.6 percent looks excellent. Yet only 40 percent of the alerts are real, so the fraud team spends most of its day on false alarms, and one fraud in five still gets through. Precision protects your staff time. Recall protects your money. Which one matters more depends on what a false alarm and a miss cost you.')
    h2(d, 'The threshold')
    body(d, 'Most models give a score, for example "0.73 likely to be fraud". The threshold is the score above which you raise an alert. Set it low and you catch more fraud (recall rises) but raise more false alarms (precision falls). Set it high and the reverse happens. The threshold is a business decision about cost, and the data scientist should not choose it alone.')
    h2(d, 'The ROC curve and AUC')
    body(d, 'The ROC curve shows what happens as you slide the threshold from high to low. It plots the share of real frauds caught against the share of fine cases wrongly flagged. A curve that bows toward the top left corner is a better model. The area under the curve is called AUC. An AUC of 0.5 is a coin flip, and 1.0 is perfect. In the illustration below the AUC is about 0.86. When fraud is very rare, the precision-recall curve is the more honest picture, because it shows how many of the alerts are real.')
    fig(d, {'kind': 'roc'}, 3.2, caption='Illustrative ROC curve. The diagonal is a coin flip. The further the curve bows toward the top left, the better the model.')
    h2(d, 'Measures for models that give a number')
    grid(d, [
        ['MAE (mean absolute error)', 'On average, how far off the forecast is, in the same unit as the thing forecast. If the MAE is 20 bags of rice, the forecast is typically 20 bags away from the truth.'],
        ['RMSE (root mean squared error)', 'Like the MAE, but a big miss counts for much more than a small one. Use it when large errors hurt most.'],
        ['R squared', 'How much of the ups and downs in the real numbers the model explains. 1 means all of it, 0 means none.'],
    ], [4.8, W - 4.8], header=['Measure', 'In plain words'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'Measures for ranking and recommendation')
    body(d, 'When a system suggests a list, such as products to offer a shop, a simple measure is the top-k hit rate: in how many cases was what the customer really wanted among the first k suggestions? With k = 5, a hit rate of 60 percent would mean that in 6 cases out of 10 the right item was in the top five.')
    h2(d, 'Measures for language models')
    body(d, 'A language model writes free text, so there is no single right answer to count. Five checks are in common use.')
    grid(d, [
        ['Benchmarks', 'Public sets of standard questions (see the next part). Useful for a first comparison.'],
        ['Human review', 'People read the answers and rate them against a short checklist. Slow, and the most trusted.'],
        ['Groundedness', 'Does every claim in the answer come from the documents the model was given?'],
        ['Citation accuracy', 'Does each cited passage exist, and does it say what the answer says it says?'],
        ['Hallucination rate', 'How often does the answer contain something invented?'],
    ], [4.2, W - 4.2], header=['Check', 'The question it answers'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    body(d, 'For your own work, build a small test set from your own documents: a few dozen real questions with answers you have checked. Run the tool on them and count the results. No public benchmark can tell you how a tool does on your contracts, your reports and your words.')
    box(d, 'Questions to ask about any quoted figure', [
        '1. Measured on which data? Was it data the model had never seen, and does it look like ours?',
        '2. At which threshold? A figure at one threshold says little about another.',
        '3. What does a miss cost us, and what does a false alarm cost us?',
        '4. Compared with what? How does the task get done today, or by a very simple method?'])

    # ---------------------------------------------------------------- 10 benchmarks
    section(d, 10, 'Benchmarks', new_page=False)
    body(d, 'A benchmark is a set of standard test questions given to many models, so that their scores can be compared. You will see them in vendor announcements.')
    bullets(d, [('MMLU', 'tests broad knowledge across many school and professional subjects, by multiple-choice questions.'),
                ('HumanEval', 'tests coding: the model writes small programs, and the programs are run to see whether they work.'),
                ('Chatbot Arena', 'a public site where people compare two anonymous answers and vote for the better one. The votes build a ranking of human preference.')])
    h2(d, 'Limits of benchmarks')
    bullets(d, [('Contamination.', 'If the test questions were in the text the model learned from, the model may have seen them. The score then overstates what it can do.'),
                ('Who ran it.', 'A vendor-run score deserves less weight than an independent one. Ask who ran the test and whether others can repeat it.'),
                ('Your task is different.', 'A model that is strong on school-style questions may be weak on your contracts, your language or your forms.')])
    body(d, 'Use benchmarks to shortlist two or three candidates. Then test those candidates on your own documents, with your own questions, before you decide.', after=0)

    # ---------------------------------------------------------------- 11 training vs inference
    section(d, 11, 'Training and inference', new_page=False)
    body(d, 'Two words describe the two phases of a model\'s life. Costs and skills differ in each.', after=4)
    fig(d, {'kind': 'versus', 'left': {'head': 'Training', 'big': 'Learn', 'unit': 'rare, large, costly', 'icon': 'book'},
            'right': {'head': 'Inference', 'big': 'Use', 'unit': 'every request', 'icon': 'speech'}, 'middle': 'produces a model file'}, 2.8,
        caption='Training makes the model file once. Inference uses the file again and again.')
    grid(d, [
        ['What happens', 'The model learns its settings (weights) from data.', 'The finished model answers a new request.'],
        ['How often', 'Rarely: once, and again when the model is updated.', 'Every time someone asks.'],
        ['What it needs', 'Large data and a great deal of computing power.', 'Fast, reliable serving, so that answers come back quickly.'],
        ['What it produces', 'A model file.', 'An answer.'],
        ['Where the cost sits', 'A large one-off cost, paid by the model maker.', 'Billed per use, which is the cost you pay and which grows with your volume.'],
    ], [3.4, 6.4, W - 9.8], header=['', 'Training', 'Inference'], size=9.5, label_cols=(0,))
    spacer(d, 4)

    # ---------------------------------------------------------------- 12 behind the scenes
    section(d, 12, 'What happens when you press send', new_page=False)
    body(d, 'You type a question and press send. An answer appears in seconds. This part opens the box. The steps are simplified, and each product differs in the details.')
    h2(d, 'A plain message')
    bullets(d, [('1. Split.', 'Your text is cut into tokens.'),
                ('2. Predict.', 'The model predicts the most likely next token, adds it, and predicts again, over and over, until the answer is complete.'),
                ('3. Check and send.', 'The reply is checked by the provider\'s safety rules and streamed back to you as it is produced, which is why the words appear one after another.')])
    h2(d, 'A message with a document', before=8)
    body(d, 'When you also upload a document, more happens before the model writes anything. This is the pipeline behind a "chat with your documents" tool.')
    fig(d, {'kind': 'flow', 'steps': [
        {'head': 'Receive', 'text': 'The file arrives; text is extracted (OCR for scans)'},
        {'head': 'Chunk', 'text': 'Text is split into passages'},
        {'head': 'Embed', 'text': 'Each chunk becomes a list of numbers that captures meaning'},
        {'head': 'Index', 'text': 'The lists are stored in a vector database'},
        {'head': 'Retrieve', 'text': 'Your question is embedded; the closest chunks are found'},
        {'head': 'Assemble', 'text': 'Question, chunks and instructions form a prompt'},
        {'head': 'Answer', 'text': 'The model writes from that prompt and may cite the chunks'}], 'head_size': 22, 'text_size': 18}, 3.2,
        caption='The seven stages of a retrieval pipeline, read left to right. The first four happen when the file is added. The last three happen on every question.')
    body(d, 'An embedding is a list of numbers that captures the meaning of a passage, so that passages with similar meaning sit close together. A vector database stores these lists and finds the closest ones to a question quickly. Products differ: a short file may simply be placed whole in the context window, and only long files go through retrieval. The exact pipeline is the vendor\'s, so ask.')
    grid(d, [
        ['Receive and extract', 'Reads the file and pulls out the text. A scan needs optical character recognition (OCR).', 'A scan is misread: a 3 becomes an 8, a stamp covers a line, a table loses its columns.'],
        ['Chunk', 'Cuts the text into passages of a workable size.', 'A clause is split across two chunks, so neither chunk holds the full meaning.'],
        ['Embed', 'Turns each chunk into numbers that capture meaning.', 'Rare terms, names and codes are captured poorly.'],
        ['Index', 'Stores the embeddings so they can be searched.', 'A stale index: the document changed but the index did not. Permissions are ignored, so a person sees a passage they should not.'],
        ['Retrieve', 'Finds the chunks closest in meaning to the question.', 'The wrong chunk is retrieved, and the model answers confidently from the wrong page.'],
        ['Assemble and answer', 'Builds the prompt and generates the answer, possibly with citations.', 'The model misreads the right chunk, or a citation points to a passage that does not say that.'],
    ], [3.4, 6.2, W - 9.6], header=['Stage', 'What it does', 'What can go wrong'], size=9, label_cols=(0,))
    spacer(d, 4)

    # ---------------------------------------------------------------- 13 foundation models
    section(d, 13, 'Foundation models, open models, fine-tuning and cost', new_page=False)
    body(d, 'A foundation model is trained once on broad data and then adapted for many tasks. Few companies train one. Most use one. The questions for you are which kind to use, how far to adapt it, and what it will cost to run.')
    h2(d, 'Proprietary and open-weight models')
    body(d, 'A proprietary model is reached by subscription or through an API, and the maker keeps the model file. An open-weight model can be downloaded and run on your own machines. Be careful with the words "open source": the licence of an open-weight model may limit how you use it, so read the licence.')
    grid(d, [
        ['Set-up effort', 'Low: sign up and start.', 'Higher: you set up the servers and the software.'],
        ['Control of data', 'Your data goes to the provider. Check the terms and where it is processed.', 'Data can stay on your own machines.'],
        ['Quality', 'Often the strongest general models.', 'Improving fast; strong for many tasks, a gap on some.'],
        ['Skills needed', 'Little technical skill.', 'Engineers who can run and secure the model.'],
        ['Running cost (kind)', 'Pay per use or per user.', 'Computers and people, whether or not the model is busy.'],
        ['Who maintains it', 'The provider.', 'You, or a partner you hire.'],
    ], [3.6, 6.2, W - 9.8], header=['', 'Proprietary', 'Open-weight'], size=9.5, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'Four ways to get a model to do your task')
    body(d, 'Fine-tuning teaches style and skills. Retrieval supplies facts. Most business needs start with prompting and retrieval.')
    fig(d, {'kind': 'ladder', 'items': [
        {'head': 'Prompting', 'text': 'write clear instructions and examples', 'hl': True},
        {'head': 'Retrieval', 'text': 'give the model the right passages from your documents'},
        {'head': 'Fine-tune', 'text': 'teach an existing model your style or skill with examples'},
        {'head': 'Train from scratch', 'text': 'build a new model on your own huge data'}]}, 2.6,
        caption='Start at the bottom. Move up only when the step below cannot do the job.')
    grid(d, [
        ['Prompting', 'The instructions the model sees.', 'Always the first step.', 'Hours'],
        ['Retrieval', 'The facts the model can see when it answers.', 'The answer must come from your own, changing documents.', 'Days to weeks'],
        ['Fine-tuning', 'The model\'s style, format and skills.', 'You need a steady tone or format that prompts cannot give, and you have good examples.', 'Weeks, with specialists'],
        ['Training from scratch', 'Everything.', 'Almost never for a company.', 'Months, large teams and data'],
    ], [3.4, 4.4, 6.0, W - 13.8], header=['Method', 'What it changes', 'When to use it', 'Effort'], size=9, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'Where AI costs come from')
    body(d, 'The model fee is one of several costs. A business case that counts only the fee will come out too low. This stack shows the parts. No figures are given, because each depends on your plan and your volume.')
    fig(d, {'kind': 'stack', 'layers': [
        {'head': 'Usage', 'text': 'Tokens in and tokens out, for every request'},
        {'head': 'Licences', 'text': 'Subscriptions per user, or platform fees'},
        {'head': 'Data preparation', 'text': 'Cleaning, scanning, labelling and organising your information'},
        {'head': 'Set-up and integration', 'text': 'Connecting the tool to your systems and your process'},
        {'head': 'People and review', 'text': 'Time to supervise, check and approve outputs'},
        {'head': 'Monitoring and upkeep', 'text': 'Watching quality, fixing drift, updating'},
        {'head': 'Switching', 'text': 'The cost of moving to another provider later'}], 'head_size': 20, 'text_size': 19}, 2.9,
        caption='Seven kinds of cost. Session 12 puts them into your business case.')

    # ---------------------------------------------------------------- 14 data readiness
    section(d, 14, 'Is our data ready for AI?')
    body(d, 'A tool is only as good as the information behind it. Consider Nile Valley Foods, which wants an assistant that answers questions across its own records: a signed supplier contract, a year of invoices and a set of HR files. They exist as paper in a filing cabinet, scanned PDFs of mixed quality on a shared drive, Word documents, emails, and a spreadsheet index that someone started years ago. The company wants answers in seconds. Can it do that today? The scorecard below shows how to find out.')
    h2(d, 'The readiness scorecard')
    grid(d, [
        ['Inventory', 'Do we know what we hold, and where?', 'Nobody can say how many documents there are, or where they sit.'],
        ['Format and quality', 'Can a machine read it?', 'Crooked, faint or handwritten scans; text that OCR reads wrongly.'],
        ['Completeness and duplicates', 'Is each document present once?', 'Five copies of one contract in different folders, or pages missing.'],
        ['Metadata', 'Is each file labelled with type, date, owner, parties and reference number?', 'File names such as "scan0042.pdf" and no labels at all.'],
        ['Rights and confidentiality', 'May we use it, and who may see it? Are personal and confidential records protected?', 'Confidential HR files mixed in with documents anyone may see.'],
        ['Currency', 'Is it up to date? Are superseded versions marked?', 'An expired contract or old policy is returned as current.'],
        ['Structure', 'Does it have headings, sections and paragraphs we can rely on?', 'One long block of text with no divisions.'],
        ['Access and ownership', 'Who owns it, and who can open it?', 'Everyone can open everything, or nobody is responsible for it.'],
    ], [3.6, 6.4, W - 10.0], header=['Check', 'The question', 'The red flag'], size=9, label_cols=(0,))
    spacer(d, 6)
    h2(d, 'Six preparation steps')
    fig(d, {'kind': 'flow', 'steps': [
        {'head': 'Inventory', 'text': 'List and classify what you hold'},
        {'head': 'Digitise', 'text': 'Scan the paper and run OCR'},
        {'head': 'Clean', 'text': 'Remove duplicates and junk'},
        {'head': 'Describe', 'text': 'Add metadata and structure'},
        {'head': 'Protect', 'text': 'Set access and mark confidential files'},
        {'head': 'Index', 'text': 'Chunk, embed, index and test'}], 'head_size': 24, 'text_size': 20}, 2.6,
        caption='Six steps, left to right, from a filing cabinet to a searchable collection. Step 6 is the pipeline from Part 12, taught in Session 9.')
    h2(d, 'How to test the result')
    body(d, 'Write about 50 real questions to which you already know the answers, drawn from the work your teams really do, across contracts, invoices and HR. Run them through the tool and record four things.')
    bullets(d, [('Retrieval.', 'Was the right passage found?'),
                ('Faithfulness.', 'Does the answer say what the passage says, and nothing more?'),
                ('Citations.', 'Does each citation point to the right document and the right place in it?'),
                ('Time saved.', 'How long did it take compared with the usual way?')])
    body(d, 'Fix the weakest step, run the same questions again and compare. This test set also protects you later, because you can rerun it whenever the tool or the documents change.')
    h2(d, 'Preparing data to train or fine-tune a model')
    body(d, 'Preparing data to train or fine-tune a model is a different job from preparing it for retrieval. The steps are:')
    bullets(d, ['Collect data that you have the right to use for this purpose.',
                'Clean it and remove personal data.',
                'Filter for quality: drop poor, wrong or repeated material.',
                'Format it as examples, such as question and answer pairs.',
                'Split it into training, validation and test sets.',
                'Tokenise it, which means cutting it into tokens the model reads.',
                'Train, then evaluate on the test set.'])
    body(d, 'This asks for more data, more skill and more money, and the result is a model that has absorbed your documents in a way you cannot easily inspect or correct. For this reason most organisations should prepare for retrieval first. Retrieval keeps each fact tied to its source, lets you delete or update a document, and works with the model you already use.', after=0)

    # ---------------------------------------------------------------- 15 product
    section(d, 15, 'From model to working product')
    body(d, 'A model on its own does nothing for a company. It becomes useful when it sits inside a process that people use and look after. The life of a working AI system goes round in a cycle.')
    fig(d, {'kind': 'cycle', 'items': ['Collect data', 'Train', 'Test', 'Deploy', 'Monitor', 'Retrain'], 'center': 'The life cycle'}, 3.5,
        caption='Deploy means put it to work. Monitor means watch the results. Drift is when the world changes and the model slowly gets worse, which is why retraining is part of the cycle.')
    h2(d, 'Models, workflows and agents')
    body(d, 'Three levels of automation are easy to mix up. Each gives the system more freedom, and so needs firmer limits.')
    fig(d, {'kind': 'ladder', 'items': [
        {'head': 'Rule', 'text': 'if this, do that, always the same'},
        {'head': 'Workflow with an AI step', 'text': 'fixed steps, one of which uses a model, with a person approving'},
        {'head': 'Agent', 'text': 'the model decides which steps to take and which tools to use', 'hl': True}]}, 2.6,
        caption='The ladder runs from the most predictable at the bottom to the most freedom at the top.')
    body(d, 'Session 12 shows you the first two steps side by side on the same messages: a rule, and a workflow with an AI step and a person approving. Session 11 looks at agents. The more freedom a system has, the more it matters to set limits on what it may do and to keep a person approving anything that leaves the company, such as an email to a customer, a payment or a change to a record. A human in the loop is a person who must approve before the action happens.')
    h2(d, 'Automation tools on the market')
    body(d, 'Many tools can build the same workflow. They differ in who they suit and how they charge. The list below says how each is billed in kind. It gives no prices, which change and depend on your plan.')
    grid(d, [
        ['Zapier', 'No-code connections between thousands of apps. Suits business users. Discussed as an option only.', 'Per task (a task is one completed action step)'],
        ['Make', 'Visual canvas with branches and detailed control. Suits people who like to see the whole flow.', 'Per operation'],
        ['n8n', 'Flexible and technical. Can be run on your own server. Suits teams with a technical person.', 'Per execution (a run of the whole workflow) on its cloud'],
        ['Microsoft Power Automate and Copilot Studio', 'Best when your company already runs Microsoft 365. Connects to Outlook, Excel, Teams.', 'Per user, or by usage credits'],
        ['Agent builders in ChatGPT, Gemini and Claude', 'Build an assistant or agent for your own instructions and files, inside the assistant you already use.', 'Part of the assistant plan, with limits that vary by plan'],
    ], [3.8, 8.0, W - 11.8], header=['Tool', 'What it suits', 'How it is billed (kind only)'], size=9, label_cols=(0,))
    spacer(d, 4)
    body(d, 'Billing terms and plan limits change often. Check the current terms before you decide, and ask what happens to your data on each plan.', after=0)

    # ---------------------------------------------------------------- 16 what to bring
    section(d, 16, 'What to bring to Session 1')
    body(d, 'You have nothing to prepare before Session 1 except to read this handbook. A few small things make the demonstrations more useful.')
    h2(d, 'What to bring')
    bullets(d, [('A laptop and one AI assistant account.', 'Any assistant you already use will do, such as ChatGPT, Claude, Gemini or Copilot. You can join the demonstrations if you wish, and you can also simply watch. The course does not need a paid plan.'),
                ('Use only sample or invented data.', 'In class and in practice, use made-up or sample information. The course gives you a fictional company, Nile Valley Foods Ltd, for this.')], after=4)
    h2(d, 'Ground rules for responsible use', before=8)
    fig(d, {'kind': 'icons', 'items': [
        {'icon': 'lock', 'head': 'Protect data', 'text': 'No personal or confidential data in a tool your company has not approved'},
        {'icon': 'magnifier', 'head': 'Check', 'text': 'Tools can be wrong. Check facts, figures and sources'},
        {'icon': 'check', 'head': 'Approve', 'text': 'A person approves anything that leaves the company'}]}, 3.3)
    body(d, 'These three rules apply from the first session. The policy you draft in Session 13 builds on them.')
    box(d, 'Questions to keep in mind from Session 1', ['Where in my own work do I already meet a system that learns from examples?',
                                              'Which AI claims have I been asked to trust without seeing a number?',
                                              'What would "better" mean in my work, in a number I could measure?'])

    # ---------------------------------------------------------------- 11 glossary
    section(d, 17, 'Glossary')
    body(d, 'Terms in plain words, from A to Z.', after=4)
    G = [
        ('Agent', 'An AI system that decides for itself which steps to take and which tools to use to reach a goal. It needs firm limits.'),
        ('AI literacy', 'Knowing enough about how AI works, where it fails and what rules apply, to use it and supervise it well.'),
        ('Algorithm', 'A set of steps a computer follows to solve a problem or make a calculation.'),
        ('API', 'A door that lets one program talk to another. A tool uses an API to ask an AI model for a result.'),
        ('Automation', 'Letting software do repeated steps without a person doing each one.'),
        ('Accuracy', 'The share of all cases a model got right. It can mislead when the event is rare.'),
        ('AUC', 'The area under the ROC curve. 0.5 is a coin flip and 1.0 is perfect.'),
        ('Benchmark', 'A set of standard test questions given to many models so that their scores can be compared.'),
        ('Chunk', 'A passage of a document, cut to a workable size so that it can be embedded and retrieved.'),
        ('Confusion matrix', 'A table of the four outcomes of a yes or no model: true positives, false positives, false negatives and true negatives.'),
        ('F1', 'One number that balances precision and recall.'),
        ('MAE and RMSE', 'Measures of how far a number forecast is from the truth, on average. RMSE punishes big misses more.'),
        ('OCR', 'Optical character recognition: reading the text from a scan or a photo.'),
        ('Open-weight model', 'A model whose file can be downloaded and run on your own machines. The licence may limit use.'),
        ('Precision', 'Of the cases the model flagged, the share that were truly positive.'),
        ('Recall', 'Of the truly positive cases, the share the model caught.'),
        ('ROC curve', 'A curve that shows how catches and false alarms change as the threshold moves.'),
        ('Threshold', 'The score above which a model raises an alert. Moving it trades false alarms against misses.'),
        ('Vector database', 'A store of embeddings that finds quickly the ones closest in meaning to a question.'),
        ('Backpropagation', 'The way a neural network shares out the blame for an error backward through its layers, so each weight can be adjusted.'),
        ('Baseline', 'How the task is done today, with its time and error rate. You compare the automated version against it.'),
        ('Bias', 'A systematic tilt in a model\'s results that treats some cases or groups unfairly, often copied from the data.'),
        ('Brief', 'A prompt written once in parts and reused. Session 8 teaches you to write one.'),
        ('Classification', 'Learning to put each case into a category, such as fraud or fine.'),
        ('Clustering', 'Finding groups of similar cases without being told the groups in advance.'),
        ('Context window', 'How much text the model can keep in view at one time, including your question, files and its answer.'),
        ('Deep learning', 'Machine learning with neural networks of many layers. It suits images, sound and language.'),
        ('Drift', 'A model getting worse over time because the world has changed since it was trained.'),
        ('Embedding', 'A list of numbers that stands for the meaning of a piece of text or an image, so that similar things are close together.'),
        ('Feature', 'One piece of information the model uses as input, such as the amount of a payment or the day of the week.'),
        ('Fine-tuning', 'Training an existing model a little more on your own examples so that it fits a particular style or task.'),
        ('Foundation model', 'A large model trained on broad data that can be adapted to many tasks. Language models are one kind.'),
        ('Governance', 'The rules, roles and checks that decide who may use AI, for what, and who answers when something goes wrong.'),
        ('Gradient descent', 'Improving a model by taking many small steps that each make the error a little smaller, like walking downhill in fog.'),
        ('Hallucination', 'A confident answer from a model that is false or invented.'),
        ('Human in the loop', 'A person who must approve or edit before an automated action goes ahead.'),
        ('Inference', 'Using a trained model to produce an answer for a new case. Training is learning; inference is using.'),
        ('Label', 'The correct answer attached to an example, used in supervised learning.'),
        ('Loss or error', 'A number that says how far the model\'s guess is from the right answer. Training tries to make it smaller.'),
        ('Machine learning', 'Computer systems that learn patterns from data instead of following only hand-written rules.'),
        ('Model', 'The result of training: a program whose behaviour comes from the numbers it has learned.'),
        ('Neural network', 'A model made of layers of simple connected units, loosely inspired by the brain.'),
        ('Overfitting', 'A model learning its training examples too closely, so that it does badly on new cases.'),
        ('Parameter or weight', 'A number inside a model that training adjusts. It sets how strongly one input influences the answer.'),
        ('Pilot', 'A small, time-limited trial in real work, with a measure of success set in advance.'),
        ('Prompt', 'Anything you type or send to an AI model.'),
        ('Prompt injection', 'Hidden instructions in an email, web page or document that try to make an AI tool do what its owner did not intend.'),
        ('Regression', 'Learning to give a number as the answer, such as a forecast of sales.'),
        ('Reinforcement learning', 'Learning by trial and reward: actions that pay off are repeated.'),
        ('Retrieval', 'Fetching the relevant passages from your own documents and giving them to the model before it answers.'),
        ('ROI (return on investment)', 'What you gain compared with what you spend, for example time saved against cost.'),
        ('Supervised learning', 'Learning from examples that come with the right answers.'),
        ('Token', 'A small piece of text, often a short word or part of a word, that a language model reads and writes.'),
        ('Training', 'The process of adjusting a model\'s weights, using data, until its guesses are good.'),
        ('Trigger', 'The event that starts an automation, such as a new email arriving or a timer going off.'),
        ('Unsupervised learning', 'Learning from data with no right answers given, by finding structure such as groups.'),
        ('Validation and test data', 'Data kept apart from training. Validation data helps tune the model. Test data is locked until the end for a fair final check.'),
        ('Workflow', 'A fixed series of steps, often across several apps, that runs when a trigger fires.'),
    ]
    G.sort(key=lambda t: t[0].lower())
    grid(d, [[a, b] for a, b in G], [4.3, W - 4.3], header=['Term', 'In plain words'], size=9.5, label_cols=(0,))

    # ---------------------------------------------------------------- 12 at a glance
    section(d, 18, 'The fourteen sessions at a glance')
    S = [
        ('1', 'Seeing: pixels, features and neurons', 'A one-page sheet: how a picture becomes numbers, the payment-risk neuron worked by hand, and the digit results'),
        ('2', 'Learning from examples: types of machine learning, decision trees, nearest neighbours', 'A one-page sheet: the four types of learning, a tree read as rules, nearest neighbours and the honest scores'),
        ('3', 'Measuring a model: accuracy, precision, recall, F1, ROC and AUC, thresholds, baselines, overfitting', 'The vendor question sheet: ten questions about the numbers behind any AI claim'),
        ('4', 'Words as numbers: bag of words, TF-IDF, embeddings and distance', 'The distance cheat sheet: four ways to say how close two things are'),
        ('5', 'Language models: tokens, attention and next-word probability', 'A one-page sheet: the next-word loop, the softmax recipe, temperature and five questions to ask about any answer'),
        ('6', 'Foundation models: pretraining, post-training, model families, reasoning and multimodal models, benchmarks', 'A model comparison grid for your own tasks, with questions for a model card and a benchmark claim'),
        ('7', 'Open weights, file formats, size and running cost', 'A rent, host or own decision sheet, with the memory sum and the licence questions'),
        ('8', 'Prompting and reasoning models', 'A reusable prompt template and a prompt log'),
        ('9', 'Giving a model your knowledge: retrieval-augmented generation, long context and fine-tuning', 'A decision tree: prompt first, then retrieve, then fine-tune'),
        ('10', 'When models fail, and how to check them', 'A five-step check routine and a test-set template'),
        ('11', 'Agentic AI: tools, loops, MCP, autonomy and guardrails', 'Your Tool Boundary Sheet: what an agent may read, write, send and spend, who approves, the log and the off switch'),
        ('12', 'Workflow mapping (practical)', 'Your mapped workflow, the choice for each step, your assistant sketch and the hours-saved estimate in the Business Case Workbook'),
        ('13', 'Governance and buying (practical)', 'Your Risk Register, AI Use Policy draft, Vendor Question List and questions for your lawyer'),
        ('14', 'Data readiness assessment, roadmap and 90-day plan (practical)', 'Your inventory and scorecard, your roadmap, and the Follow-up Kit'),
    ]
    grid(d, [list(s) for s in S], [1.0, 7.4, W - 8.4], header=['No.', 'Session', 'You keep'], size=9.5, label_cols=(0,), min_h=1.0)
    spacer(d, 8)
    para(d, 'Session 0, the introduction, comes first and gives you this handbook. Each session lasts two hours. After the course, the instructor follows up at 30, 60 and 90 days.', 10, after=8)
    para(d, 'Jotham Martin Wambi  |  KLAi Professional Learning  |  jothammartin.wambi@gmail.com  |  +256 750 990 718', 9, color='404040')

    out = EDITION / '03 Learner Materials' / (name + '.docx')
    save(d, out)
    to_pdf(out)


if __name__ == '__main__':
    build()
