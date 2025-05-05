# install letta_client with `pip install letta-client`
from letta_client import Letta

# create a client to connect to your local Letta Server
client = Letta(
  base_url="http://localhost:8283"
)

# create an agent with two basic self-editing memory blocks
agent_state = client.agents.create(
    memory_blocks=[
        {
          "label": "human",
          "value": "The human's name is Bob the Builder."
        },
        {
          "label": "persona",
          "value": "My name is Sam, the all-knowing sentient AI."
        }
    ],
    model="openai/gpt-4o-mini",
    context_window_limit=16000,
    embedding="openai/text-embedding-3-small"
)

# the AgentState object contains all the information about the agent
print(agent_state)
