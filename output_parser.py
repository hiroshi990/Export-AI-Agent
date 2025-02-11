from langchain.schema import AgentAction,AgentFinish
from langchain.agents import AgentOutputParser
from typing import Union
import re


class custom_output_parser(AgentOutputParser):
    """class to handle the output generated by the LLM"""

    def parse(self, agent_output: str) -> Union[AgentAction, AgentFinish]:
        if "Final Answer:" in agent_output:
            return AgentFinish(
                return_values={"output": agent_output.split("Final Answer:")[-1].strip()},
                log=agent_output,
            )

        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, agent_output, re.DOTALL)
        if not match:
            raise ValueError(f"Could not parse LLM output: `{agent_output}`")

        action = match.group(1).strip()
        action_input = match.group(2)
        return AgentAction(tool=action, tool_input=action_input.strip(" ").strip('"'), log=agent_output)

