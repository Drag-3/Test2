import unittest
from StreamLanguage.sl_types.data_instances.primatives.integer import SLInteger
from StreamLanguage.sl_types.data_instances.primatives.float import SLFloat
from StreamLanguage.sl_types.data_instances.collections.array import SLArray
from StreamLanguage.sl_types.data_instances.primatives.string import SLString
from StreamLanguage.sl_types.meta_type.primatives.integer_type import SLIntegerType
from StreamLanguage.sl_types.meta_type.primatives.float_type import SLFloatType
from StreamLanguage.sl_types.meta_type.collections.array_type import SLArrayType

class TestSLTypes(unittest.TestCase):

    def test_slinteger_creation(self):
        """Test creating an SLInteger instance."""
        int_obj = SLInteger(5)
        self.assertEqual(int_obj.value, 5)
        self.assertIsInstance(int_obj, SLInteger)

    def test_slfloat_creation(self):
        """Test creating an SLFloat instance."""
        float_obj = SLFloat(5.5)
        self.assertEqual(float_obj.value, 5.5)
        self.assertIsInstance(float_obj, SLFloat)

    def test_type_conversion_integer_to_float(self):
        """Test converting SLInteger to SLFloat."""
        int_obj = SLInteger(5)
        float_obj = SLFloat(int_obj)
        self.assertEqual(float_obj.value, 5.0)
        self.assertIsInstance(float_obj, SLFloat)

    def test_type_conversion_float_to_integer(self):
        """Test converting SLFloat to SLInteger."""
        float_obj = SLFloat(5.8)
        int_obj = SLInteger(float_obj)
        self.assertEqual(int_obj.value, 5)  # Truncation
        self.assertIsInstance(int_obj, SLInteger)

    def test_slarray_creation(self):
        """Test creating an SLArray instance."""
        array_obj = SLArray([SLInteger(1), SLInteger(2), SLInteger(3)])
        self.assertEqual(len(array_obj.value), 3)
        self.assertIsInstance(array_obj, SLArray)
        self.assertEqual(array_obj.value[0].value, 1)

    def test_array_operations(self):
        """Test array append, get, and slice operations."""
        array_obj = SLArray([SLInteger(1), SLInteger(2)])
        array_obj.append(SLInteger(3))
        self.assertEqual(array_obj.value[-1].value, 3)

        # Test array get
        self.assertEqual(array_obj.get(1).value, 2)

        # Test array slice
        sliced_array = array_obj.slice(1, 3)
        self.assertEqual(sliced_array[0].value, 2)
        self.assertEqual(len(sliced_array), 2)

    def test_slinteger_addition(self):
        """Test adding two SLInteger instances."""
        int_obj1 = SLInteger(3)
        int_obj2 = SLInteger(7)
        result = int_obj1 + int_obj2
        self.assertEqual(result.value, 10)
        self.assertIsInstance(result, SLInteger)

    def test_slfloat_addition(self):
        """Test adding two SLFloat instances."""
        float_obj1 = SLFloat(3.5)
        float_obj2 = SLFloat(6.5)
        result = float_obj1 + float_obj2
        self.assertEqual(result.value, 10.0)
        self.assertIsInstance(result, SLFloat)

    def test_type_coercion_integer_float_addition(self):
        """Test adding SLInteger and SLFloat, which should return SLFloat."""
        int_obj = SLInteger(5)
        float_obj = SLFloat(2.5)
        result = int_obj + float_obj
        self.assertEqual(result.value, 7.5)
        self.assertIsInstance(result, SLFloat)

    def test_type_mismatch_error(self):
        """Test handling type mismatch during operations."""
        int_obj = SLInteger(5)
        str_obj = SLString("test")
        with self.assertRaises(TypeError):
            int_obj + str_obj

    def test_slarray_type_coercion(self):
        """Test that all elements in SLArray must have the same type."""
        array_obj = SLArray([SLInteger(1), SLInteger(2)])
        with self.assertRaises(TypeError):
            array_obj.append(SLFloat(3.0))

    def test_type_conversion_to_string(self):
        """Test converting an SLInteger or SLFloat to SLString."""
        int_obj = SLInteger(5)
        float_obj = SLFloat(5.5)
        str_obj_from_int = int_obj.to_slstring()
        str_obj_from_float = float_obj.to_slstring()
        self.assertIsInstance(str_obj_from_int, SLString)
        self.assertEqual(str_obj_from_int.value, "5")
        self.assertEqual(str_obj_from_float.value, "5.5")


if __name__ == '__main__':
    unittest.main()
