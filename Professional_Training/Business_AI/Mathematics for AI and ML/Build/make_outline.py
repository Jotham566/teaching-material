import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / 'templates_gen'))
from docx_kit import *  # noqa

def bullets(d, items, size=10, after=2):
    for it in items:
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.5); p.paragraph_format.first_line_indent = Cm(-0.4)
        add_run(p, '•  ', size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True); add_run(p, it[1], size)
        else:
            add_run(p, it, size)

d = new_doc('Course outline', 'Mathematics for AI and Machine Learning')
title(d, 'Mathematics for AI and Machine Learning', 'Course outline  |  36 hours, 18 sessions of 2 hours  |  Updated 4 November 2026')
h2(d, 'What it is', 0)
para(d, 'The mathematics that sits under machine learning and modern AI, taught the way KLAi teaches everything else. Each idea comes as a picture first, then a small calculation by hand, then the same idea on a computer, then a real use in AI. The course follows the three pillars that the main references share: linear algebra, calculus and optimisation, and probability and statistics. It adds information theory, because that is where the training loss of language models comes from. By the end a learner can read the equations in a machine learning paper or in a library manual, and has built linear regression, logistic regression, PCA, a small neural network and attention from first principles.', 10, after=4)
h2(d, 'Linked to the AI tools people use today')
para(d, 'Every session ends by showing where the mathematics appears in tools such as ChatGPT, Gemini and Claude. These are products built on large language models. Their exact designs are not published, so the course uses the published transformer design and open models to show the same mathematics, and it says plainly which parts are published and which are not. Examples: embeddings and cosine similarity in document search, matrix multiplication in every layer, the softmax and temperature that choose the next word, cross-entropy and perplexity as the training score, and attention as the core step.', 10, after=4)
h2(d, 'Who it is for')
bullets(d, [('Learners who code.', 'Analysts, engineers and students. They work in Python (NumPy and Matplotlib in Google Colab, which is free).'),
            ('Learners who do not code.', 'Career changers and managers. They do the same exercise in Google Sheets or Excel on the same data, so the idea is identical and only the tool differs. Every session has both versions.'),
            ('Entry requirement.', 'High school algebra. No calculus or statistics needed. Taking it before the Machine Learning course is best, and it also works alongside it.')], 10)
h2(d, 'Dates, fees and enrolment')
bullets(d, ['First intake starts on 21 November 2026. Enrolment is ongoing, so learners can still sign up after the start date.',
            'Fee: UGX 1,000,000 per learner, the same as the other KLAi courses. Groups of 1 to 5, group pricing on request, and in-house training for teams.',
            'Evenings and weekends, in two-hour sessions. Online, at the Innovation Hub in Nakawa, or at the learner\'s workplace.'], 10)
h2(d, 'How every session runs (2 hours)')
grid(d, [['0:00', '10', 'Recall, then a real question from AI that today\'s mathematics answers'], ['0:10', '35', 'Concept: a picture, then one example calculated by hand'], ['0:45', '10', 'Break'],
         ['0:55', '45', 'Lab in Python, Google Sheets or Excel: predict, run, then change one thing'], ['1:40', '15', 'Where this appears in ChatGPT, Gemini, Claude and other ML, and an exit check'], ['1:55', '5', 'Save the work']],
     [2.0, 2.0, 13.4], header=['Starts', 'Minutes', 'What happens'], size=9)
