import re

def read_file(path):
    with open(path, 'r', encoding="utf-8") as file:
        return file.readlines()
        
def write_to_file(data, path):
    with open(path, 'w', encoding='utf-8') as file:
        if isinstance(data, list):
            for key, val in data:
                file.write(f"{key}:{val}\n")
        else:
            file.write(str(data))

def txt_to_words(lines):
    words = []
    
    for line in lines:
        _line = (line
                .replace("'", "")
                .replace("?", "")
                .replace("!", "")
                .replace(".", "")
                .replace("-", " ")
                .replace(",", " ")
                .lower().strip())
        words += _line.split(" ")
    return words
    
def get_avg_cnt(lines):
    word_counts = []
    for line in lines:
        sentences = re.split(r'[.!?]', line.strip())
        for sentence in sentences:
            cleaned_sentence = re.sub(r'[,]', '', sentence.strip())
            if cleaned_sentence.strip():
                word_count = len(cleaned_sentence.split())
                word_counts.append(word_count)

    return sum(word_counts) / len(word_counts)

def calc_freq(words):
    word_freq = {}
    for word in words:
        if len(word) == 0:
            continue
        if word in word_freq:
            word_freq[word] += 1
        else:
            word_freq[word] = 1
    
    return sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
if __name__ == '__main__':
    txt = read_file("./data/first_task.txt")
    
    words = txt_to_words(txt)
    word_freq = calc_freq(words)
    write_to_file(word_freq, "./1_res.txt")
    
    avg_cnt = get_avg_cnt(txt)
    write_to_file(avg_cnt, './1_res_18.txt')
    