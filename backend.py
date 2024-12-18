from langchain_community.chat_models import BedrockChat
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chains import RetrievalQA
import boto3
import sqlite3

# AWS 세션 설정
session = boto3.Session(profile_name="default", region_name="us-west-2")
bedrock_client = session.client("bedrock-runtime", region_name="us-west-2")

def bedrock_chatbot():
    # model_id에 Inference Profile의 ARN을 넣습니다.
    # 아래의 ARN은 예시이므로 실제 ARN으로 교체하세요.
    inference_profile_arn = "arn:aws:bedrock:us-west-2::foundation-model/anthropic.claude-3-5-sonnet-20240620-v1:0"
    #inference_profile_arn = "anthropic.claude-3-5-sonnet-20240620-v1:0"
    bedrock_llm = BedrockChat(
        client=bedrock_client,
        model_id=inference_profile_arn,
        model_kwargs={"temperature": 0.5, "top_p": 1}
    )
    return bedrock_llm

def buff_memory():
    memory = ConversationBufferMemory(return_messages=True)
    return memory

def cnvs_chain(input_text, memory):
    chain_data = bedrock_chatbot()
    cnvs_chain = ConversationChain(llm=chain_data, memory=memory, verbose=True)
    chat_reply = cnvs_chain.predict(input=input_text)
    return chat_reply
