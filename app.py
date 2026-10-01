import os
import re
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, request, jsonify, render_template

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, AIMessage

from crewai import LLM, Crew, Agent, Task
from crewai_tools import SerperDevTool

from langgraph.checkpoint.memory import MemorySaver

# ── OpenRouter config ─────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


# ── CrewAI travel planner ─────────────────────────────────────────────────────
def run_travel_planner_crew(place: str, days: str, budget: str) -> str:
    crew_llm = LLM(
        model="openrouter/openai/gpt-4o-mini",
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
        temperature=0.7
    )

    search_place_agent = Agent(
        role=f"{place} finder for vacation",
        goal="To find less crowded or very silent places for traveling nearby the main destination.",
        backstory="You are an influencer who travels the entirety of India, specializing in hidden gems.",
        llm=crew_llm,
        tools=[SerperDevTool()],
        verbose=True
    )

    booking_agent = Agent(
        role="Travel Planner",
        goal=f"Take the isolated spots from search_place_agent and build a full itinerary for {days} days within a budget of {budget}.",
        backstory="You are a meticulous travel agent who organizes transit options and hotel stays.",
        llm=crew_llm,
        tools=[SerperDevTool()],
        verbose=True
    )

    search_task = Task(
        description=f"Find places that are less crowded and make a list of areas within an approximate 50 km radius of {place}.",
        agent=search_place_agent,
        expected_output=f"A clean list of offbeat spots nearby {place}."
    )

    booking_task = Task(
        description=f"Plan logistics (train/flight/bus) and accommodation options for {place} within a total budget of {budget} for {days} days.",
        agent=booking_agent,
        expected_output="An itemized list of travel options with costs, recommended hotel options with pricing, and a total expense breakdown.",
        context=[search_task]
    )

    crew = Crew(
        agents=[search_place_agent, booking_agent],
        tasks=[search_task, booking_task],
        memory=True,
        verbose=True
    )
    return str(crew.kickoff(inputs={"place": place, "days": days, "budget": budget}))


# ── LangGraph setup ───────────────────────────────────────────────────────────
memory = MemorySaver()


class State(TypedDict):
    messages: Annotated[list, add_messages]


llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0
)


def calling_llm(state: State):
    system_instruction = SystemMessage(
        content="You are ARVEX, a premium AI travel assistant. If the user wants to plan a trip, vacation, or itinerary, "
                "you MUST start your response with this exact command format:\n"
                "NEED_PLAN: place='<destination>', days='<number>', budget='<amount>'\n"
                "Fill in the destination, days, and budget from the conversation. If any detail is missing, ask the user for it first.\n"
                "If they are just asking a normal follow-up question, reply normally without the NEED_PLAN tag."
    )
    conversation = [system_instruction] + state["messages"]
    response = llm.invoke(conversation)
    return {"messages": [response]}


def crew_planner_node(state: State):
    last_message_text = state["messages"][-1].content

    place = re.search(r"place='([^']+)'", last_message_text).group(1)
    days = re.search(r"days='([^']+)'", last_message_text).group(1)
    budget = re.search(r"budget='([^']+)'", last_message_text).group(1)

    print(f"\n[ARVEX] Routing → Place: {place}, Days: {days}, Budget: {budget}. Launching CrewAI...")

    itinerary = run_travel_planner_crew(place=place, days=days, budget=budget)

    return {"messages": [AIMessage(content=f"Here is your complete itinerary crafted by ARVEX:\n\n{itinerary}")]}


def route_decision(state: State):
    last_message_text = state["messages"][-1].content
    if "NEED_PLAN:" in last_message_text:
        return "crew_planner"
    return END


builder = StateGraph(State)
builder.add_node("calling_llm", calling_llm)
builder.add_node("crew_planner", crew_planner_node)

builder.add_edge(START, "calling_llm")
builder.add_conditional_edges(
    "calling_llm",
    route_decision,
    {"crew_planner": "crew_planner", END: END}
)
builder.add_edge("crew_planner", "calling_llm")

graph = builder.compile(checkpointer=memory)


# ── Flask app ─────────────────────────────────────────────────────────────────
flask_app = Flask(__name__)


@flask_app.route("/")
def index():
    return render_template("index.html")


@flask_app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    thread_id = data.get("thread_id", "default_thread")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    config = {"configurable": {"thread_id": thread_id}}

    try:
        response = graph.invoke({"messages": [user_message]}, config=config)
        bot_reply = response["messages"][-1].content
        clean_reply = re.sub(r"NEED_PLAN:.*?\n", "", bot_reply).strip()
        return jsonify({"reply": clean_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("ARVEX Travel Agent starting on http://localhost:5000")
    flask_app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)