import numpy as np
from copy import deepcopy
from numpy.polynomial import Polynomial
from random import randint
from math import ceil

import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog as fd
import tkinter.scrolledtext as scrolledtext

# получить последовательность из дважды вложенного массива
def create_sequence_from_double_nested_array(double_nested_array):
    return ''.join([''.join([str(char) for char in nested_array]) for nested_array in deepcopy(double_nested_array)])

# сделать вектор необходимой длины
def make_vector_need_len(vector, vector_length):
    vector_copy = deepcopy(vector)
    while len(vector_copy) < vector_length:
        vector_copy.append(0)
    return vector_copy

# делаем вектор биноминальным (состоящим только из 0 и 1)
def get_binom_vector(vector):
    vector_copy = deepcopy(vector)
    for i in range(len(vector_copy)):
        if vector_copy[i] % 2 == 0:
            vector_copy[i] = 0
        else:
            vector_copy[i] = 1
    return vector_copy

# получаем вектор с элементом заданной степени
def get_vector_from_power(power):
    vector = [0]*(power+1)
    vector[power] = 1
    return vector

# получаем кол-во ненулевых элементов в векторе
def get_wt(vector):
    return sum(vector)

# получаем синдром из вектора (кодового слова)
def get_syndrome_from_vector(code_word, gen_polynom, n):
    syndrome = list(Polynomial(code_word) % Polynomial(gen_polynom))
    for i in range(len(syndrome)):
        if syndrome[i] % 2 == 0:
            syndrome[i] = 0
        else:
            syndrome[i] = 1
    while len(syndrome) < n:
        syndrome.append(0)
    return syndrome

# получаем длину кодовых слов (m + k - сумма макс степени порожд полинома и длины инф слов)
def get_n(g, len_of_inf_word):
    gen_polynom = deepcopy(list(g))
    m = 0
    for i in range(len(g),0,-1):
        if gen_polynom[i-1] == 1:
            m = i-1
            break
    return m + len_of_inf_word

# def get_inf_words(text, len_of_inf_word):


