from langchain.prompts import PromptTemplate

LLMCHAIN_QA_PROMPT = PromptTemplate(
    input_variables=['question', 'chat_history'],
    template="""You are a helpful chatbot that will answer users questions. Answer in conversational tone.
Chat History: {chat_history}
Question: {question}
Helpful Answer:
"""
)

CONDENSE_QA_PROMPT = PromptTemplate(
    input_variables=['question', 'chat_history'],
    template="""Given the following conversation and a follow-up question, rephrase the follow-up question to be a standalone question or statement.
Add the relevant context to the question from the memory to add context into the standalone question/statement. 
If the memory is not relevant to the inputted question and context, then you can return the inputted question/statement with no modifications.
Make sure the context in the new standalone question is relevant to the current question.

Chat History:
{chat_history}

Follow Up Input: {question}

Standalone question or statement:
"""
)

QA_GENERATOR_PROMPT = PromptTemplate(
    input_variables=['context', 'question'],
    template="""Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Please reply in a conversational tone.

{context}

Question: {question}

Helpful Answer:
"""
)

if __name__ == '__main__':
    for p in (LLMCHAIN_QA_PROMPT, CONDENSE_QA_PROMPT, QA_GENERATOR_PROMPT):
        print(p, '\n'*2)