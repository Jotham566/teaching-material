import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
BUILD = HERE.parent
EDITION = BUILD.parent.parent
sys.path.insert(0, str(BUILD / 'templates_gen'))
from docx_kit import *  # noqa

def bullets(d, items, size=10, after=2, num=False):
    for i, it in enumerate(items, 1):
        p = para(d, '', size, after=after)
        p.paragraph_format.left_indent = Cm(0.6); p.paragraph_format.first_line_indent = Cm(-0.5)
        add_run(p, (f'{i}.  ' if num else '•  '), size, True)
        if isinstance(it, tuple):
            add_run(p, it[0] + ' ', size, True); add_run(p, it[1], size)
        else:
            add_run(p, it, size)

d = new_doc('Course map for approval', 'Applied AI and Automation, Executive Edition')
title(d, 'Course map for approval: 14 sessions that explain how AI works', '5 November 2026  |  14 sessions and 28 hours  |  nothing is built until this is approved')

h2(d, 'Why change', 0)
para(d, 'The first executive already uses AI tools. She asked for the technicals: a touch of the maths behind ChatGPT and a touch of machine learning. Session 0, already delivered, gives the map: the types of AI, the training loop, gradient descent, backpropagation, metrics, data readiness, inference, foundation models, open weights, the ways to adapt a model, costs and roles. The course now goes deeper on each of those through demonstrations, and the documents move to the end. I compared the plan with Elements of AI (University of Helsinki), DeepLearning.AI Generative AI for Everyone, the MIT Sloan and MIT Professional Education executive generative AI programmes, the vendor prompt-engineering guides and the OSI Open Source AI Definition 1.0. No learner writes code. Juniors who want coding labs can be offered them separately.', 10, after=4)

h2(d, 'Design rules')
bullets(d, [
 ('Size.', '14 sessions of 2 hours, 28 hours in all. No coding labs, no exams, no marks.'),
 ('Who does what.', 'I demonstrate and the learner may join in.'),
 ('Order for every concept.', 'A picture, an everyday analogy, a calculation with at most three numbers done by hand, the real industry term, then one demonstration.'),
 ('Maths.', 'Multiply, add and compare. The real names (dot product, Euclidean distance, Manhattan distance, cosine similarity) are explained as pictures.'),
 ('Recorded demonstrations.', 'Every demonstration is recorded in advance. The real result is shown on the slide and labelled with the model, the day and the number of runs. The live run is optional.'),
 ('Examples.', 'They come from finance, operations, customer service, HR, sales, compliance and legal. The fictional case company Nile Valley Foods Ltd is the shared thread, so the same material can train financial managers and other executives, in a group or one to one.'),
 ('Three skins.', 'Every demonstration document comes in three interchangeable skins with the same structure: a contract clause, an invoice or financial statement line, and an HR policy paragraph. The trainer picks the skin that fits the room.'),
 ('Take-away.', 'Each session ends with something the learner keeps, and I say what it is.'),
 ('Documents.', 'Documents and templates are created in the last three sessions.')], 10)

