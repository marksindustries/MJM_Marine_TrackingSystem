from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from models import llm, embeddings
from questionsMethods import QuestionsMethods
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain


def ProcessDocuments(file, questions_list, data):
    # Load the PDF file using the correct path
    loader = UnstructuredFileLoader(file)

    documents = loader.load()
    # split the documents into chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=2000, chunk_overlap=20)
    texts = text_splitter.split_documents(documents=documents)

    embeddings = HuggingFaceEmbeddings()
    # create the vectorestore to use as the index
    db = Chroma.from_documents(texts, embeddings)
    # expose this index in a retriever interface
    retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": 2})

    template = """
        You are an expert on insurance policies. 
        Please answer the question based only on the provided context. 
        If the answer is not mentioned in the context, respond with 'Not Found'. 
        Provide your answer in one or two words only.

        Context: {context}

        Question: {question}

        Answer: 
        
    """

    prompt = PromptTemplate(
        template=template,
        input_variables=["context", "question"])

    qa = RetrievalQA.from_chain_type(
        llm=llm(),
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt})

    answers = QuestionsMethods.ProcessQuestionsMethod(
        qa, questions_list, data)

    return answers


def composeMail(context):

    email_template = """
    You are tasked with composing an email to a subcontractor requesting information that is mentioned as "Not Found" or "missing" in the context provided.

    Context: 
    {context}

    Please compose an email requesting the necessary information.

    Email Draft:

"""

    prompt_mail = PromptTemplate(
        template=email_template,
        input_variables=["context"])

    chain = LLMChain(prompt=prompt_mail, llm=llm())

    answer = chain.invoke({"context": context})

    return answer['text']
