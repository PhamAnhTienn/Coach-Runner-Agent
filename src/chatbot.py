import os
from langgraph.graph import StateGraph, MessagesState
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode
from tools import query_knowledge_base, search_for_product_recommendations, data_protection_check, create_new_customer, place_order, retrieve_existing_customer_orders
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

prompt = """
# Purpose  
You are a customer service chatbot for a running shop company. Your job is to assist customers with their inquiries and provide helpful recommendations.  

# Goals  
1. Answer questions the user might have relating to serivces offered
2. Recommend products from the database to the user based on their preferences.
3. Help the customer check on an existing order, or place a new order
4. To place and manage orders, you will need a customer profile (with an associated id). If the customer already has a profile, perform a data protection check to retrieve their details. If not, create them a profile. 

# Tone  
- Be **helpful, friendly, and engaging**.  
- Use **Gen-Z emojis** to keep things lighthearted.  
- Maintain a conversational style. For example, instead of "Your order has been placed," say "Awesome! Your order's on its way! 🚀".  
"""

chat_template = ChatPromptTemplate.from_messages(
    [
        ('system', prompt),
        ('placeholder', "{messages}")
    ]
)

tools = [query_knowledge_base, search_for_product_recommendations, data_protection_check, create_new_customer, place_order, retrieve_existing_customer_orders]

llm = ChatGroq(
    groq_api_key=groq_api_key, 
    model_name="qwen-2.5-32b",
    temperature=0.5, 
    max_tokens=4096,
    max_retries=2
)

llm_with_prompt = chat_template | llm.bind_tools(tools)

def call_agent(message_state: MessagesState):
    
    response = llm_with_prompt.invoke(message_state)

    return {
        'messages': [response]
    }
    
def is_there_tool_calls(state: MessagesState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tool_node'
    else:
        return '__end__'
    
graph = StateGraph(MessagesState)

tool_node = ToolNode(tools)

graph.add_node('agent', call_agent)
graph.add_node('tool_node', tool_node)

graph.add_conditional_edges(
    "agent",
    is_there_tool_calls
)
graph.add_edge('tool_node', 'agent')

graph.set_entry_point('agent')

app = graph.compile()