# получаем информационные слова заданной длины из переданного текста
def get_inf_words(text, len_of_inf_word, need_len_to_make_char_from_inf_word):
    inf_words = [bin(ord(char))[2:] for char in list(text)]
    for i in range(len(inf_words)):
        inf_words[i] = list(inf_words[i])
        inf_words[i] = [int(num) for num in inf_words[i]]
        inf_words[i].reverse()
        inf_words[i] = make_vector_need_len(inf_words[i], need_len_to_make_char_from_inf_word)
        inf_words[i] = ''.join([str(num) for num in inf_words[i]])
    inf_words = [int(char) for char in list(''.join(inf_words))]
    count_of_inf_word_need_len = ceil(len(inf_words) // len_of_inf_word) + 1
    inf_words = make_vector_need_len(inf_words, len_of_inf_word * count_of_inf_word_need_len)
    inf_words_need_len = []
    for j in range(count_of_inf_word_need_len):
        inf_words_need_len.append(inf_words[j*len_of_inf_word:(j+1)*len_of_inf_word])
    
    # print(len_of_inf_word * ceil(len(inf_words) // len_of_inf_word))
    # print(len(inf_words))
    # print(inf_words_need_len)
    return inf_words_need_len

# получаем кодовое слово из информационного слова
def get_code_words(inf_words, gen_polynom, n):
    code_words = []
    for inf_word in inf_words:
        # print(inf_word)
        # print(gen_polynom)
        code_word = list(Polynomial(inf_word) * Polynomial(gen_polynom))
        for i in range(len(code_word)):
            if code_word[i] % 2 == 0:
                code_word[i] = 0
            else:
                code_word[i] = 1
        while len(code_word) < n:
            code_word.append(0)
        code_words.append(code_word)
    return code_words

# делаем произвольное число ошибок (от 0 до num_of_errors) ошибок в векторе
def make_mistake_in_vector(vector, num_of_errors):
    vector_copy = deepcopy(vector)
    # # Если хотим чтобы ошибки не накладывались друг на друга - раскоментировать нижнее
    num_memory = []
    # #
    # print(vector_copy)
    for i in range(randint(0,num_of_errors)):
        num = randint(0, len(vector_copy) - 1)
        # # Если хотим чтобы ошибки не накладывались друг на друга - раскоментировать нижнее
        while num in num_memory:
            num = randint(0, len(vector_copy) - 1)
        num_memory.append(num)
        # # 
        if (vector_copy[num] == 0):
            vector_copy[num] = 1
        else:
            vector_copy[num] = 0
    # print(vector_copy)
    # print('#####################')
    return vector_copy

# делаем произвольное число ошибок (от 0 до num_of_errors) ошибок во всех векторах
def make_mistake_in_vectors(vectors, num_of_errors):
    vectors_copy = deepcopy(vectors)
    for i in range(len(vectors)):
        vectors_copy[i] = make_mistake_in_vector(vectors_copy[i], num_of_errors)
    return vectors_copy

# исправляем ошибки в кодовых словах
def correct_mistake_in_code_word(code_word_with_mistakes, gen_polynom, n, t):
    initial_syndrome = get_syndrome_from_vector(code_word_with_mistakes, gen_polynom, n)
    # print('initial_syndrome: ', initial_syndrome)

    initial_code_word = []
    error_vector = []

    # если в кодовом слове нет ошибки
    if (sum(initial_syndrome) == 0):
        initial_code_word = code_word_with_mistakes
        # print('1) initial_code_word: ', initial_code_word)
 
    elif (get_wt(initial_syndrome) <= t):
        error_vector = initial_syndrome
        initial_code_word = get_binom_vector([int(num) for num in list(Polynomial(code_word_with_mistakes) - Polynomial(error_vector))])
        initial_code_word = make_vector_need_len(initial_code_word, n)
        # print('2) initial_code_word: ', initial_code_word)

    else:
        for i in range(1,n):
            current_syndrome = get_binom_vector(list((Polynomial([0, 1]) * Polynomial(initial_syndrome)) % Polynomial(gen_polynom)))
            # print('initial_syndrome: ', initial_syndrome)
            # print('current_syndrome: ', current_syndrome)
            initial_syndrome = current_syndrome
            # while len(current_syndrome) < n:
            #     current_syndrome.append(0)
            if (get_wt(current_syndrome) <= t):
                # print(n)
                # print(list(Polynomial(get_vector_from_power(n)) + 1))
                # print(list((Polynomial(get_vector_from_power(n-i)) * Polynomial(current_syndrome))))
                error_vector1 = list((Polynomial(get_vector_from_power(n-i)) * Polynomial(current_syndrome)) % (Polynomial(get_vector_from_power(n)) + 1))
                error_vector1 = get_binom_vector(error_vector1)
                # print('error_vector1: ', error_vector1)
                # while len(error_vector) < n:
                #     error_vector.append(0)
                initial_code_word = get_binom_vector(list(Polynomial(code_word_with_mistakes) - Polynomial(error_vector1)))
                initial_code_word = make_vector_need_len(initial_code_word, n)
                # print('cd_wd: ', initial_code_word)
                initial_syndrome = current_syndrome

                break
                # break
            else:
                initial_syndrome = current_syndrome
    return initial_code_word

def correct_mistake_in_code_words(code_words_with_mistakes, gen_polynom, n, t):
    correct_code_words = []
    for code_word_with_mistake in code_words_with_mistakes:
        correct_code_words.append(correct_mistake_in_code_word(code_word_with_mistake, gen_polynom, n, t))
    return correct_code_words


# получаем информационное слово из кодового 
def get_inf_word_from_code_word(code_word, gen_polynom, len_of_inf_word):
    inf_word = list(Polynomial(code_word) // Polynomial(gen_polynom))
    for i in range(len(inf_word)):
        if inf_word[i] % 2 == 0:
            inf_word[i] = 0
        else:
            inf_word[i] = 1
    inf_word = make_vector_need_len(inf_word, len_of_inf_word)
    return inf_word

# получаем информационные слова из кодовых слов
def get_inf_words_from_code_words(code_words, gen_polynom, len_of_inf_word):
    decode_inf_words = []
    for code_word in code_words:
        decode_inf_words.append(get_inf_word_from_code_word(code_word, gen_polynom, len_of_inf_word))
    return decode_inf_words

# получить букву из информационного слова
def make_char_from_inf_word(inf_word):
    return chr(int('0b' + ''.join([str(num) for num in reversed(deepcopy(inf_word))]), 2))

def make_char_from_inf_word(inf_words, need_len_to_make_char_from_inf_word):
    decode_text = ''
    text = deepcopy(inf_words)
    for i in range(len(text)):
        text[i] = ''.join([str(char) for char in text[i]])
    text = ''.join(text)
    for j in range(len(text)//need_len_to_make_char_from_inf_word):
        decode_text += chr(int('0b' + ''.join(reversed(list(text[j*need_len_to_make_char_from_inf_word:(j+1)*need_len_to_make_char_from_inf_word]))), 2))
    return decode_text

def get_solution(text, num_of_errors):
    # 1 + x + x^2 + x^5 + x^6 + x^9
    g = [1, 0, 0, 0, 1, 0, 1, 1, 1]
    # g = [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
    # h = [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1]
    # g = [1,0,0,0,1,0,1,1,1]
    # g = [1, 1, 1, 0, 0, 1, 1, 0, 0, 1]
    len_of_inf_word = 7
    need_len_to_make_char_from_inf_word = 12
    # t - количесвто исправляемых ошибок
    t = 2
    # n - длина кодовых слов и синдромов
    n = get_n(g, len_of_inf_word)
    # print('n: ', n)

    # text = 'й111111111йййййцукенгшщзхъ\фывапролджэячсмитьбю.qwertyuiop[]]]]]\asdfghjkl;zxcvbnm,./|'

    inf_words = get_inf_words(text, len_of_inf_word, need_len_to_make_char_from_inf_word)
    # print('inf_words: ', inf_words)

    code_words = get_code_words(inf_words, g, n)
    # print('code_words', code_words)



    #####################
    # code_word = [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
    # code_word = code_words[0]
    # code_word_with_one_mistake = make_mistake_in_vector(code_words[0], 0) # code_word_with_one_mistake
    # code_word_with_one_mistake = [1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0] # code_word_with_one_mistake
    # code_word_with_two_mistake = [1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0] # code_word_with_two_mistake
    # code_word_with_two_mistake = [1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0] # code_word_with_two_mistake

    code_words_with_mistakes = make_mistake_in_vectors(code_words, num_of_errors)
    # print('code_words_with_mistakes: ', code_words_with_mistakes)

    correct_code_words = correct_mistake_in_code_words(code_words_with_mistakes, g, n, t)

    decode_inf_words = get_inf_words_from_code_words(correct_code_words, g, len_of_inf_word)
    # print('code_words:', code_words)
    # print('correct_code_words:', correct_code_words)
    # print('inf_words:', inf_words)
    # print('decode_inf_words:', decode_inf_words)

    decode_text = make_char_from_inf_word(decode_inf_words, need_len_to_make_char_from_inf_word)
    # print(text)
    # print(decode_text)

    # print(decode_text == text)

    return {
        'initial_text': text,
        'decode_text': decode_text,
        'inf_words': create_sequence_from_double_nested_array(inf_words),
        'decode_inf_words': create_sequence_from_double_nested_array(decode_inf_words),
        'code_words': create_sequence_from_double_nested_array(code_words),
        'code_words_with_mistakes': create_sequence_from_double_nested_array(code_words_with_mistakes),
        'correct_code_words': create_sequence_from_double_nested_array(correct_code_words)
    }

class SecondWindow(tk.Toplevel):
    def __init__(self, master=None, result=None):
        super().__init__(master)
        self.title("Second window")
        self.minsize(1320, 660)

        self.f_left = tk.Frame(self)
        self.f_left.pack(side='left')
        self.f_left.pack(padx=(10, 10))

        self.f_right = tk.Frame(self)
        self.f_right.pack(side='left')
        self.f_right.pack(padx=(10, 10))

        self.label1 = tk.Label(self.f_left, text=result['title1'])
        self.label1.pack(side='top')
        self.label1.pack(pady=10)

        self.text_code_words = scrolledtext.ScrolledText(self.f_left, wrap=tk.WORD, height=10)
        self.text_code_words.pack(side='top')
        self.text_code_words.insert(tk.END, result['code_words'])
        
        self.label2 = tk.Label(self.f_left, text=result['title2'])
        self.label2.pack(side='top')
        self.label2.pack(pady=10)

        self.text_code_words_with_mistakes = scrolledtext.ScrolledText(self.f_left, wrap=tk.WORD, height=10)
        self.text_code_words_with_mistakes.pack(side='top')
        self.text_code_words_with_mistakes.insert(tk.END, result['code_words_with_mistakes'])
        
        self.label3 = tk.Label(self.f_left, text=result['title3'])
        self.label3.pack(side='top')
        self.label3.pack(pady=10)

        self.text_correct_code_words = scrolledtext.ScrolledText(self.f_left, wrap=tk.WORD, height=10)
        self.text_correct_code_words.pack(side='top')
        self.text_correct_code_words.insert(tk.END, result['correct_code_words'])
        
        self.label4 = tk.Label(self.f_right, text=result['title4'])
        self.label4.pack(side='top')
        self.label4.pack(pady=10)

        self.text_inf_words = scrolledtext.ScrolledText(self.f_right, wrap=tk.WORD, height=7)
        self.text_inf_words.pack(side='top')
        self.text_inf_words.insert(tk.END, result['inf_words'])
        
        self.label5 = tk.Label(self.f_right, text=result['title5'])
        self.label5.pack(side='top')
        self.label5.pack(pady=10)

        self.text_decode_inf_words = scrolledtext.ScrolledText(self.f_right, wrap=tk.WORD, height=7)
        self.text_decode_inf_words.pack(side='top')
        self.text_decode_inf_words.insert(tk.END, result['decode_inf_words'])
        
        self.label6 = tk.Label(self.f_right, text=result['title6'])
        self.label6.pack(side='top')
        self.label6.pack(pady=10)

        self.initial_text = scrolledtext.ScrolledText(self.f_right, wrap=tk.WORD, height=7)
        self.initial_text.pack(side='top')
        self.initial_text.insert(tk.END, result['initial_text'])
        
        self.label7 = tk.Label(self.f_right, text=result['title7'])
        self.label7.pack(side='top')
        self.label7.pack(pady=10)

        self.decode_text = scrolledtext.ScrolledText(self.f_right, wrap=tk.WORD, height=7)
        self.decode_text.pack(side='top')
        self.decode_text.insert(tk.END, result['decode_text'])



class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x500')
        self.minsize(600, 500)
        self.title('Циклические коды')

        self.f_top = tk.Frame(self)
        self.f_top.pack()

        self.f_bottom = tk.Frame(self)
        self.f_bottom.pack(side='left')
        self.f_bottom.pack(padx=(20, 0))

        self.f_btn = tk.Frame(self)
        self.f_btn.pack(side='right')

        self.label_initial_text = tk.Label(self.f_top, text='Введите текст, который надо закодировать: ')
        self.label_initial_text.pack(side='top')
        self.label_initial_text.pack(pady=(10, 0))

        self.initial_text = tk.Text(self.f_top, height=20, width=55)
        self.initial_text.pack(side='top')
        self.initial_text.pack(pady=(10, 0))

        self.num_of_errors = tk.IntVar()

        self.label_num_of_errors_text = tk.Label(self.f_bottom, text='Укажите максимальное число ошибок в кодовых словах')
        self.label_num_of_errors_text.pack(side='top')
        # self.label_num_of_errors_text.pack(pady=(10, 0))

        self.checkbutton1 = tk.Checkbutton(self.f_bottom, text="0 Ошибок", variable=self.num_of_errors, onvalue=0)
        self.checkbutton1.pack(side='left')

        self.checkbutton2 = tk.Checkbutton(self.f_bottom, text="1 Ошибка", variable=self.num_of_errors, onvalue=1)
        self.checkbutton2.pack(side='left')

        self.checkbutton3 = tk.Checkbutton(self.f_bottom, text="2 Ошибки", variable=self.num_of_errors, onvalue=2)
        self.checkbutton3.pack(side='left')


        button_1 = tk.Button(self.f_btn, text='Получить результат', font='Times 12', command=self.get_all_inputs_and_get_solution)
        button_1.pack(side='bottom')
        button_1.pack(padx=(0, 20))

    def open_window(self, result):
        self.new_window = SecondWindow(self, result=result)
    
    def get_all_inputs_and_get_solution(self):
        try:
            self.initial_text_var = self.initial_text.get("1.0","end").strip()
            if (self.initial_text_var == ''):
                messagebox.showwarning(title="Предупреждение", message="Введите текст, который надо закодировать")
                return
        except:
            messagebox.showwarning(title="Предупреждение", message="Что-то пошло не так")
            return
        # print()
        # print()

        self.result = get_solution(self.initial_text_var, self.num_of_errors.get())

        self.open_window({
            'title1': 'Последовательность кодовых слов:',
            'code_words': self.result['code_words'],
            'title2': 'Последовательность кодовых слов с ошибками:',
            'code_words_with_mistakes': self.result['code_words_with_mistakes'],
            'title3': 'Последовательность кодовых слов с исправленными ошибками:',
            'correct_code_words': self.result['correct_code_words'],
            'title4': 'Последовательность информационных слов:',
            'inf_words': self.result['inf_words'],
            'title5': 'Последовательность информационных слов после декодирования:',
            'decode_inf_words': self.result['decode_inf_words'],
            'title6': 'Начальный текст:',
            'initial_text': self.result['initial_text'],
            'title7': 'Текст после кодирования/декодирования:',
            'decode_text': self.result['decode_text'],
        })
        # self.open_window({
        #     'input_title': 'Последовательность информационных слов до декодирования:',
        #     'input_text': self.result['inf_words'],
        #     'output_title': 'Последовательность информационных слов после декодирования:',
        #     'output_text': self.result['code_words_with_mistakes']
        # })

    # def get_all_inputs_and_get_solution(self):
    #     try:
    #         self.count_of_adders_var = int(self.count_of_adders.get("1.0","end").strip())
    #         if (self.count_of_adders_var < 2 or self.count_of_adders_var > 5):
    #             messagebox.showwarning(title="Предупреждение", message="Количество сумматоров должно быть больше 1 и меньше 5")
    #             return
    #     except:
    #         messagebox.showwarning(title="Предупреждение", message="Введите корректные значения количества сумматоров")
    #         return
        
    #     try:
    #         self.adders_var = [row.split(',') for row in self.adders.get("1.0","end").strip().split('\n')]
    #         if (self.count_of_adders_var != len(self.adders_var)):
    #             messagebox.showwarning(title="Предупреждение", message="Неверно указано количество сумматоров")
    #             return
    #         for i in range(len(self.adders_var)):
    #             if (len(self.adders_var[i]) < 2 or len(self.adders_var[i]) > 3):
    #                 messagebox.showwarning(title="Предупреждение", message="Количество регистров сумматора должно быть равно 2 или 3")
    #                 return
    #             for j in range(len(self.adders_var[i])):
    #                 self.adders_var[i][j] = int(self.adders_var[i][j])
    #                 if (self.adders_var[i][j] < 1 or self.adders_var[i][j] > 3):
    #                     messagebox.showwarning(title="Предупреждение", message="Номер регистра не может быть больше 3 или меньше 1")
    #                     return
    #     except:
    #         messagebox.showwarning(title="Предупреждение", message="Введите корректные значения номеров регистров сумматоров")
    #         return
        
    #     try:
    #         self.num_of_errors_var = int(self.num_of_errors.get("1.0","end").strip())
    #         if (self.num_of_errors_var < 0 or self.count_of_adders_var > 8):
    #             messagebox.showwarning(title="Предупреждение", message="Количество ошибок должно быть больше 0 и меньше 9")
    #             return
    #     except:
    #         messagebox.showwarning(title="Предупреждение", message="Указано некорректное число ошибок")
    #         return

    #     try:
    #         self.initial_text_var = self.initial_text.get("1.0","end").strip()
    #         if (self.initial_text_var == ''):
    #             messagebox.showwarning(title="Предупреждение", message="Введите текст, который надо закодировать")
    #             return
    #     except:
    #         messagebox.showwarning(title="Предупреждение", message="Что-то пошло не так")
    #         return
        
    #     result = get_solution({
    #         'count_of_adders': self.count_of_adders_var,
    #         'adders': self.adders_var,
    #         'num_of_errors': self.num_of_errors_var,
    #         'initial_text': self.initial_text_var
    #     })
    #     messagebox.showwarning(title="Закодированная последовательность", message=result['code_words'])
    #     messagebox.showwarning(title="Исходная последовательность", message=result['initial_text'])

if __name__ == "__main__":
    main = Main()
    main.mainloop()