h2(d, 'The map')
rows = [
['1', 'Seeing: pixels, features and neurons', 'How does a machine recognise a picture?', 'An image as a grid of three numbers per pixel (red, green, blue). A neuron as a weighted checklist, like a risk score for a payment. Layers find edges, then shapes, then things.', 'Show an image as RGB numbers. A small trained network labels dog or cat. Show what each layer picks up.', 'A one-page "how a network sees" sheet.'],
['2', 'Learning from examples: types of machine learning, decision trees, nearest neighbours', 'How does a machine learn a rule from past cases?', 'A decision tree as a checklist. Nearest neighbours as precedent: find the most similar past cases.', 'A built model predicts a business category, with the case chosen by me (for example types of customer message or of expense), run live. A tree drawn from real data.', 'A one-page choice sheet: which kind of learning fits which business question.'],
['3', 'Measuring a model: accuracy, precision, recall, F1, ROC and AUC, thresholds, baselines, overfitting', 'How do I know whether a model is any good?', 'A fraud alarm with its four kinds of answer. A dial that trades missed cases for false alarms. A model that memorises.', 'Move a threshold and watch precision and recall change on a real result table. A model that scores 90 percent by saying no every time.', 'A metric question list to ask any vendor or team.'],
['4', 'Words as numbers: bag of words, TF-IDF, embeddings and distance', 'How can a computer find text that means the same thing?', 'Count words, then place meanings on a map. Euclidean as the straight line, Manhattan as walking city blocks, dot product as an agreement score, cosine similarity as the angle between two arrows whatever their length.', 'Semantic search: a plain-words description returns the right formal term or clause. The same four distances computed by hand in a spreadsheet.', 'The distance cheat sheet.'],
['5', 'Language models: tokens, attention and next-word probability', 'What does a chatbot actually do when it answers?', 'Text cut into tokens. Attention as "which earlier words matter to this word". The next word chosen from a list of probabilities. Temperature as how adventurous the choice is.', 'Show tokens, the probability list for the next word and the effect of temperature, using an open model with the real numbers.', 'A plain-words one-page explanation to give a colleague.'],
['6', 'Foundation models: pretraining, post-training, model families, reasoning and multimodal models, benchmarks', 'Where do ChatGPT, Gemini and Claude come from, and how do they differ?', 'Pretraining as reading a library, post-training as coaching. Mixture of experts, reasoning models and image-generating diffusion models, each in one sentence and one picture. What a benchmark does and does not tell you.', 'Compare the same task on two or three assistants, recorded, with the results labelled. Read a model card.', 'A model-comparison grid for their own tasks.'],
['7', 'Open weights, file formats, size and running cost', 'What does it mean to own, host or rent a model?', 'Open source versus open weights, with the OSI definition and the Llama licence as the example of the difference. Weights are a large file of numbers. Safetensors, GGUF and ONNX are containers. Quantisation shrinks the numbers. Parameters and memory.', 'Run a small open model on a laptop. Show file sizes before and after quantisation.', 'A rent, host or own decision sheet.'],
['8', 'Prompting and reasoning models', 'How do I get reliable work out of an assistant?', 'A good brief to a new colleague: role, context, examples, format, checks. Prompts are tested like anything else.', 'A weak and a strong prompt side by side with recorded results. A structured-output (table) prompt. A reasoning model against a standard model.', 'A reusable prompt template and a prompt log.'],
['9', 'Giving a model your knowledge: retrieval-augmented generation, long context and fine-tuning', 'How do I make an assistant know my documents?', 'Climb from prompting to retrieval to LoRA fine-tuning, and move up only when the cheaper step measurably falls short. Retrieval as a librarian who fetches the pages first. Fine-tuning as training a new hire in the house style.', 'The same question answered with and without the document. The search step shown with embedding similarity. A small fine-tuning explained with a before and after.', 'A decision tree: prompt, retrieve or fine-tune.'],
['10', 'When models fail, and how to check them', 'When should I not trust the answer?', 'Hallucination, arithmetic slips, bias in ranking, instructions hidden inside a document. A checking routine.', 'Recorded failure cases with the key. A test set of ten questions, scored.', 'A five-step check routine and a test-set template.'],
['11', 'Agentic AI: tools, loops, MCP, autonomy and guardrails', 'What changes when an assistant can act as well as answer?', 'Plan, act, observe, repeat. An agent as a junior assistant with access badges. Least privilege, approval for important actions, logging. MCP as a standard plug for tools.', 'A personal assistant agent that summarises email, recorded. Show the permissions it was given and the approval step. Show an injected instruction.', 'A tool-boundary sheet for any agent.'],
['12', 'Workflow mapping (practical)', 'Which of my tasks should be a rule, an AI step or an agent?', 'Trigger, steps, handoffs, check. The same twelve customer messages handled by rules and then by AI.', 'The two recorded automations side by side with the measured comparison. Map her own workflow (work, or personal email summaries) on the template. Sketch a personal assistant.', 'A mapped workflow with a rule, AI or agent choice and an hours-saved estimate (the business case template).'],
['13', 'Governance and buying (practical)', 'What rules and questions protect the company?', 'Use policy, risk register, vendor questions, human accountability. The law in hedged plain words (Uganda Data Protection and Privacy Act, 2019; no legal advice).', 'A vendor proposal taken apart, recorded.', 'The AI use policy draft and the vendor question list.'],
['14', 'Data readiness assessment, roadmap and 90-day plan (practical)', 'Is our information ready, and what do we do first?', 'The five kinds of data, the readiness scorecard, the six steps from records room to AI-ready data.', 'The scorecard scored on her own organisation.', 'The data roadmap, the 90-day plan and the follow-up kit.']]
grid(d, rows, [1.5, 2.6, 2.3, 4.0, 4.0, 3.0], header=['Session', 'Title', 'The question it answers', 'The picture or analogy', 'The demonstration the lecturer runs', 'What the learner keeps'], size=7.5, hdr_size=7.5, label_cols=(0,))

h2(d, 'What is reused and what changes', 10)
bullets(d, [
 'Source material is reused and rewritten without code: vectors, cosine similarity, attention and softmax from the Mathematics for AI and ML course; neurons, text as data and language models from the AI and Data Science course; metrics from the IUEA second half.',
 'The old sessions "Where AI fits", "Reviewing documents", "Automation 1" and "Automation 2" are absorbed into Sessions 6, 8, 10, 11 and 12.',
 'The old documents sessions move to Sessions 12 to 14. Session 0 stays as delivered.',
 'The flyer line for AI & Automation needs one new sentence, for example: how AI works, where it fits, your AI policy and your data roadmap. The flyer figures of 24 hours and 12 sessions become 28 hours and 14 sessions. This is a change for you to approve.'], 10)

h2(d, 'Facts discipline')
bullets(d, [
 'No claims about the internals, size or training data of closed models.',
 'Open-model facts come only from published model cards.',
 'The fine-tuning cost figures found online are not quoted. Adoption forecasts are not quoted unless I have checked the original source.',
 'Every AI result on a slide is a real recorded run. A "what was verified" list is kept in the Rehearsal Record.',
 ('Still unverified before building.', 'The free tools for each demonstration (an image classifier, a small open model, an email-summary agent on free tiers). The external facts on slides (the OSI definition and Llama licence status, the MCP specification status and the prompt-guide recommendations) are re-checked in the teaching week.')], 10)

h2(d, 'Decisions needed')
bullets(d, [
 'Approve the 14-session map.',
 'Confirm the case for the Session 2 model demonstration, for example types of customer message or of expense.',
 'Confirm the three document skins (contract clause, invoice or financial statement line, HR policy paragraph), or name others.',
 'Confirm the flyer change.',
 'Confirm whether the personal assistant agent demonstration uses a free tool, pre-recorded, and which email account it uses. It will be a demonstration mailbox and never a real one.'], 10, num=True)

out = EDITION / '01 Course Overview'
name = 'Course Map for Approval (5 Nov 2026)'
save(d, out / (name + '.docx'))
subprocess.run(['soffice', '-env:UserInstallation=file:///tmp/lo_map', '--headless', '--convert-to', 'pdf', '--outdir', str(out), str(out / (name + '.docx'))], capture_output=True, timeout=200)
