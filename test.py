# install letta_client with `pip install letta-client`
from letta_client import Letta
import httpx # For catching specific connection errors

# create a client to connect to your local Letta Server
client = Letta(
  base_url="http://127.0.0.1:8283" # Using 127.0.0.1
)

print("Inspecting client.agents before any server call...")
print("Dir client.agents:")
client_agents_dir = dir(client.agents)
print(client_agents_dir)

if hasattr(client.agents, '__doc__') and client.agents.__doc__:
    print("\nDocstring for client.agents:")
    print(client.agents.__doc__)
else:
    print("\nclient.agents has no extensive docstring attribute.")

# From the dir output, 'messages' looks like a relevant attribute for interaction.
# Let's inspect client.agents.messages if it exists.
if 'messages' in client_agents_dir:
    print("\nDir client.agents.messages:")
    try:
        print(dir(client.agents.messages))
        if hasattr(client.agents.messages, '__doc__') and client.agents.messages.__doc__:
            print("\nDocstring for client.agents.messages:")
            print(client.agents.messages.__doc__)
        else:
            print("\nclient.agents.messages has no extensive docstring attribute.")
    except Exception as e:
        print(f"Could not inspect client.agents.messages: {e}")
else:
    print("\n'messages' attribute not found directly on client.agents. Further exploration would be needed if agent creation succeeded.")


agent_state = None
print("\nAttempting to create agent...")
try:
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
    print("\nAgent State (if created):")
    print(agent_state)

except httpx.ConnectError as e:
    print(f"\nFailed to connect to Letta server at http://127.0.0.1:8283: {e}")
    print("This is an httpx.ConnectError. Ensure the Letta server is running.")
    print("Cannot proceed with live agent interaction as agent creation failed.")
    agent_state = None
except Exception as e:
    print(f"\nAn unexpected error occurred during agent creation: {e}")
    print("Cannot proceed with live agent interaction.")
    agent_state = None


if agent_state and agent_state.id:
    print(f"\nAgent created successfully. Agent ID: {agent_state.id}")
    print("Proceeding to explore interaction via client.agents.messages (based on dir output)...")

    # The 'messages' attribute on client.agents seems like the most plausible path.
    # It's likely a sub-client for managing chat messages.
    # Common methods would be 'create', 'list', etc.
    # Let's assume client.agents.messages.create() is the method.
    if 'messages' in client_agents_dir and hasattr(client.agents.messages, 'create'):
        print("\nAttempting interaction with client.agents.messages.create():")
        try:
            prompts = [
                "What is your name?",
                "What is the human's name?"
            ]
            for p_text in prompts:
                print(f"\nAsking: \"{p_text}\" using client.agents.messages.create()")
                # This is a guess for the message structure.
                # It typically involves the agent_id and a list of message objects.
                # The actual response from .create() might be just the created message,
                # or it might be a more complex object including the agent's reply if it's synchronous.
                # Often, one creates a user message, and then the system generates an assistant message.
                
                # Option 1: Creating a message and hoping it triggers a response (less direct for chat)
                # created_message = client.agents.messages.create(
                #     agent_id=agent_state.id,
                #     role="user", # Assuming parameters like role and content
                #     content=p_text
                # )
                # print(f"Response from messages.create() (for user message '{p_text}'):")
                # print(created_message)
                # To get the agent's reply, one might then need to list messages or check a stream.

                # Option 2: A more direct chat-like interaction if available on messages client
                # Some clients might have a method on the messages sub-client that is like create_chat_completion
                # For now, we'll stick to the idea of "creating a user message" and logging that.
                # The actual mechanism to get the *agent's reply* needs to be discovered.
                # It could be implicit (agent replies in the background and updates a list)
                # or require another call (e.g. client.agents.messages.get_latest_reply(agent_id=...))

                # Let's assume for exploration that `messages.create` might directly return or lead to a completion.
                # This is speculative without API docs.
                # A more robust approach often involves a "run" or "invoke" type method on the agent or a session.
                # Since dir(client.agents) did not show create_chat_completion,
                # and dir(agent_state) is not available yet, this is an educated guess.

                print(f"Note: The exact way to use 'client.agents.messages.create()' for a request-response chat")
                print(f"is not fully known without documentation. It might just add a user message to a log,")
                print(f"requiring another step to get the agent's reply.")
                print(f"If 'client.agents.messages' had a method like 'get_completion' or 'chat', that would be used.")
                
                # Since the server is down, we can't test this live.
                # This part of the code shows the *intended exploration path*.
                print(f"Placeholder for attempting to send '{p_text}' and retrieve a reply via client.agents.messages interface.")


        except Exception as e:
            print(f"Error during client.agents.messages.create() attempt: {e}")
    else:
        print("\nclient.agents.messages.create() not found or 'messages' not on client.agents.")
        print("Further investigation of the client library's specific API for chat interactions would be needed.")

    # Introspection on agent_state object itself
    print("\nDir agent_state (if agent was created):")
    print(dir(agent_state))

    # Checking for direct interaction methods on agent_state
    print("\nChecking for direct interaction methods on agent_state object:")
    # ... (rest of the agent_state introspection from previous script)
    for method_name in ['chat', 'query', 'run', 'invoke', 'create_chat_completion']:
        if hasattr(agent_state, method_name):
            print(f"agent_state has method: .{method_name}() - attempting call.")
            try:
                # This is a generic attempt; actual arguments might differ
                # For create_chat_completion, it would need a 'messages' list
                if method_name == 'create_chat_completion':
                    response = getattr(agent_state, method_name)(messages=[{"role": "user", "content": "What is your name?"}])
                else: # Assuming a simple prompt for others
                    response = getattr(agent_state, method_name)(prompt="What is your name?")
                print(f"Response from agent_state.{method_name}(): {response}")
            except Exception as e:
                print(f"Error calling agent_state.{method_name}(): {e}")
        else:
            print(f"agent_state does not have a .{method_name}() method.")

else:
    print("\nSkipping agent interaction attempts because agent was not created (likely due to server connection issues or other creation error).")

print("\n--- Script finished ---")
