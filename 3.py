def replace_na_with_average(numbers):
    for i in range(len(numbers)):
        if numbers[i] == 'N/A':
            left = right = None
            
            if i > 0 and numbers[i-1] != 'N/A':
                left = int(numbers[i-1])
            if i < len(numbers) - 1 and numbers[i+1] != 'N/A':
                right = int(numbers[i+1])
            
            neighbors = [n for n in [left, right] if n is not None]
            if neighbors:
                numbers[i] = sum(neighbors) / len(neighbors)
            else:
                numbers[i] = 0

    return list(map(int, numbers))

def filter_and_average(numbers):
    filtered_numbers = [num for num in numbers if num % 7 == 0]
    if filtered_numbers:
        return sum(filtered_numbers) / len(filtered_numbers)
    return 0

def get_averages(path):
    averages = []
    
    with open(input_file, 'r') as f:
        for line in f:
            numbers = line.strip().split()
            numbers = replace_na_with_average(numbers)
            average = filter_and_average(numbers)
            averages.append(average)
    return averages

def write_res(data, path):
    averages = []

    with open(output_file, 'w') as f:
        for avg in data:
            f.write(f"{avg}\n")
            
if __name__ == '__main__':
    input_file = './data/third_task.txt'
    output_file = './3_result_18.txt'
    averages = get_averages(input_file)
    write_res(averages, output_file)
