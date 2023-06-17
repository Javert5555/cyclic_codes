from copy import deepcopy
from numpy.polynomial import Polynomial
from random import randint
from math import ceil

import tkinter as tk
# from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext

# получить последовательность из дважды вложенного массива
def create_sequence_from_double_nested_array(double_nested_array):
    return ''.join([''.join([str(char) for char in nested_array]) for nested_array in deepcopy(double_nested_array)])

# сделать вектор необходимой длины, просто добавляем 0 в конец списка,
# пока список не станет необходимой длины
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

# получаем кол-во ненулевых элементов (единиц) в векторе
def get_wt(vector):
    return sum(vector)

# получаем синдром из вектора (кодового слова)
def get_syndrome_from_vector(code_word, gen_polynom, n):
    # синдром - остаток от деления кодового слова на порождающий полином
    syndrome = list(Polynomial(code_word) % Polynomial(gen_polynom))

    # делаем полученный вектор биноминальным
    syndrome = get_binom_vector(syndrome)

    # делаем вектор необходимой длины, путём добавления в конец нулей
    syndrome = make_vector_need_len(syndrome, n)

    return syndrome

# получаем длину кодовых слов (m + k - сумма макс степени порожд полинома и длины инф слов)
def get_n(g, len_of_inf_word):
    gen_polynom = deepcopy(list(g))
    m = 0
    # ищем индекс первого ненулевого элемента массива, начиная с конца
    for i in range(len(g)-1,0,-1):
        if gen_polynom[i] == 1:
            m = i
            break
    return m + len_of_inf_word

# def get_inf_words(text, len_of_inf_word):


