import unittest
from lib2to3.fixes.fix_input import context

from a_model import (
    Context,
    ProgramNode,
    IfNode,
    WhileNode,
    ForNode,
    AssignmentNode,
    BinaryOperationNode,
    UnaryOperationNode,
    FunctionCallNode,
    ReturnNode,
    IdentifierNode,
    PrimitiveIntNode,
    PrimitiveFloatNode,
    PrimitiveStringNode,
    VariableDeclarationNode,
    ArrayNode,
    FunctionNode,
    LambdaNode,
    ApplyNode,
    TryCatchNode,
    ParserError,
)


class TestASTModel(unittest.TestCase):
    def setUp(self):
        """Set up a fresh context for each test."""
        self.context = Context()

    def test_primitive_int_node(self):
        """Test evaluation and type of a PrimitiveIntNode."""
        node = PrimitiveIntNode(5)
        self.assertEqual(node.evaluate(self.context), 5)
        self.assertEqual(node.get_type(self.context), int)

    def test_assignment_node(self):
        """Test AssignmentNode evaluation and type inference."""
        var_decl = VariableDeclarationNode(IdentifierNode('x'), value=PrimitiveIntNode(10))
        var_decl.evaluate(self.context)
        assignment = AssignmentNode(IdentifierNode('x'),
                                    BinaryOperationNode('+', IdentifierNode('x'), PrimitiveIntNode(5)))
        result = assignment.evaluate(self.context)
        self.assertEqual(result, 15)
        self.assertEqual(self.context.get_type('x'), int)

    def test_if_node(self):
        """Test IfNode evaluation with both true and false branches within a function context."""
        # Create a function node to encapsulate the if statement
        func_body = []
        condition = BinaryOperationNode('>', PrimitiveIntNode(10), PrimitiveIntNode(5))
        then_block = [ReturnNode(PrimitiveIntNode(1))]
        else_block = [ReturnNode(PrimitiveIntNode(0))]
        if_node = IfNode(condition, then_block, else_block)
        func_body.append(if_node)

        # Define the function with the if statement as its body
        function_node = FunctionNode("testFunc", [], func_body, return_type=int)

        # Declare and evaluate the function in the context
        self.context.declare_function("testFunc", function_node)
        func_call = FunctionCallNode(IdentifierNode("testFunc"), [])
        result = func_call.evaluate(self.context)

        # Assert that the correct value is returned when the condition is true
        self.assertEqual(result, 1)

        # Now test the else branch by changing the condition
        func_body = []
        condition = BinaryOperationNode('<', PrimitiveIntNode(10), PrimitiveIntNode(5))
        if_node = IfNode(condition, then_block, else_block)
        func_body.append(if_node)

        # Redefine the function with the updated if statement
        function_node = FunctionNode("testFunc", [], func_body, return_type=int)
        self.context.declare_function("testFunc", function_node)
        result = func_call.evaluate(self.context)

        # Assert that the correct value is returned when the condition is false
        self.assertEqual(result, 0)

    def test_function_node(self):
        """Test FunctionNode evaluation and invocation."""
        params = [IdentifierNode('a'), IdentifierNode('b')]
        body = [ReturnNode(BinaryOperationNode('+', IdentifierNode('a'), IdentifierNode('b')))]
        function = FunctionNode('add', params, body)
        function.evaluate(self.context)

        # Now invoke the function
        func_call = FunctionCallNode(IdentifierNode('add'), [PrimitiveIntNode(2), PrimitiveIntNode(3)])
        result = func_call.evaluate(context= self.context)
        self.assertEqual(result, 5)

    def test_try_catch_node(self):
        """Test TryCatchNode for handling exceptions."""
        try_block = [
            BinaryOperationNode('/', PrimitiveIntNode(10), PrimitiveIntNode(0))]  # Will raise ZeroDivisionError
        catch_block = (ZeroDivisionError, [ReturnNode(PrimitiveStringNode("Caught an error"))])
        try_catch_node = TryCatchNode(try_block, catch_block)
        result = try_catch_node.evaluate(self.context)
        self.assertEqual(result, "Caught an error")

    def test_array_node(self):
        """Test ArrayNode for correct evaluation and type checking."""
        array_node = ArrayNode([PrimitiveIntNode(1), PrimitiveIntNode(2), PrimitiveIntNode(3)])
        result = array_node.evaluate(self.context)
        self.assertEqual(result, [1, 2, 3])
        self.assertEqual(array_node.get_type(self.context), [int])

    def test_lambda_node(self):
        """Test LambdaNode evaluation and invocation."""
        params = [IdentifierNode('x')]
        body = ReturnNode(BinaryOperationNode('*', IdentifierNode('x'), PrimitiveIntNode(2)))
        lambda_node = LambdaNode(params, body)

        lambda_func = lambda_node.evaluate(self.context)
        result = lambda_func(5)
        self.assertEqual(result, 10)

    def test_apply_node(self):
        """Test ApplyNode for correct function application."""
        params = [IdentifierNode('x')]
        body = ReturnNode(BinaryOperationNode('*', IdentifierNode('x'), PrimitiveIntNode(2)))
        lambda_node = LambdaNode(params, body)
        apply_node = ApplyNode(lambda_node, [PrimitiveIntNode(3)])
        result = apply_node.evaluate(self.context)
        self.assertEqual(result, 6)

    def test_variable_declaration_node(self):
        """Test VariableDeclarationNode for proper type inference and evaluation."""
        var_decl = VariableDeclarationNode(IdentifierNode('x'), value=PrimitiveIntNode(10))
        var_decl.evaluate(self.context)
        result = self.context.lookup('x')
        self.assertEqual(result, 10)
        self.assertEqual(self.context.get_type('x'), int)


if __name__ == '__main__':
    unittest.main()
