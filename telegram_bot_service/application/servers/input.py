from natasha import MorphVocab
from keras.layers import Dense
from keras.models import Sequential
import tensorflow as tf
from keras import layers, Model, Input

from keras.preprocessing.sequence import pad_sequences
import numpy as np
# from pip.keras.models import Sequential
# from tensorflow.keras.layers import Dense, Dropout


def get_dictionary_dataset() -> list[str]:
    with open("data/dictionary_dataset.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        return content.split("\n")

def get_token_dataset() -> list[str]:
    with open("data/token_dataset.txt", 'r', encoding='utf-8') as file:
        content = file.read()
        return content.split("\n")

def get_data(title: str) -> tuple[list[str], list[str]]:
    with open(title, 'r', encoding='utf-8') as file:
        content = file.read()
        content = content.split("\n")
        x = [content[i] for i in range(0, len(content), 2)]
        y = [content[i] for i in range(1, len(content), 2)]
        return x, y


def filter_dictionary(input_words: str) -> tuple[str, float]:
    dictionary = get_dictionary_dataset()
    _min = 100
    find_word = input_words
    vocab = MorphVocab()
    normal_forms = vocab.normal_forms(input_words)[0]
    if normal_forms in dictionary:
        return input_words, 0
    len_max = len(input_words) + 2
    len_min = len_max - 4
    for word in dictionary:
        if len_min < len(word) and len_max > len(word):
            if len(set(word) & set(input_words)) < max(len(set(word)), len(set(input_words)))-4:
                continue
            if len(word) < 3 or len(input_words) < 3:
                changes = levenshtein_algorithm(input_words, word)
            elif word[0] in input_words[0:3] or word[1] in input_words[0:3] or word[2] in input_words[0:3]:
                changes = levenshtein_algorithm(input_words, word)
            else:
                changes = 100
            if changes < _min:
                _min = changes
                find_word = word
    return  find_word, _min


def levenshtein_algorithm(input_word, word) -> float:
    k_array = []
    keyboard = [["й", "ц", "у", "к", "е", "н", "г", "ш", "щ", "з", "х", "ъ",], ["ф", "ы", "в", "а", "п", "р", "о", "л", "д", "ж", "э"], ["я", "ч", "с", "м", "и", "т", "ь", "б", "ю"]]
    replacement = [("и", "е"), ("а", "о"), ("д", "т"), ("з", "с"), ("г", "к"), ("б", "п"), ("в", "ф"), ("ж", "ш")]
    for i in range(len(input_word)+1):
        k_array.append([i] + [0] * len(word))
    for i in range(len(word)+1):
        k_array[0][i] = i
    for i in range(1, len(input_word)+1):
        for j in range(1, len(word)+1):
            k_insert = 1
            k_pop = 1
            if i == len(input_word) and input_word[i-1] in "смить":
                k_pop = 0.8
            k_equals = 1
            if input_word[i-1] == word[j-1]:
                k_equals = 0
            elif (input_word[i-1], word[j-1]) in replacement or (word[j-1], input_word[i-1]) in replacement:
                k_equals = 0.2
            else:
                i_word = 0
                j_word = 0
                for _i in range(3):
                    if word[j-1] in keyboard[_i]:
                        i_word = _i
                        j_word = keyboard[_i].index(word[j-1])
                for _i in range(3):
                    for _j in range(1, 3):
                        try:
                            if keyboard[i_word+1-_i][j_word+1-_j] == input_word[i]:
                                k_equals = 0.8
                                break
                        except:
                            continue
            k = min(k_array[i][j-1]+k_pop, k_array[i-1][j]+1, k_array[i-1][j-1]+k_equals)
            if k > 30 and i == j:
                return 100
            else:
                k_array[i][j] = k
    distance = k_array[-1][-1]
    length_diff = abs(len(input_word)-len(word))
    normalized_distance = distance + length_diff * 0.5
    prefix_len = 0
    for i in range(min(len(input_word), len(word))):
        if input_word[i] == word[i]:
            prefix_len += 1
        else:
            break
    prefix_bonus = 0
    if len(input_word) > 0:
        prefix_bonus += (prefix_len / len(input_word)) * 2.5
    if len(word) < len(input_word):
        normalized_distance += 1.0
    normalized_distance = max(0, normalized_distance - prefix_bonus)
    return normalized_distance

def clearing_input(_input: str):
    punctuation_marks = ".,/?!*\"_+&=-\\\n"
    _input.strip()
    _input = _input.lower()
    _input = ' '.join((_input.split()))
    _input = _input.split(" ")
    clean_input = len(_input) * ["_"]
    i = 0
    while i < len(_input):
        double_min = 100
        if _input[i] == "_":
            i += 1
            continue
        if _input[i][-1] in punctuation_marks:
            _input.insert(i+1, _input[i][-1])
            clean_input.insert(i+1, _input[i][-1])
            _input[i] = _input[i][:-1]
            _input[i+1] = "_"
            continue
        if len(_input) - i > 1 and len(_input[i+1]) > 2 and len(_input[i]) > 2:
            double_input_word, double_min = filter_dictionary("".join([_input[i], _input[i+1]]))
        input_word, _min = filter_dictionary(_input[i])
        if _min <= 30 and _min < double_min:
            _input[i], clean_input[i] = "_", input_word
            i += 1
            continue
        elif double_min <= 30:
            _input[i], clean_input[i] = "_", double_input_word
            _input.pop(i+1)
            clean_input.pop(i+1)
            i += 1
            continue
        print("Ошибка")
        break
    return clean_input



print(clearing_input("Что у меня в карзине? чупрыный"))
# x_train, y_train = get_data("training.txt")
# x_test, y_test = get_data("test.txt")
# # очистка данных от ошибок
# for i in range(len(x_train)):
#     print(i, x_train[i])
#     x_train[i] = clearing_input(x_train[i])
#     print(y_train[i])
#     y_train[i] = clearing_input(y_train[i])
#     print()

# # for i in range(len(x_test)):
# #     print(i, x_test[i])
# #     x_test[i] = clearing_input(x_test[i])
# #     print(y_test[i])
# #     y_test[i] = clearing_input(y_test[i])
# #     print()

# #превращение в токен
# for i in range(len(x_train)):
#     print(i, x_train[i])
#     x_train[i] = transfer_to_token(x_train[i])
#     print(y_train[i])
#     y_train[i] = transfer_to_token(y_train[i])
#     print()

# # for i in range(len(x_test)):
# #     print(i, x_test[i])
# #     x_test[i] = transfer_to_token(x_test[i])
# #     print(y_test[i])
# #     y_test[i] = transfer_to_token(y_test[i])
# #     print()

# # x_padded = pad_sequences(x_train, padding="post", maxlen=15)
# # y_padded = pad_sequences(y_train, padding="post", maxlen=15)

# # x_padded = tf.constant(x_padded, dtype=tf.int64)
# # y_padded = tf.constant(y_padded, dtype=tf.int64)

# # # x_padded_test = pad_sequences(x_test, padding="post", maxlen=100)
# # # y_padded_test = pad_sequences(y_test, padding="post", maxlen=100)

# # # x_padded_test = tf.constant(x_padded_test, dtype=tf.int64)
# # # y_padded_test = tf.constant(y_padded_test, dtype=tf.int64)
# # # print(x_padded_test[0])
# # # print(y_padded_test[0])
# # vocab_size = 104
# # model = Sequential([
# #     layers.Input(shape=(None,), dtype=tf.int64),
# #     layers.Embedding(input_dim=vocab_size, output_dim=128, mask_zero=True),
# #     layers.LSTM(320, return_sequences=True),
# #     layers.TimeDistributed(layers.Dense(104, activation="softmax"))
# # ])

# # model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=["accuracy"])
# # model.fit(x_padded, y_padded,batch_size=200,
# #     validation_split=0.2,
# #     epochs=10,
# #     verbose=1 )

# # model.save_weights('model_full.weights.h5') 
# # model.load_weights('model_full.weights.h5')

# # scores = model.evaluate(x_padded_test, y_padded_test, verbose=1)
# # print("Доля правильных ответов на тестовых данных в процентах: ", round(scores[1]*100, 4))
# start_token = 104   # первый свободный индекс
# end_token = 105     # второй свободный индекс
# vocab_size = 106 
# embedding_dim = 128
# lstm_units = 256

# # ENCODER
# encoder_inputs = layers.Input(shape=(None,), dtype="int64")
# x = layers.Embedding(vocab_size, embedding_dim, mask_zero=True)(encoder_inputs)
# encoder_outputs, state_h, state_c = layers.LSTM(lstm_units, return_state=True)(x)
# encoder_states = [state_h, state_c]

# # DECODER
# decoder_inputs = layers.Input(shape=(None,), dtype="int64")
# y = layers.Embedding(vocab_size, embedding_dim, mask_zero=True)(decoder_inputs)
# decoder_lstm = layers.LSTM(lstm_units, return_sequences=True, return_state=True)
# decoder_outputs, _, _ = decoder_lstm(y, initial_state=encoder_states)
# decoder_dense = layers.Dense(vocab_size, activation="softmax")
# decoder_outputs = decoder_dense(decoder_outputs)

# # Модель "обучение"
# model = Model([encoder_inputs, decoder_inputs], decoder_outputs)

# model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

# # допустим, у тебя уже есть pad_sequences
# encoder_input_data = pad_sequences(x_train, padding="post", maxlen=20)
# decoder_input_data = pad_sequences([[start_token] + seq for seq in y_train], padding="post", maxlen=20)
# decoder_output_data = pad_sequences([seq + [end_token] for seq in y_train], padding="post", maxlen=20)

# # decoder_output должен быть (batch, seq_len, 1)
# decoder_output_data = tf.expand_dims(decoder_output_data, -1)

# model.fit([encoder_input_data, decoder_input_data], decoder_output_data,
#           batch_size=64,
#           epochs=20,
#           validation_split=0.2)


# # Сохранение весов
# model.save_weights("model_full.weights.h5")

# # Энкодер
# encoder_model = Model(encoder_inputs, encoder_states)

# # Декодер
# deco# Декодер инференса
# decoder_state_input_h = Input(shape=(lstm_units,))
# decoder_state_input_c = Input(shape=(lstm_units,))
# decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]

# # Создаём embedding слой заново, но с теми же весами
# decoder_inputs_inf = Input(shape=(None,), dtype='int64')
# decoder_embedding_inf = model.layers[2](decoder_inputs_inf)  # слой Embedding из обученной модели

# decoder_outputs2, state_h2, state_c2 = decoder_lstm(
#     decoder_embedding_inf, initial_state=decoder_states_inputs
# )

# decoder_states2 = [state_h2, state_c2]
# decoder_outputs2 = decoder_dense(decoder_outputs2)

# decoder_model = Model(
#     [decoder_inputs_inf] + decoder_states_inputs,
#     [decoder_outputs2] + decoder_states2
# )

# def decode_sequence(input_seq, max_len=20):
#     states_value = encoder_model.predict(input_seq, verbose=0)
#     target_seq = np.array([[start_token]])
#     decoded_tokens = []

#     for _ in range(max_len):
#         output_tokens, h, c = decoder_model.predict([target_seq] + states_value, verbose=0)
#         sampled_token_index = np.argmax(output_tokens[0, -1, :])
#         if sampled_token_index == end_token:
#             break
#         decoded_tokens.append(sampled_token_index)
#         target_seq = np.array([[sampled_token_index]])
#         states_value = [h, c]

#     return decoded_tokens


# encoder_input_data_test = pad_sequences(x_test, padding="post", maxlen=20)

# for i in range(len(x_test)):
#     input_seq = np.array([encoder_input_data_test[i]])
#     decoded_tokens = decode_sequence(input_seq)

#     input_words = tokens_to_words(x_test[i])
#     true_words = tokens_to_words(y_test[i])
#     pred_words = tokens_to_words(decoded_tokens)

#     print(f"Example {i}:")
#     print("INPUT  :", " ".join(input_words))
#     print("TARGET :", " ".join(true_words))
#     print("PREDICT:", " ".join(pred_words))
#     print("="*50)
