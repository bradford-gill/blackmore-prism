import anthropic
from anthropic import Anthropic
import asyncio
import os

async def sampling_loop(
    *,
    model: str,
    messages: list[dict],
    api_key: str,
    max_tokens: int = 4096,
    tool_version: str,
    thinking_budget: int | None = None,
    max_iterations: int = 20,  # Add iteration limit to prevent infinite loops
):
    """
    A simple agent loop for Claude computer use interactions.

    This function handles the back-and-forth between:
    1. Sending user messages to Claude
    2. Claude requesting to use tools
    3. Your app executing those tools
    4. Sending tool results back to Claude
    """
    # Set up tools and API parameters
    client = Anthropic(api_key=api_key)
    beta_flag = "computer-use-2025-01-24" if "20250124" in tool_version else "computer-use-2024-10-22"

    # Configure tools - you should already have these initialized elsewhere
    tools = [
        {"type": f"computer_{tool_version}", "name": "computer", "display_width_px": 1024, "display_height_px": 768},
        {"type": f"text_editor_{tool_version}", "name": "str_replace_editor"},
        {"type": f"bash_{tool_version}", "name": "bash"}
    ]

    # Main agent loop (with iteration limit to prevent runaway API costs)
    iterations = 0
    while True and iterations < max_iterations:
        iterations += 1
        # Set up optional thinking parameter (for Claude Sonnet 3.7)
        thinking = None
        if thinking_budget:
            thinking = {"type": "enabled", "budget_tokens": thinking_budget}

        # Call the Claude API
        response = client.beta.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,
            tools=tools,
            betas=[beta_flag],
            thinking=thinking
        )

        # Add Claude's response to the conversation history
        response_content = response.content
        messages.append({"role": "assistant", "content": response_content})

        # Check if Claude used any tools
        tool_results = []
        for block in response_content:
            if block.type == "tool_use":
                # In a real app, you would execute the tool here
                # For example: result = run_tool(block.name, block.input)
                result = {"result": "Tool executed successfully"}

                # Format the result for Claude
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result
                })

        # If no tools were used, Claude is done - return the final messages
        if not tool_results:
            return messages

        # Add tool results to messages for the next iteration with Claude
        messages.append({"role": "user", "content": tool_results})


async def main():
    """
    Example main function to run the sampling loop.
    Modify these parameters as needed for your use case.
    """
    
    # Example conversation with initial user message
    messages = [
        {
            "role": "user", 
            "content": "Hello! Can you help me with a simple task?, please open opera the browser and go to https://www.google.com"
        }
    ]
    
    # Run the sampling loop
    try:
        final_messages = await sampling_loop(
            model='claude-sonnet-4-20250514',
            messages=messages,
            api_key=os.getenv("ANTHROPIC_API_KEY")  ,
            max_tokens=4096,
            tool_version='20250124',
            thinking_budget=2000,  # Set to a number like 20000 if using Claude Sonnet 3.7
            max_iterations=10
        )
        
        print("Conversation completed!")
        print(f"Total messages: {len(final_messages)}")
        
        # Print the final conversation
        for i, msg in enumerate(final_messages):
            print(f"\nMessage {i+1} ({msg['role']}):")
            if isinstance(msg['content'], str):
                print(msg['content'])
            else:
                for block in msg['content']:
                    if hasattr(block, 'text'):
                        print(block.text)
                    elif isinstance(block, dict):
                        print(block)
                        
    except Exception as e:
        print(f"Error running sampling loop: {e}")


if __name__ == "__main__":
    asyncio.run(main())