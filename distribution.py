import numpy as np

def generate_split(target_sum, min_value=10):
    # Estimate how many parts we should divide into, this is a rough estimate
    # You might need to adjust the `scale` parameter based on your needs
    parts_count = int(target_sum / (min_value + 3))
    if parts_count >= 2:
        # Generate numbers from an exponential distribution
        exponential_numbers = np.random.exponential(scale=(target_sum / parts_count) / 3, size = parts_count)

        # Scale the numbers so their sum equals to (target_sum - parts_count * min_value)
        # then add min_value to each part
        adjusted_parts = min_value + (exponential_numbers / sum(exponential_numbers)) * (target_sum - parts_count * min_value)

        # Ensure the total sum matches the target_sum through normalization
        final_parts = adjusted_parts * (target_sum / sum(adjusted_parts))
    
    else:
        final_parts = [target_sum]

    return round_and_adjust(final_parts)

def round_and_adjust(numbers):
    if len(numbers) > 1:
        # Step 1: Round numbers and calculate the initial sum
        rounded_numbers = [round(num) for num in numbers]
        target_sum = round(sum(numbers))
        current_sum = sum(rounded_numbers)
        
        # Step 2: Adjust the rounded numbers to reach the target sum
        differences = [num - round(num) for num in numbers]  # Calculate differences due to rounding
        while current_sum != target_sum:
            # Find the index to adjust based on whether we need to increase or decrease the sum
            if current_sum < target_sum:
                index = differences.index(max(differences))  # Index of max difference if sum is too low
                rounded_numbers[index] += 1  # Increment the rounded number
            else:
                index = differences.index(min(differences))  # Index of min difference if sum is too high
                rounded_numbers[index] -= 1  # Decrement the rounded number
            
            # Update the current sum and ensure the adjusted number won't be modified again
            current_sum = sum(rounded_numbers)
            differences[index] = 0  # Set the difference to zero to avoid adjusting the same number again
    else:
        rounded_numbers = [int(num) for num in numbers]
    
    return rounded_numbers