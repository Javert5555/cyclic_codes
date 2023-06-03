import numpy as np
from copy import deepcopy
from numpy.polynomial import Polynomial
from random import randint


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

def get_n(g, len_of_inf_word):
    gen_polynom = deepcopy(list(g))
    m = 0
    for i in range(len(g),0,-1):
        if gen_polynom[i-1] == 1:
            m = i-1
            break
    return m + len_of_inf_word

def get_inf_words(text, len_of_inf_word):
    inf_words = [bin(ord(char))[2:] for char in list(text)]
    for i in range(len(inf_words)):
        inf_words[i] = list(inf_words[i])
        while len(inf_words[i]) < len_of_inf_word:
            inf_words[i].insert(0, 0)
        inf_words[i] = [int(num) for num in inf_words[i]]
        inf_words[i].reverse()
        # inf_words[i] = Polynomial(inf_words[i])
    # print(inf_words)
    return inf_words

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

def get_error_vectors(n):
    error_vectors = []
    # количество вектор ошибок равно количеству строк транспонированной проверочной матрицы
    for i in range(n):
        error_vector = []
        for j in range(n):
            error_vector.append(0)
        error_vector[i] = 1
        # т.к. единицы идут справа-налево по диагонали
        # error_vector.reverse()
        error_vectors.append(error_vector)
    # вектора для декодирования двух ошибок, например:
    # 110000
    # 101000
    # 100100
    # ...
    error_vectors2 = []

    for i in range(len(error_vectors)):
        for j in range(i+1, len(error_vectors)):
            error_vector = deepcopy(error_vectors[i])
            error_vector[j] = 1
            error_vectors2.append(error_vector)
    
    for el in error_vectors2:
        error_vectors.append(el)
    
    return(error_vectors)

def get_syndrome_from_code_word_vector(code_word, gen_polynom, n):
    syndrome = list(Polynomial(code_word) % Polynomial(gen_polynom))
    for i in range(len(syndrome)):
        if syndrome[i] % 2 == 0:
            syndrome[i] = 0
        else:
            syndrome[i] = 1
    while len(syndrome) < n:
        syndrome.append(0)
    return syndrome

def get_syndromes_from_error_vectors(error_vectors, gen_polynom, n):
    syndromes = []
    for i in range(len(error_vectors)):
        syndromes.append(get_syndrome_from_code_word_vector(error_vectors[i], gen_polynom, n))
    return syndromes

def get_code_word_without_mistake(code_word_with_mistake, error_vector, n):
    code_word_without_mistake = list(Polynomial(code_word_with_mistake) - Polynomial(error_vector))
    for i in range(len(code_word_without_mistake)):
        if code_word_without_mistake[i] % 2 == 0:
            code_word_without_mistake[i] = 0
        else:
            code_word_without_mistake[i] = 1
    while len(code_word_without_mistake) < n:
        code_word_without_mistake.append(0)
    return code_word_without_mistake

def get_inf_word_from_code_word(code_word, gen_polynom):
    inf_word = list(Polynomial(code_word) // Polynomial(gen_polynom))
    for i in range(len(inf_word)):
        if inf_word[i] % 2 == 0:
            inf_word[i] = 0
        else:
            inf_word[i] = 1
    return inf_word

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

def make_mistake_in_vectors(vectors, num_of_errors):
    vectors_copy = deepcopy(vectors)
    for i in range(len(vectors)):
        vectors_copy[i] = make_mistake_in_vector(vectors_copy[i], num_of_errors)
    return vectors_copy

def get_solution():
    g = [1, 0, 0, 0, 1, 0, 1, 1, 1]
    # code_word = np.array([0, 1, 0, 0, 0, 0, 1, 0, 1])
    # code_word = np.array([0, 0, 0, 0, 1])
    # v = np.array([1, 0, 1, 1, 0, 0, 1])
    len_of_inf_word = 7
    n = get_n(g, len_of_inf_word)
    inf_words = get_inf_words("9foadsasqnfi", len_of_inf_word)
    print(inf_words)
    code_words = get_code_words(inf_words, g, n)
    # print(code_words)
    all_error_vectors = get_error_vectors(n)
    # print(len(error_vectors))
    # for el in all_error_vectors:
    #     print(el)
    
    all_possible_syndromes = get_syndromes_from_error_vectors(all_error_vectors, g, n)
    # for el in all_possible_syndromes:
    #     print(el)

    code_words_with_mistakes = make_mistake_in_vectors(code_words, 1)

    all_syndromes = get_syndromes_from_error_vectors(code_words_with_mistakes, g, n)
    print('syndr ', all_syndromes)

    initial_letters = []
    for i in range(len(all_syndromes)):
        if (sum(all_syndromes[i]) == 0):
            initial_letter = deepcopy(inf_words[i])
            initial_letter.reverse()
            initial_letter = chr(int('0b' + ''.join([str(num) for num in initial_letter]), 2))
            initial_letters.append(initial_letter)
            print(initial_letter)
        elif (all_syndromes[i] in all_possible_syndromes):
            index_of_error_vector = all_possible_syndromes.index(all_syndromes[i])
            print(index_of_error_vector)
            code_word_without_mistake = get_code_word_without_mistake(code_words[i], all_error_vectors[index_of_error_vector], n)
            print(code_word_without_mistake)
            inf_word = get_inf_word_from_code_word(code_word_without_mistake, g)
        #     print(inf_word)
            inf_word.reverse()
            letter = chr(int('0b' + ''.join([str(num) for num in inf_word]), 2))
            initial_letters.append(letter)
        #     print(letter)
    print(initial_letters)

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

