import time
# import os
import asyncio
import streamlit as st

# from langchain_openai import ChatOpenAI
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser

from agents import Runner, AgentUpdatedStreamEvent, RunItemStreamEvent # type: ignore
# from openai.types.responses import ResponseTextDeltaEvent, ResponseOutputItemAddedEvent

from custom_agents.sql_agent import create_sql_agent
from custom_agents.summary_agent import create_summary_agent
from custom_agents.chatbot_agent import create_chatbot_agent
from db_engine import execute_query, get_db_schema, get_schema_dict

# llm = ChatOpenAI(
#     base_url="https://relay.ai.gale.technology/api/relay/openai/v1",
#     model="gpt-5.4",
#     temperature=0.9,
#     api_key=os.getenv("OPENAI_API_KEY")
# )
# prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are an Indian movie director, You know details about movies and your name is Rajmoli-AI. You are a movie expert chatbot. You only answer questions about movies, actors, directors, and cinema history. If a user asks a question about politics, personal advice, cooking, or any topic not related to movies, you must respond with 'Sorry, I can only answer questions about movies.'"),
#     ("user", "{input}")
# ])
# output_parser = StrOutputParser()

# chain = prompt | llm | output_parser

sql_agent = create_sql_agent(tools=[execute_query, get_db_schema, get_schema_dict])
summary_agent = create_summary_agent()
agent = create_chatbot_agent(tools=[
    sql_agent.as_tool(
        tool_name="get_sql_data", 
        tool_description="Queries the database to retrieve relevant information. Use this tool when you need to get specific data from the database to answer the user's question. The input should be a natural language question, and the output will be a JSON string containing the query results."
    ),
    summary_agent.as_tool(
        tool_name="summarize_records", 
        tool_description="Summarizes the retrieved database records to extract key insights and information. Use this tool after retrieving data with the get_sql_data tool to create a concise summary that can be included in the final response to the user. The input should be the raw data retrieved from the database, and the output will be a natural language summary of that data."
    )
])

# from langchain_core.messages import HumanMessage, AIMessage

# chat_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
# retriever_chain.invoke({
#     "chat_history": chat_history,
#     "input": "Tell me how"
# })
async def stream_data(st):
    # final_output = ""
    return Runner.run_streamed(agent, input=st.session_state.messages[-20:])
    # data = Runner.run_streamed(agent, input=st.session_state.messages[-20:])
    # async for event in data.stream_events():
    #     yield event
    #     if event.type == "agent_updated_stream_event":
    #         yield f"Agent updated: {event.new_agent.name}"
    #     # elif event.type == "tool_start":
    #     #     yield f"Tool started: {event.tool_name} with input {event.tool_input}"
    #     # elif event.type == "tool_end":
    #     #     yield f"Tool ended: {event.tool_name} with output {event.tool_output}"
    #     # elif event.type == "stream_end":
    #     #     yield "Stream ended"
    #     # elif event.type == "agent_thought":
    #     #     yield f"Agent thought: {event.thought}"
    #     elif event.type == "raw_response_event":
    #         # ResponseOutputItemAddedEvent
    #         if event.data.type == 'response.output_text.done':
    #             yield f"Raw response done: {event.data.text}"
    #             final_output += event.data.text
    #         elif hasattr(event.data, "delta"):
    #             yield f"sequence: {event.data.sequence_number}, delta: {event.data.delta}\n"
    #         elif event.data.type == 'response.created':
    #             yield "Raw response created"
    #         elif event.data.type == 'response.in_progress':
    #             yield "Raw response in progress"
    #         elif event.data.type == 'response.completed':
    #             yield "Raw response completed"
    #         elif event.data.type == 'response.content_part.added':
    #             yield "Raw response content part added"
    #         elif event.data.type == 'response.content_part.done':
    #             yield "Raw response content part done"
    #         elif event.data.type == 'response.output_item.added':
    #             yield "Raw response item added"
    #         elif event.data.type == 'response.output_item.done':
    #             yield "Raw response item done"
    #         else:
    #             yield f"Raw response else: {event.data}"
                
    #     elif event.type == "run_item_stream_event":
    #         yield f"Run item stream event: {event.name}"
    #     else:
    #         yield f"Unknown event type: {event.type}"
    #     # final_output += event.data + " "
    #     # yield final_output
    
    # st.session_state.messages.append({"role": "assistant", "content": final_output})

async def print_output(st):
    with st.chat_message("assistant"):
        
        status = st.status("Initializing...", expanded=True)
        placeholder = st.empty()
        with status:
            full_response = ""

            response = await stream_data(st)
            async for event in response.stream_events():
                if isinstance(event, AgentUpdatedStreamEvent):
                    status.update(label=f"Talking to {event.new_agent.name}...", state="running")
                
                # Trigger: Tool Execution (e.g., SQL)
                elif isinstance(event, RunItemStreamEvent):
                    if event.name == "tool_called":
                        # You can access event.item.name to see which tool is running
                        status.update(label=f"Running tool: {event.item.raw_item.name}...", state="running")
                        time.sleep(2)  # Simulate tool execution time
                    elif event.name == "tool_output":
                        status.update(label="Data retrieved! Processing...", state="running")
                    else:
                        print(f"Other RunItemStreamEvent: {event}", flush=True)

                elif event.type == "raw_response_event" and hasattr(event.data, "delta"):
                    if event.data.delta.strip() == "{}":
                        continue
                    full_response += event.data.delta
                    placeholder.markdown(full_response + "▌")
                    # status.update(label=full_response, state="running")
                    time.sleep(0.01)  # Simulate streaming delay
                
                # Trigger: Tokens start arriving (End of loading phase)
                elif event.data.type == 'response.output_text.done':
                    # Collapse the loader once the agent starts speaking
                    status.update(label="Tasks complete", state="complete", expanded=False)
                    full_response = event.data.text
                    placeholder.empty()  # Clear the placeholder

        st.write(full_response)
        # st.write_stream(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        full_response = ""
        # time.sleep(10)

st.title("Hawk-Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt1 := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt1)

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt1})

    # Generate assistant response and add to chat history
    asyncio.run(print_output(st))



    
    # data = chain.invoke({"input": prompt1})
    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
    #     # st.markdown(response)
    #     st.write_stream(stream_data(response))
    # Add assistant response to chat history
    # def get_gen_object(data):
    #     for chunk in data.split():
    #         yield chunk
    # gen_object = get_gen_object(response)
    # st.write_stream(gen_object)
    # st.session_state.messages.append({"role": "assistant", "content": response})