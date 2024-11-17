import re

def read_file(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.readlines()
        
def write_to_file(data, path):
    with open(path, 'w', encoding='utf-8') as file:
        for avg in data:
            file.write(f"{avg}\n")
        file.write("\n")
        file.write(f"{max(averages)}\n")
        file.write(f"{min(averages)}")

def calculate_average_of_negatives(numbers):
    negatives = [num for num in numbers if num < 0]
    if negatives:
        return sum(negatives) / len(negatives)
    return 0  # Если нет отрицательных чисел, возвращаем None

def get_averages(txt):
    averages = []
    for line in txt:
        numbers = list(map(float, line.split()))
        average = calculate_average_of_negatives(numbers)
        averages.append(average)
    return averages
    
    
if __name__ == '__main__':
    txt = read_file("./data/second_task.txt")
    averages = get_averages(txt)
    write_to_file(averages, './2_res_18.txt')
    