h2(d, 'The eighteen sessions')
rows = [
 ['1', 'Functions, notation and logarithms', 'Reading sums and functions; exponentials and logarithms', 'A model scores each possible next word with a probability; training works with the logarithm of that probability'],
 ['2', 'Vectors', 'Data rows as vectors; dot product, length, distance, cosine similarity', 'Text becomes vectors (embeddings); cosine similarity finds the right passage when AI searches your documents'],
 ['3', 'Matrices', 'Matrices as tables and as transformations; multiplication and shapes', 'Each layer of a language model is a matrix multiplication; "billions of parameters" means billions of numbers in matrices'],
 ['4', 'Solving linear systems', 'Equations as matrices; inverse, rank, determinant; least squares', 'Fitting a line is solving equations; why too many features and too few rows break a fit'],
 ['5', 'Eigenvalues and eigenvectors', 'Directions that a matrix only stretches', 'Where data varies most; the basis of PCA and of understanding embeddings'],
 ['6', 'SVD and PCA', 'Breaking a matrix into simple parts; reducing dimensions', 'Compression and noise removal; low-rank adaptation (LoRA) fine-tunes big models by training small matrices'],
 ['7', 'Derivatives', 'Slope of a curve; rules; checking with numbers', 'The slope of the loss says how wrong the model is and which way to change it'],
 ['8', 'Partial derivatives and the gradient', 'Many inputs; the direction of steepest increase', 'A model with billions of parameters has a gradient with billions of entries'],
 ['9', 'The chain rule and the Jacobian', 'Derivatives of functions of functions; computation graphs', 'Backpropagation through dozens of layers is the chain rule used again and again'],
 ['10', 'Gradient descent', 'Learning rate, stochastic gradient descent, momentum, Adam, convexity', 'How ChatGPT-style models are trained: an Adam-type optimiser with a learning-rate schedule'],
 ['11', 'Backpropagation by hand', 'A tiny network forward and backward, then in matrix form', 'What happens in every training step, and why training costs far more computing than answering a question'],
 ['12', 'Optimisation in practice', 'Regularisation, constraints in plain terms, overflow and the stable softmax', 'Why long outputs do not overflow, why many models use 16-bit numbers, and how overfitting is controlled'],
 ['13', 'Probability basics', 'Random variables, expectation, variance, covariance', 'A chat model outputs a probability for every possible next word'],
 ['14', 'Distributions and sampling', 'Bernoulli, binomial, Gaussian, multivariate Gaussian; the central limit theorem; confidence intervals and A/B tests', 'Temperature and top-p sampling pick the next word, which is why the same question can give different answers; how to test whether a new AI feature really is better'],
 ['15', 'Conditional probability and Bayes', 'Updating beliefs with evidence; a small Naive Bayes classifier', 'Spam filters and diagnosis; reasoning with uncertain answers'],
 ['16', 'Maximum likelihood and MAP', 'Why squared error and cross-entropy are the right losses; bias and variance', 'Training a language model is maximum likelihood; weight decay is a MAP prior'],
 ['17', 'Information theory', 'Entropy, cross-entropy, KL divergence, softmax, perplexity', 'Cross-entropy is the training loss of language models, and perplexity is their standard score'],
 ['18', 'Course project', 'Build linear regression, logistic regression, PCA, a small network and attention from first principles', 'Attention is the core step inside ChatGPT, Gemini and Claude; the project is yours to keep, with automatic self-checks and no marks'],
]
grid(d, rows, [0.9, 3.6, 5.6, 7.3], header=['#', 'Session', 'What is taught', 'Where it appears in ChatGPT, Gemini, Claude and other ML'], size=8.5, label_cols=(0,))
h2(d, 'Kept out on purpose')
para(d, 'Measure theory, formal proofs, convex duality, tensor calculus and the finer points of numerical linear algebra. They are useful for researchers but lose most learners. Derivations appear only where they feed something the learner then implements: the least-squares solution, backpropagation, and the gradient of softmax with cross-entropy.', 10, after=4)
h2(d, 'No exams, no marks, and what learners keep')
bullets(d, ['No exams, no marks, no grades and no pass mark. Each session ends with an automatic check of the notebook or spreadsheet that shows OK or NOT YET. The checks are for the learner to see what works, and nothing is recorded.',
            'The course project (session 18) is a practical build that each learner keeps. The Python version is a notebook on the learner\'s own personal data, with automatic self-checks. The spreadsheet version is a guided workbook (Google Sheets or Excel) with the same numbers. A project checklist supports feedback from the learner and a partner.',
            'A certificate of completion from KLAi Professional Learning for completing the course project.',
            'A one-page formula sheet that each learner writes, with every formula named in plain words and in the industry term.'], 10)
h2(d, 'Decisions already made')
bullets(d, ['36 hours in 18 sessions. Both coding and non-coding learners. Preferably taken before the Machine Learning course.',
            'High school algebra as the only entry requirement. Derivations only where they feed an implementation.',
            'Start 21 November 2026 with ongoing enrolment. The fee is the same as the other courses. The non-coding track works in Google Sheets and in Excel.'], 10)
h2(d, 'Next step')
para(d, 'The flyer comes first, so that you can share and market the course. After you approve the flyer, I build the rest in the style of the Applied AI course: KLAi slides with spoken notes, Python notebooks, spreadsheet workbooks for Google Sheets and Excel, automatic checks, and a facilitator guide.', 10, after=4)
save(d, Path(__file__).resolve().parent.parent / 'Course_Outline_Mathematics_for_AI_and_ML.docx')
