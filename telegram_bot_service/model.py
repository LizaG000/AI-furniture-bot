import json
import numpy as np
import pickle
# from tensorflow.keras.layers import TextVectorization, Embedding, GlobalAveragePooling1D, Dense
# from tensorflow.keras.models import Sequential
# from keras.utils import to_categorical
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def get_json() -> dict:
    with open("data/intents.json", "r", encoding="utf-8") as f:
        return json.load(f)
#
# def train_model_keras():
#     x_texts = []  # тексты
#     _y_labels = []  # индексы интентов
#     intents_dict = get_json()
#     intent_names = list(intents_dict.keys())
#
#     # подготовка данных
#     for key, data in intents_dict.items():
#         for example in data["input_example"]:
#             x_texts.append(example)
#             _y_labels.append(key)
#     print(_y_labels)
#     x_texts = np.array(x_texts)
#     y_labels = np.array(_y_labels)
#
#     # векторизация текста
#     vocab_size = 300
#     embedding_dim = 10
#     sequence_length = 6
#
#     vectorizer = TextVectorization(
#         max_tokens=vocab_size,
#         output_mode='int',
#         output_sequence_length=sequence_length
#     )
#     vectorizer.adapt(x_texts)
#
#     # преобразуем тексты в последовательности чисел
#     x_vect = vectorizer(x_texts)
#     intent_names = list(intents_dict.keys())  # ['greeting', 'goodbye', 'catalog', ...]
#     y_labels = [intent_names.index(label) for label in y_labels]
#     print(y_labels)
#     y_labels = to_categorical(y_labels, num_classes=8).astype(np.float32)
#     print("Векторы x (числовое представление текста):")
#     print(x_vect.numpy())
#     print("y (метки интентов):")
#     print(y_labels)
#
#     model = Sequential([
#         Embedding(input_dim=vocab_size, output_dim=embedding_dim, mask_zero=True),
#         GlobalAveragePooling1D(),
#         Dense(32, activation='relu'),
#         Dense(len(intent_names), activation='softmax')
#     ])
#
#     model.compile(
#         loss='categorical_crossentropy',
#         optimizer='adam',
#         metrics=['accuracy']
#     )
#
#     # Передаём строки напрямую
#     model.fit(x_vect, y_labels, validation_split=0.2, epochs=30, batch_size=16)
#     predictions = model.predict(x_vect)
#     predicted_classes = np.argmax(predictions, axis=1)
#
#     print("\nПредсказания модели для каждого текста:")
#     for text, true_idx, pred_idx in zip(x_texts, y_labels, predicted_classes):
#         print(f"Текст: {text}")
#         print(f"Истинный интент: {true_idx}")
#         print(f"Предсказанный интент: {pred_idx}")
#         print("---")

def train_model():
    x_texts = []
    y_labels = []
    intents_dict = get_json()
    for key, data in intents_dict.items():
        for example in data["input_example"]:
            x_texts.append(example)
            y_labels.append(key)
    vectorizer = TfidfVectorizer()
    x = vectorizer.fit_transform(x_texts)

    model = LogisticRegression()
    model.fit(x, y_labels)

    with open('models/model.pkl', "wb") as f:
        pickle.dump(model, f)

    with open('models/vectorizer.pkl', "wb") as f:
        pickle.dump(vectorizer, f)

train_model()