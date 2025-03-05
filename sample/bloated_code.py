"""
Sample bloated code for demonstration purposes.
This code performs a simple task but includes unnecessary operations and variables.
"""

import time
import random
import math
import string
import sys
import os

def process_data(data_input):
    """
    Process input data and return a result.
    
    This function is intentionally bloated with unnecessary operations.
    """
    # Unnecessary variable assignments
    start_time = time.time()
    unused_var1 = "This variable is never used"
    unused_var2 = 42
    unused_list = [1, 2, 3, 4, 5]
    
    # Create a copy of input data unnecessarily
    data_copy = data_input.copy()
    
    # Redundant operations
    result = 0
    for i in range(len(data_copy)):
        # Unnecessary temporary variables
        temp_value = data_copy[i]
        squared = temp_value * temp_value
        result += temp_value
        
        # Dead code that does nothing useful
        for j in range(5):
            dummy_value = j * j * j
            dummy_value = dummy_value / (j + 1) if j > 0 else 0
        
        # More unused operations
        random_value = random.random()
        if random_value > 0.5:
            # This branch never affects the result
            sin_value = math.sin(random_value)
            cos_value = math.cos(random_value)
    
    # Unnecessary string operations
    temp_str = "".join([c for c in "Hello, World!" if c not in "aeiou"])
    temp_str = temp_str.upper()
    
    # Compute average unnecessarily
    total = sum(data_input)
    count = len(data_input)
    average = total / count if count > 0 else 0
    
    # Compute end time (unused)
    end_time = time.time()
    elapsed = end_time - start_time
    
    # Redundant system information collection
    current_dir = os.getcwd()
    python_version = sys.version
    platform_name = sys.platform
    
    # Return the result (which is just the sum of input values)
    return result

def filter_data(data_input, threshold=50):
    """
    Filter data based on a threshold.
    
    This function contains redundant and inefficient operations.
    """
    # Unnecessary conversion to list
    data_list = list(data_input)
    
    # Inefficient filtering with multiple iterations
    filtered_data = []
    for item in data_list:
        # Unnecessary variable
        item_value = item
        
        # Redundant check
        is_above_threshold = item_value > threshold
        if is_above_threshold:
            # Multiple unnecessary steps
            temp_value = item_value * 2
            temp_value = temp_value / 2
            filtered_data.append(temp_value)
        else:
            # This does nothing useful
            dummy_value = item_value + 100
            dummy_value = dummy_value - 100
    
    # Additional unnecessary processing
    result = []
    for item in filtered_data:
        result.append(item)
    
    # Generate random string (unused)
    random_str = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    
    return result

def calculate_statistics(data_input):
    """
    Calculate statistics for a list of numbers.
    
    This function includes unnecessary calculations and variables.
    """
    # Return empty results for empty input
    if not data_input:
        return {
            'count': 0,
            'sum': 0,
            'mean': 0,
            'median': 0,
            'min': 0,
            'max': 0
        }
    
    # Count elements (unnecessarily complex)
    counter = 0
    for _ in data_input:
        counter += 1
    
    # Calculate sum (inefficiently)
    total = 0
    for item in data_input:
        total = total + item
    
    # Calculate mean
    mean = total / counter if counter > 0 else 0
    
    # Sort data (inefficiently)
    sorted_data = data_input.copy()
    for i in range(len(sorted_data)):
        for j in range(i + 1, len(sorted_data)):
            if sorted_data[i] > sorted_data[j]:
                # Swap elements
                temp = sorted_data[i]
                sorted_data[i] = sorted_data[j]
                sorted_data[j] = temp
    
    # Calculate median
    if counter % 2 == 0:
        # Even number of elements
        middle1 = sorted_data[counter // 2 - 1]
        middle2 = sorted_data[counter // 2]
        median = (middle1 + middle2) / 2
    else:
        # Odd number of elements
        median = sorted_data[counter // 2]
    
    # Find min and max (inefficiently)
    min_value = sorted_data[0]
    max_value = sorted_data[-1]
    
    # Unnecessary calculations of standard deviation
    variance_sum = 0
    for item in data_input:
        deviation = item - mean
        squared_deviation = deviation * deviation
        variance_sum += squared_deviation
    
    variance = variance_sum / counter if counter > 0 else 0
    std_dev = math.sqrt(variance)
    
    # Unnecessary histogram calculation
    histogram = {}
    for item in data_input:
        bin_key = item // 10 * 10
        if bin_key in histogram:
            histogram[bin_key] += 1
        else:
            histogram[bin_key] = 1
    
    # Return only the essential statistics despite calculating more
    return {
        'count': counter,
        'sum': total,
        'mean': mean,
        'median': median,
        'min': min_value,
        'max': max_value
    }

if __name__ == "__main__":
    # Example usage
    sample_data = [23, 45, 67, 89, 12, 34, 56, 78, 90]
    processed = process_data(sample_data)
    filtered = filter_data(sample_data, 40)
    stats = calculate_statistics(sample_data)
    
    print(f"Processed data: {processed}")
    print(f"Filtered data: {filtered}")
    print(f"Statistics: {stats}")