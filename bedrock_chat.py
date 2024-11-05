from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_aws.retrievers import AmazonKnowledgeBasesRetriever
from botocore.client import Config
from langchain_aws import ChatBedrock

import boto3
import json
import os
import sys



def get_claudeV3_llm():
    
    sts_client = boto3.client('sts')
    boto3_session = boto3.session.Session()
    region_name = boto3_session.region_name

    bedrock_config = Config(connect_timeout=120, read_timeout=120, retries={'max_attempts': 0}, region_name=region_name)
    bedrock_client = boto3_session.client("bedrock-runtime",
                              config=bedrock_config)
    
    claude_parameters = {
                   'max_tokens':4096, 
                    "temperature":0,
                    "top_k":250,
                    "top_p":1,
                    "stop_sequences": ["\n\nHuman"],
                }

    claude_llm = ChatBedrock(model_id = 'anthropic.claude-3-haiku-20240307-v1:0',
                    client = bedrock_client, 
                    model_kwargs = claude_parameters 
                    )
    return claude_llm

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

MAX_HISTORY_LENGTH = 5

def build_chain(model="claude_haiku"):
    region = os.environ["AWS_REGION"]
    bedrock_kb_id = os.environ["BEDROCK_KB_ID"]

    if model=="claude_haiku":
        llm=get_claudeV3_llm()
    

    retriever = AmazonKnowledgeBasesRetriever(knowledge_base_id=bedrock_kb_id,region_name=region, retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}})
    prompt_template = """\n\nHuman:The following is a friendly conversation between a human and an AI. \
        The AI is talkative and provides lots of specific details from its <context>. If the AI does not \
        know the answer to a <question>, it truthfully says it does not know.
        <context>{context}</context>
        Answer the below question as truthfully as possible based on above <context>.
        <question>{question}</question>
        \n\nAssistant:
        """

    PROMPT = PromptTemplate(
      template=prompt_template, input_variables=["context", "question"]
    )
    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm, 
        chain_type="stuff", 
        retriever=retriever, 
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )
    return qa

def run_chain(chain, prompt: str, history=[]):
    result = chain(prompt)
    print(result)
    
    return {
        "answer": result['result'],
        "source_documents": result['source_documents']
    }

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        chain = build_chain(sys.argv[1])
    else:
        chain = build_chain()

    result = run_chain(chain, "What is Sagemaker?")
    print(result['answer'])
    if 'source_documents' in result:
        print('Sources:')
        for d in result['source_documents']:
          print(d.metadata['source'])