# получаем информационные слова заданной длины из переданного текста
def get_inf_words(text, len_of_inf_word, need_len_to_make_char_from_inf_word):
    inf_words = [bin(ord(char))[2:] for char in list(text)] # преобразуем текст в массив по типу: ['110001', '110010', '110011', '1010']
    for i in range(len(inf_words)):
        inf_words[i] = list(inf_words[i]) # преобразуем каждый элемент массива в список: '110001' -> ['1', '1', '0', '0', '0', '1']
        inf_words[i] = [int(num) for num in inf_words[i]] # преобразуем каждый элемент массива в список чисел: [1, 1, 0, 0, 0, 1]
        inf_words[i].reverse() # разворачиваем каждый элемент массива: [1, 1, 0, 0, 0, 1] -> [1, 0, 0, 0, 1, 1]

        # делаем каждый элемент массива необходимой длины: [1, 0, 0, 0, 1, 1] -> [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
        inf_words[i] = make_vector_need_len(inf_words[i], need_len_to_make_char_from_inf_word)

        # преобразуем каждый элемент массива в строку: [1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0] -> 110001000000
        inf_words[i] = ''.join([str(num) for num in inf_words[i]])
    
    # преобразовать весь массив инф слов в одну последовательность цифр
    inf_words = [int(char) for char in list(''.join(inf_words))]

    # считаем количество информационных слов необходимой длины, а именно 7
    count_of_inf_word_need_len = ceil(len(inf_words) // len_of_inf_word) + 1

    # добавляем в конец последовательности необходимое число нули, чтобы потом разделить эту последователность на
    # информационные слова одинаковой длины
    inf_words = make_vector_need_len(inf_words, len_of_inf_word * count_of_inf_word_need_len)
    inf_words_need_len = []

    # делим эту последователность на информационные слова одинаковой длины
    for j in range(count_of_inf_word_need_len): inf_words_need_len.append(inf_words[j*len_of_inf_word:(j+1)*len_of_inf_word])
    
    return inf_words_need_len

# получаем кодовое слово из информационного слова
def get_code_words(inf_words, gen_polynom, n):
    code_words = []
    for inf_word in inf_words:
        # получаем кодовое слово из информационного слова путём произведения
        # информационного слова на порождающий полином
        code_word = list(Polynomial(inf_word) * Polynomial(gen_polynom))

        # делаем полученный вектор биноминальным
        code_word = get_binom_vector(code_word)

        # делаем вектор необходимой длины, путём добавления в конец нулей
        code_word = make_vector_need_len(code_word, n)
        code_words.append(code_word)
    return code_words

# делаем произвольное число ошибок (от 0 до num_of_errors) ошибок в векторе
def make_mistake_in_vector(vector, num_of_errors):
    vector_copy = deepcopy(vector)
    # # Если хотим чтобы ошибки не накладывались друг на друга - раскоментировать нижнее
    num_memory = []
    # #
    for i in range(randint(0,num_of_errors)):
        # получаем случайный индекс, где необходимо допустить ошибку
        num = randint(0, len(vector_copy) - 1)
        # # Если хотим чтобы ошибки не накладывались друг на друга - раскоментировать нижнее
        # если уже был использован, генерируем другой
        while num in num_memory:
            num = randint(0, len(vector_copy) - 1)
        num_memory.append(num)
        
        # меняем значение бита на противоположное значение
        if (vector_copy[num] == 0):
            vector_copy[num] = 1
        else:
            vector_copy[num] = 0
    return vector_copy

# делаем произвольное число ошибок (от 0 до num_of_errors) ошибок во всех векторах
def make_mistake_in_vectors(vectors, num_of_errors):
    vectors_copy = deepcopy(vectors)
    for i in range(len(vectors)):
        vectors_copy[i] = make_mistake_in_vector(vectors_copy[i], num_of_errors)
    return vectors_copy

# исправляем ошибки в кодовых словах
def correct_mistake_in_code_word(code_word_with_mistakes, gen_polynom, n, t):
    # вычисляем синдром
    initial_syndrome = get_syndrome_from_vector(code_word_with_mistakes, gen_polynom, n)
    # print('initial_syndrome: ', initial_syndrome)

    initial_code_word = []
    error_vector = []

    # если в кодовом слове нет ошибки, возвращаем полученное кодовое слово
    if (sum(initial_syndrome) == 0):
        initial_code_word = code_word_with_mistakes
        # print('1) initial_code_word: ', initial_code_word)

    # если в синдроме число ненулевых элементов (единиц) находится в пределе от 0 до t,
    # где t - число гарантированно исправляемых ошибок кодом,
    # то считаем данный синдром вектором e(x)
    # и возвращаем v(x)-e(x)
    elif (get_wt(initial_syndrome) <= t):
        error_vector = initial_syndrome
        initial_code_word = get_binom_vector([int(num) for num in list(Polynomial(code_word_with_mistakes) - Polynomial(error_vector))])
        initial_code_word = make_vector_need_len(initial_code_word, n)
        # print('2) initial_code_word: ', initial_code_word)

    # если в синдроме число ненулевых элементов (единиц) больше t
    else:
        for i in range(1,n):
            # вычисляем "текущий" синдром по следующей формуле: x*s(i-1) mod(g)
            current_syndrome = get_binom_vector(list((Polynomial([0, 1]) * Polynomial(initial_syndrome)) % Polynomial(gen_polynom)))
            # print('initial_syndrome: ', initial_syndrome)
            # print('current_syndrome: ', current_syndrome)
            initial_syndrome = current_syndrome
            # если в полученном синдроме число ненулевых элементов (единиц) находится в пределе от 0 до t,
            # то находим вектор ошибок по формуле: x^(n-i) * s(i) mod(x^n + 1)
            if (get_wt(current_syndrome) <= t):
                # print(n)
                # print(list(Polynomial(get_vector_from_power(n)) + 1))
                # print(list((Polynomial(get_vector_from_power(n-i)) * Polynomial(current_syndrome))))
                error_vector1 = list((Polynomial(get_vector_from_power(n-i)) * Polynomial(current_syndrome)) % (Polynomial(get_vector_from_power(n)) + 1))
                error_vector1 = get_binom_vector(error_vector1)
                # print('error_vector1: ', error_vector1)
                initial_code_word = get_binom_vector(list(Polynomial(code_word_with_mistakes) - Polynomial(error_vector1)))
                initial_code_word = make_vector_need_len(initial_code_word, n)
                # initial_syndrome = current_syndrome

                # print('3) initial_code_word: ', initial_code_word)
                break
            else:
                initial_syndrome = current_syndrome
    return initial_code_word

# исправляем ошибки во всех векторах
def correct_mistake_in_code_words(code_words_with_mistakes, gen_polynom, n, t):
    correct_code_words = []
    for code_word_with_mistake in code_words_with_mistakes:
        correct_code_words.append(correct_mistake_in_code_word(code_word_with_mistake, gen_polynom, n, t))
    return correct_code_words


# получаем информационное слово из кодового путём целочисленного деления кодового слова на порождающий полином
def get_inf_word_from_code_word(code_word, gen_polynom, len_of_inf_word):
    inf_word = list(Polynomial(code_word) // Polynomial(gen_polynom))
    inf_word = get_binom_vector(inf_word)
    inf_word = make_vector_need_len(inf_word, len_of_inf_word)
    return inf_word

# получаем информационные слова из кодовых слов
def get_inf_words_from_code_words(code_words, gen_polynom, len_of_inf_word):
    decoded_inf_words = []
    for code_word in code_words:
        decoded_inf_words.append(get_inf_word_from_code_word(code_word, gen_polynom, len_of_inf_word))
    return decoded_inf_words

# получаем символы (буквы) из информационных слов
def make_char_from_inf_words(inf_words, need_len_to_make_char_from_inf_word):
    decoded_text = ''
    text = deepcopy(inf_words)
    # преобразовываем информационные слова в последовательность информационных слов
    for i in range(len(text)):
        text[i] = ''.join([str(char) for char in text[i]])
    text = ''.join(text)

    # получаем символ из каждого куска последовательности информационных слов
    # и добавляем данный символ к переменной decoded_text
    for j in range(len(text)//need_len_to_make_char_from_inf_word):
        # decoded_text += chr(int('0b' + ''.join(reversed(list(text[j*need_len_to_make_char_from_inf_word:(j+1)*need_len_to_make_char_from_inf_word]))), 2))
        decoded_text += chr(int('0b' + ''.join(reversed(list(text[j*need_len_to_make_char_from_inf_word:(j+1)*need_len_to_make_char_from_inf_word]))), 2))
    return decoded_text

def get_solution(text, num_of_errors):
    # 1 + x + x^2 + x^5 + x^6 + x^9
    g = [1, 0, 0, 0, 1, 0, 1, 1, 1]

    len_of_inf_word = 7
    need_len_to_make_char_from_inf_word = 12
    # t - количесвто исправляемых ошибок
    t = 2
    # n - длина кодовых слов и синдромов
    n = get_n(g, len_of_inf_word)

    inf_words = get_inf_words(text, len_of_inf_word, need_len_to_make_char_from_inf_word)

    code_words = get_code_words(inf_words, g, n)

    code_words_with_mistakes = make_mistake_in_vectors(code_words, num_of_errors)

    correct_code_words = correct_mistake_in_code_words(code_words_with_mistakes, g, n, t)

    decoded_inf_words = get_inf_words_from_code_words(correct_code_words, g, len_of_inf_word)

    decoded_text = make_char_from_inf_words(decoded_inf_words, need_len_to_make_char_from_inf_word)

    return {
        'initial_text': text,
        'decoded_text': decoded_text,
        'inf_words': create_sequence_from_double_nested_array(inf_words),
        'decoded_inf_words': create_sequence_from_double_nested_array(decoded_inf_words),
        'code_words': create_sequence_from_double_nested_array(code_words),
        'code_words_with_mistakes': create_sequence_from_double_nested_array(code_words_with_mistakes),
        'correct_code_words': create_sequence_from_double_nested_array(correct_code_words)
    }

class SecondWindow(tk.Toplevel):
    def __init__(self, master=None, result=None):
        super().__init__(master)
        self.title('Циклические коды, окно вывода данных')
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

        self.text_decoded_inf_words = scrolledtext.ScrolledText(self.f_right, wrap=tk.WORD, height=7)
        self.text_decoded_inf_words.pack(side='top')
        self.text_decoded_inf_words.insert(tk.END, result['decoded_inf_words'])
        
        self.label6 = tk.Label(self.f_right, text=result['title6'])
        self.label6.pack(side='top')
        self.label6.pack(pady=10)

        self.initial_text = scrolledtext.ScrolledText(self.f_right, wrap=tk.WORD, height=7)
        self.initial_text.pack(side='top')
        self.initial_text.insert(tk.END, result['initial_text'])
        
        self.label7 = tk.Label(self.f_right, text=result['title7'])
        self.label7.pack(side='top')
        self.label7.pack(pady=10)

        self.decoded_text = scrolledtext.ScrolledText(self.f_right, wrap=tk.WORD, height=7)
        self.decoded_text.pack(side='top')
        self.decoded_text.insert(tk.END, result['decoded_text'])



class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('600x540')
        self.minsize(600, 540)
        self.title('Циклические коды, окно ввода данных')

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

        # self.initial_text = tk.Text(self.f_top, height=20, width=55)
        # self.initial_text.pack(side='top')
        # self.initial_text.pack(pady=(10, 0))

        self.initial_text = scrolledtext.ScrolledText(self.f_top, wrap=tk.WORD, height=20, width=55)
        self.initial_text.pack(side='top')
        self.initial_text.pack(pady=(10, 0))

        self.label_gen_pol = tk.Label(self.f_top, text='Порождающий полином: g(x)=1+x^4+x^6+x^7+x^8')
        self.label_gen_pol.pack(side='top')
        self.label_gen_pol.pack(pady=(10, 0))

        self.len_params = tk.Label(self.f_top, text='Длина кодовых слов: 15. Длина информационных слов: 7.')
        self.len_params.pack(side='top')
        self.len_params.pack(pady=(10, 0))

        self.num_fixed_error = tk.Label(self.f_top, text='Количество гарантированно исправляемых ошибок: 2')
        self.num_fixed_error.pack(side='top')
        self.num_fixed_error.pack(pady=(10, 0))

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
            self.initial_text_var = self.initial_text.get("1.0","end")
            if (self.initial_text_var.strip() == ''):
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
            'decoded_inf_words': self.result['decoded_inf_words'],
            'title6': 'Начальный текст:',
            'initial_text': self.result['initial_text'],
            'title7': 'Текст после кодирования/декодирования:',
            'decoded_text': self.result['decoded_text'],
        })

if __name__ == "__main__":
    main = Main()
    main.mainloop()