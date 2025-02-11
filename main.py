import os
from compiler import compiler




class execute:
    def __init__(self):
        self.directory_path = os.path.join(os.getcwd(), "pdfs")
        self.url = "https://www.ibef.org/indian-exports"
        self.agent_executor = None  # Initialize attribute

    def create_agent(self):
        if self.agent_executor is None:  # Prevent redundant initialization
            self.agent_executor = compiler(self.directory_path, self.url).return_agent()
        return self.agent_executor

    def run(self, query):
        if self.agent_executor is None:
            self.create_agent()  # Ensure agent is created before using it

        try:
            response = self.agent_executor.invoke({"input": query})
            output = response.get("output", "")
            if not output or "error" in str(output).lower():
                return "I couldn't generate a complete response. Try rephrasing your question."
            return output

        except Exception as e:
            return f"I encountered an error: {str(e)}"



if __name__== "__main__":
    execute()
