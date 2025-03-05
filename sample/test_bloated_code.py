"""
Test file for the bloated_code.py module.
"""

import unittest
import pytest
from bloated_code import process_data, filter_data, calculate_statistics

class TestBloatedCode(unittest.TestCase):
    """Test cases for the bloated code module."""
    
    def test_process_data(self):
        """Test the process_data function."""
        # Test with a simple list
        data = [1, 2, 3, 4, 5]
        result = process_data(data)
        self.assertEqual(result, sum(data))
        
        # Test with an empty list
        empty_data = []
        result = process_data(empty_data)
        self.assertEqual(result, 0)
        
        # Test with negative numbers
        negative_data = [-1, -2, -3, -4, -5]
        result = process_data(negative_data)
        self.assertEqual(result, sum(negative_data))
    
    def test_filter_data(self):
        """Test the filter_data function."""
        # Test with values above and below threshold
        data = [30, 40, 50, 60, 70]
        result = filter_data(data, 50)
        self.assertEqual(result, [60, 70])
        
        # Test with custom threshold
        result = filter_data(data, 30)
        self.assertEqual(result, [40, 50, 60, 70])
        
        # Test with empty list
        empty_data = []
        result = filter_data(empty_data)
        self.assertEqual(result, [])
        
        # Test with all values below threshold
        low_data = [10, 20, 30, 40]
        result = filter_data(low_data, 50)
        self.assertEqual(result, [])
    
    def test_calculate_statistics(self):
        """Test the calculate_statistics function."""
        # Test with a simple list
        data = [10, 20, 30, 40, 50]
        result = calculate_statistics(data)
        
        self.assertEqual(result['count'], 5)
        self.assertEqual(result['sum'], 150)
        self.assertEqual(result['mean'], 30)
        self.assertEqual(result['median'], 30)
        self.assertEqual(result['min'], 10)
        self.assertEqual(result['max'], 50)
        
        # Test with an empty list
        empty_data = []
        result = calculate_statistics(empty_data)
        
        self.assertEqual(result['count'], 0)
        self.assertEqual(result['sum'], 0)
        self.assertEqual(result['mean'], 0)
        self.assertEqual(result['median'], 0)
        self.assertEqual(result['min'], 0)
        self.assertEqual(result['max'], 0)
        
        # Test with even number of elements (for median calculation)
        even_data = [10, 20, 30, 40]
        result = calculate_statistics(even_data)
        
        self.assertEqual(result['median'], 25)  # (20 + 30) / 2

# Pytest-style tests for the same functions
@pytest.mark.parametrize("input_data,expected_sum", [
    ([1, 2, 3, 4, 5], 15),
    ([], 0),
    ([-1, -2, -3, -4, -5], -15),
    ([100, 200, 300], 600)
])
def test_process_data_parametrized(input_data, expected_sum):
    """Test process_data with parametrized inputs."""
    result = process_data(input_data)
    assert result == expected_sum

@pytest.mark.parametrize("input_data,threshold,expected_result", [
    ([30, 40, 50, 60, 70], 50, [60, 70]),
    ([30, 40, 50, 60, 70], 30, [40, 50, 60, 70]),
    ([], 50, []),
    ([10, 20, 30, 40], 50, [])
])
def test_filter_data_parametrized(input_data, threshold, expected_result):
    """Test filter_data with parametrized inputs."""
    result = filter_data(input_data, threshold)
    assert result == expected_result

def test_calculate_statistics_with_simple_data():
    """Test calculate_statistics with a simple dataset."""
    data = [10, 20, 30, 40, 50]
    result = calculate_statistics(data)
    
    assert result['count'] == 5
    assert result['sum'] == 150
    assert result['mean'] == 30
    assert result['median'] == 30
    assert result['min'] == 10
    assert result['max'] == 50

def test_calculate_statistics_with_empty_data():
    """Test calculate_statistics with an empty dataset."""
    data = []
    result = calculate_statistics(data)
    
    assert result['count'] == 0
    assert result['sum'] == 0
    assert result['mean'] == 0
    assert result['median'] == 0
    assert result['min'] == 0
    assert result['max'] == 0

if __name__ == '__main__':
    unittest.main()