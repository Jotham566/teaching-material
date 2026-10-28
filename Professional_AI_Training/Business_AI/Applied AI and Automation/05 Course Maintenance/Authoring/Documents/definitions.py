"""Shared course definitions. Examples illustrate a definition; they do not replace it."""
OECD='https://oecd.ai/en/ai-principles'
ML='https://developers.google.com/machine-learning/intro-to-ml/what-is-ml'
LLM='https://developers.google.com/machine-learning/crash-course/llm/transformers'
DS='https://www.ibm.com/think/topics/data-science'
AGENT='https://www.anthropic.com/research/building-effective-agents'
CAG='https://arxiv.org/abs/2412.15605'
RAG='https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-information-retrieval'
NIST='https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf'
D={
'AI':('Artificial intelligence is the field of developing computational systems that perform functions associated with intelligence, including perception, reasoning, learning and decision-making.',OECD),
'AI system':('An AI system infers from inputs how to produce predictions, content, recommendations or decisions for explicit or implicit objectives. Systems differ in autonomy and adaptation.',OECD),
'Data analysis':('Data analysis is the systematic examination and interpretation of data to answer questions and support conclusions.',DS),
'Data science':('Data science is an interdisciplinary field that uses statistical and computational methods, with domain knowledge, to extract knowledge from data.',DS),
'Machine learning':('Machine learning is a branch of AI in which algorithms fit models to data so that performance on a task can improve through experience.',ML),
'Model':('A model is a computational or mathematical representation used to describe relationships or map inputs to outputs. Its structure or parameters may be specified or learned.',ML),
'Machine-learning model':('A machine-learning model is a computational representation whose parameters or structure are learned from data to perform a task.',ML),
'Deep learning':('Deep learning is machine learning using neural networks with multiple layers that learn representations of data.',ML),
'Generative AI':('Generative AI is a class of AI models and systems that produce new content by modelling patterns learned from data.',NIST),
'Large language model':('A large language model is a neural-network model trained on extensive language data to model token sequences and generate or process language.',LLM),
'Training':('Training is the process of fitting a model to data by adjusting its parameters or structure according to an objective.',ML),
'Inference':('Inference is using a fitted model to compute an output from an input without running a training update.',ML),
'Foundation model':('A foundation model is trained on broad data and can be adapted to many downstream tasks, through prompting or further training.','https://arxiv.org/abs/2108.07258'),
'Token':('A token is a unit into which a model represents input or output, such as a word, part of a word, punctuation or an image patch. Tokenisation depends on the model.',LLM),
'Context':('Context is the information available to a model for the current computation, including instructions, supplied evidence and earlier conversation within its context window.',LLM),
'RAG':('Retrieval-augmented generation retrieves relevant source material and supplies it to a generative model when producing an answer.',RAG),
'CAG':('Cache-augmented generation preloads a manageable knowledge collection into model context and reuses cached computation for subsequent questions.',CAG),
'Fine-tuning':('Fine-tuning is further training of an existing model on selected data to change its behaviour for particular tasks.',LLM),
'Automation':('Automation uses software to execute defined work with reduced human intervention. It can use fixed rules, AI or both.',AGENT),
'Agent':('An AI agent is a system in which a model selects actions or tool calls, observes results and decides how to continue towards a goal within defined limits.',AGENT),
'API':('An application programming interface is a defined contract through which software components request operations or exchange data.','https://developer.mozilla.org/en-US/docs/Glossary/API'),
'Webhook':('A webhook is an event notification that one system sends to a configured endpoint, commonly through an HTTP request.',AGENT),
'JSON':('JavaScript Object Notation is a text format for structured data. It supports objects, arrays, strings, numbers, booleans and null. Our tool request uses an object.','https://www.rfc-editor.org/rfc/rfc8259'),
'Bias and fairness':('Bias can mean systematic distortion in data or estimates. Fairness concerns whether system behaviour creates unjustified disadvantage; unequal error rates require investigation.',NIST),
'Hallucination':('A hallucination is generated content that is false, unsupported or inconsistent with the relevant source or task. Fluency does not establish accuracy.',NIST),
}
EXTRA={
'Neural network':'A neural network is a model composed of connected computational units that transform inputs using parameters, usually including nonlinear functions.',
'Attention':'Attention computes a weighted combination of representations, with weights determined by relationships between inputs. Attention weights alone do not explain a model’s decision.',
'Supervised learning':'Supervised learning fits a model using examples paired with target outputs.',
'Unsupervised learning':'Unsupervised learning identifies structure in data without supplied target labels for the task.',
'Reinforcement learning':'Reinforcement learning learns a policy for choosing actions from feedback expressed as rewards.',
'Self-supervised learning':'Self-supervised learning derives prediction targets from the data itself, rather than relying on separately supplied target labels.',
'Regression':'Regression predicts a numerical quantity.',
'Classification':'Classification assigns a category or estimates scores for predefined categories.',
'Embedding':'An embedding is a numerical representation learned or constructed so that relationships between items can be compared computationally.',
'Vector search':'Vector search retrieves items by comparing numerical representations using a similarity or distance measure.',
'Multimodal':'A multimodal model or system processes or generates more than one type of information, such as text, images or audio.',
'Prompt injection':'Prompt injection is an attempt to redirect an AI system through instructions placed in untrusted content.',
}
for k,v in EXTRA.items():D[k]=(v,LLM if k in ['Attention','Embedding','Multimodal','Neural network'] else ML)
def meaning(term):return D[term][0]
def source(term):return D[term][1]

D['Embedding']=(D['Embedding'][0],'https://developers.google.com/machine-learning/crash-course/embeddings/obtaining-embeddings')
D['Prompt injection']=(D['Prompt injection'][0],NIST)

# A field definition is distinct from OECD's AI-system definition.
D['AI']=(D['AI'][0],'https://www.ibm.com/think/topics/artificial-intelligence')
