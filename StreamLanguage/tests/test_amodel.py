import unittest

from StreamLanguage.ast.context import Context
from StreamLanguage.ast.nodes.error_handling import TryCatchNode
from StreamLanguage.ast.nodes.expressions import IdentifierNode, AssignmentNode, BinaryOperationNode, UnaryOperationNode
from StreamLanguage.ast.nodes.flow_control import IfNode
from StreamLanguage.ast.nodes.functions import ReturnNode, FunctionNode, FunctionCallNode, LambdaNode, ApplyNode
from StreamLanguage.ast.nodes.structure import VariableDeclarationNode
from StreamLanguage.ast.nodes.types import PrimitiveIntNode, PrimitiveStringNode, ArrayNode


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
        function_node.evaluate(self.context)
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
        function_node.evaluate(self.context)
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


    def test_addition(self):
        """Test BinaryOperationNode for addition."""
        addition = BinaryOperationNode('+', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = addition.evaluate(self.context)
        self.assertEqual(result, 8)

    def test_subtraction(self):
        """Test BinaryOperationNode for subtraction."""
        subtraction = BinaryOperationNode('-', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = subtraction.evaluate(self.context)
        self.assertEqual(result, 2)

    def test_multiplication(self):
        """Test BinaryOperationNode for multiplication."""
        multiplication = BinaryOperationNode('*', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = multiplication.evaluate(self.context)
        self.assertEqual(result, 15)

    def test_division(self):

        """Test BinaryOperationNode for division."""
        division = BinaryOperationNode('/', PrimitiveIntNode(6), PrimitiveIntNode(3))
        result = division.evaluate(self.context)
        self.assertEqual(result, 2)

    def test_greater_than(self):
        """Test BinaryOperationNode for greater than comparison."""
        greater_than = BinaryOperationNode('>', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = greater_than.evaluate(self.context)
        self.assertTrue(result)

    def test_less_than(self):
        """Test BinaryOperationNode for less than comparison."""
        less_than = BinaryOperationNode('<', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = less_than.evaluate(self.context)
        self.assertFalse(result)

    def test_equality(self):
        """Test BinaryOperationNode for equality comparison."""
        equality = BinaryOperationNode('==', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = equality.evaluate(self.context)
        self.assertFalse(result)

    def test_inequality(self):
        """Test BinaryOperationNode for inequality comparison."""
        inequality = BinaryOperationNode('!=', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = inequality.evaluate(self.context)
        self.assertTrue(result)

    def test_and(self):
        """Test BinaryOperationNode for logical AND."""
        and_op = BinaryOperationNode('&&', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = and_op.evaluate(self.context)
        self.assertTrue(result)

    def test_or(self):
        """Test BinaryOperationNode for logical OR."""
        or_op = BinaryOperationNode('||', PrimitiveIntNode(5), PrimitiveIntNode(3))
        result = or_op.evaluate(self.context)
        self.assertTrue(result)

    def test_not(self):
        """Test BinaryOperationNode for logical NOT."""
        not_op = UnaryOperationNode('!', PrimitiveIntNode(5))
        result = not_op.evaluate(self.context)
        self.assertFalse(result)

    def test_negation(self):
        """Test UnaryOperationNode for negation."""
        negation = UnaryOperationNode('-', PrimitiveIntNode(5))
        result = negation.evaluate(self.context)
        self.assertEqual(result, -5)

    def test_positive(self):
        """Test UnaryOperationNode for positive."""
        positive = UnaryOperationNode('+', PrimitiveIntNode(5))
        result = positive.evaluate(self.context)
        self.assertEqual(result, 5)

    def test_function_overloading(self):
        """Test function overloading with different parameter counts."""
        params = [IdentifierNode('a'), IdentifierNode('b')]
        body = [ReturnNode(BinaryOperationNode('+', IdentifierNode('a'), IdentifierNode('b')))]
        function = FunctionNode('add', params, body)
        function.evaluate(self.context)

        # Now define a function with a single parameter
        params = [IdentifierNode('a')]
        body = [ReturnNode(IdentifierNode('a'))]
        function = FunctionNode('add', params, body)
        function.evaluate(self.context)

        # Now invoke the function with a single argument
        func_call = FunctionCallNode(IdentifierNode('add'), [PrimitiveIntNode(5)])
        result = func_call.evaluate(self.context)
        self.assertEqual(result, 5)
if __name__ == '__main__':
    unittest.main()
