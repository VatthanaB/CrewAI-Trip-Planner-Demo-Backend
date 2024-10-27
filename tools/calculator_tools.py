from langchain.tools import tool


# Defining a class 'CalculatorTools' to handle mathematical calculations
class CalculatorTools():

    # Using the 'tool' decorator to define a function for performing calculations
    # The function is labeled as "Make a calculation"
    @tool("Make a calculation")
    def calculate(operation):
        """This function performs mathematical calculations, such as addition, subtraction,
        multiplication, division, etc.
        The input should be a valid mathematical expression in string format.
        Examples of valid inputs: '200*7', '5000/2*10'
        """
        try:
            # Using 'eval()' to evaluate and execute the string expression as a Python expression
            return eval(operation)
        except SyntaxError:
            # Catching any syntax errors in case the input is not a valid mathematical expression
            return "Error: Invalid syntax in mathematical expression"

# from pydantic import BaseModel, Field
# from langchain.tools import tool

# # Define a Pydantic model for the tool's input parameters
# class CalculationInput(BaseModel):
#     operation: str = Field(..., description="The mathematical operation to perform")
#     factor: float = Field(..., description="A factor by which to multiply the result of the operation")

# # Use the tool decorator with the args_schema parameter pointing to the Pydantic model
# @tool("perform_calculation", args_schema=CalculationInput, return_direct=True)
# def perform_calculation(operation: str, factor: float) -> str:
#     """
#     Performs a specified mathematical operation and multiplies the result by a given factor.

#     Parameters:
#     - operation (str): A string representing a mathematical operation (e.g., "10 + 5").
#     - factor (float): A factor by which to multiply the result of the operation.

#     Returns:
#     - A string representation of the calculation result.
#     """
#     # Perform the calculation
#     result = eval(operation) * factor

#     # Return the result as a string
#     return f"The result of '{operation}' multiplied by {factor} is {result}."