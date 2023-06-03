import numpy as np
from copy import deepcopy
from numpy.polynomial import Polynomial
from random import randint
from math import ceil


# print(np.polydiv([2,1,1,1], [1,1]))

# def get_code_word(inf_word, gen_polynom):
#     result = np.polymul(inf_word, gen_polynom)
#     for i in range(len(result)):
#         if result[i] % 2 == 0:
#             result[i] = 0
#         else:
#             result[i] = 1
#     return result

# def get_error_vectors(n):
#     error_vectors = []
#     # количество вектор ошибок равно количеству строк транспонированной проверочной матрицы
#     for i in range(n):
#         error_vector = []
#         for j in range(n):
#             error_vector.append(0)
#         error_vector[i] = 1
#         # т.к. единицы идут справа-налево по диагонали
#         # error_vector.reverse()
#         error_vectors.append(np.array(error_vector))
    
#     # вектора для декодирования двух ошибок, например:
#     # 110000
#     # 101000
#     # 100100
#     # ...
#     # error_vectors2 = []

#     # for i in range(len(error_vectors)):
#     #     for j in range(i+1, len(error_vectors)):
#     #         error_vector = deepcopy(error_vectors[i])
#     #         error_vector[j] = 1
#     #         error_vectors2.append(error_vector)
    
#     # for el in error_vectors2:
#     #     error_vectors.append(el)
    
#     return(error_vectors)

# def get_syndromes_vectors(error_vectors, code_word):
#     syndromes_vectors = []
#     for i in range(len(error_vectors)):
#         syndromes_vectors.append(np.polydiv(error_vectors[i], code_word)[1])
#     return(syndromes_vectors)

# def decode_code_word(code_word):
#     print(123)

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
    initial_code_words = []
    for code_word_with_mistake in code_words_with_mistakes:
        initial_code_words.append(correct_mistake_in_code_word(code_word_with_mistake, gen_polynom, n, t))
    return initial_code_words


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
    initial_inf_words = []
    for code_word in code_words:
        initial_inf_words.append(get_inf_word_from_code_word(code_word, gen_polynom, len_of_inf_word))
    return initial_inf_words

# получить букву из информационного слова
def make_char_from_inf_word(inf_word):
    return chr(int('0b' + ''.join([str(num) for num in reversed(deepcopy(inf_word))]), 2))

def make_char_from_inf_word(inf_words, need_len_to_make_char_from_inf_word):
    initial_text = ''
    text = deepcopy(inf_words)
    for i in range(len(text)):
        text[i] = ''.join([str(char) for char in text[i]])
    text = ''.join(text)
    for j in range(len(text)//need_len_to_make_char_from_inf_word):
        initial_text += chr(int('0b' + ''.join(reversed(list(text[j*need_len_to_make_char_from_inf_word:(j+1)*need_len_to_make_char_from_inf_word]))), 2))
    return initial_text

def get_solution():
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

    text = '1pasdoфывkjsdgfuihduofginфригвынигр ицупвщг  р доыр ваигп'

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

    code_words_with_mistakes = make_mistake_in_vectors(code_words, t)
    print('code_words_with_mistakes: ', code_words_with_mistakes)

    initial_code_words = correct_mistake_in_code_words(code_words_with_mistakes, g, n, t)

    initial_inf_words = get_inf_words_from_code_words(initial_code_words, g, len_of_inf_word)
    print('code_words:', code_words)
    print('initial_code_words:', initial_code_words)
    print('inf_words:', inf_words)
    print('initial_inf_words:', initial_inf_words)

    initial_text = make_char_from_inf_word(initial_inf_words, need_len_to_make_char_from_inf_word)

    print(initial_text == text)























    # all_possible_syndromes = get_syndromes_from_vectors(all_error_vectors, g, n)
    # # for el in all_possible_syndromes:
    # #     print(el)

    # code_words_with_mistakes = make_mistake_in_vectors(code_words, 2)

    # all_syndromes = get_syndromes_from_vectors(code_words_with_mistakes, g, n)
    # # print('syndr ', all_syndromes)

    # # initial_letters = []
    # # for i in range(len(all_syndromes)):
    # #     if (sum(all_syndromes[i]) == 0):
    # #         initial_letter = deepcopy(inf_words[i])
    # #         initial_letter.reverse()
    # #         initial_letter = chr(int('0b' + ''.join([str(num) for num in initial_letter]), 2))
    # #         initial_letters.append(initial_letter)
    # #         print(initial_letter)
    # #     elif (all_syndromes[i] in all_possible_syndromes):
    # #         # print('n', n)
    # #         e = all_syndromes[i]
    # #         syndrome = all_syndromes[i]
    # #         for j in range(1, n):
    # #             # print(j)
    # #             left_part = list(Polynomial([0, 1]) * Polynomial(syndrome))
    # #             syndrome =  get_syndrome_from_code_word_vector(left_part, g, n)
    # #             # print(syndrome)
    # #             if (sum(syndrome) <= 2):
    # #                 e = Polynomial([0, 1]) ** 2
    # #                 # print('e', e)
    # # code_word = [1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    # code_word = [0,1,1,1,0,1,1,0,0,1,0,1]
    # e = get_syndrome_from_code_word_vector(code_word, g, n)
    # syndrome = get_syndrome_from_code_word_vector(code_word, g, n)
    # for j in range(1, n):
    #     # print(j)
    #     left_part = list(Polynomial([0, 1]) * Polynomial(syndrome))
    #     syndrome =  get_syndrome_from_code_word_vector(left_part, g, n)
    #     print(syndrome)
    #     if (sum(syndrome) <= 2):
    #         e = Polynomial([0, 1]) ** (n-j) % Polynomial([1,0,0,0,0,0])
    #         print(n)

    # print(initial_letters)

get_solution()

# print(list(get_code_word(i,g)))
# print(error_vectors[0] == Polynomial([1,0,0,0,0,0,0]))




# i = np.array([1, 1, 0, 1])

# # Define the second polynomial as a NumPy array
# g = np.array([1, 1, 0, 1])

# v = np.array([1, 0, 1, 1, 0, 0, 1])
# error_vectors = get_error_vectors(7)

# print(get_syndromes_vectors(error_vectors, g))
# print(get_syndromes_vectors(error_vectors, g))

# print(get_code_word(deepcopy(i), deepcopy(g)))
# print(get_error_vectors(7))

