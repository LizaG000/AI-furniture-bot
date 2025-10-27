import json
import numpy as np
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import tokenizer_from_json

# from tensorflow.keras.layers import TextVectorization, Embedding, GlobalAveragePooling1D, Dense
# from tensorflow.keras.models import Sequential
# from keras.utils import to_categorical
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def get_json() -> dict:
    with open("data/intents copy.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def get_questions_answers() -> tuple[list[str], list[str]]:
    with open("data/dialogs.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    questions = []
    answers = []
    
    for item in data:
        questions.append(item.get("question", ""))
        answers.append(item.get("answer", ""))
    
    return questions, answers


def train_model():
    x_texts = []
    y_labels = []
    intents_dict = get_json()
    for key, data in intents_dict.items():
        for example in data["input_example"]:
            x_texts.append(example)
            y_labels.append(key)
    print(y_labels)
    vectorizer = TfidfVectorizer()
    x = vectorizer.fit_transform(x_texts)

    model = LogisticRegression()
    model.fit(x, y_labels)

    with open('models/model1.pkl', "wb") as f:
        pickle.dump(model, f)

    with open('models/vectorizer1.pkl', "wb") as f:
        pickle.dump(vectorizer, f)

# train_model()

def predict_intent(text):
    with open("models/model1.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("models/vectorizer1.pkl", "rb") as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    
    X = vectorizer.transform([text])
    intent = model.predict(X)[0]
    return intent

def train_dialog_model():
    questions, answers = get_questions_answers()
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(questions)
    
    # Сохраняем модель и векторизатор
    with open('models/dialog_vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    with open('models/dialog_questions.pkl', 'wb') as f:
        pickle.dump(questions, f)
    with open('models/dialog_answers.pkl', 'wb') as f:
        pickle.dump(answers, f)
# train_dialog_model()

# Функция для поиска ответа
def get_answer(user_question):
    with open('models/dialog_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    with open('models/dialog_questions.pkl', 'rb') as f:
        questions = pickle.load(f)
    with open('models/dialog_answers.pkl', 'rb') as f:
        answers = pickle.load(f)
    
    user_vec = vectorizer.transform([user_question])
    questions_vec = vectorizer.transform(questions)
    
    similarity = cosine_similarity(user_vec, questions_vec)
    best_idx = similarity.argmax()
    
    return answers[best_idx]

def predirect_keras_model(text: str) -> str:
    model = load_model('models/text_classification_model.keras')
    with open('models/tokenizer.json', 'r', encoding='utf-8') as f:
        tokenizer_data = f.read()
    tokenizer = tokenizer_from_json(tokenizer_data)
    answers = ['add_address', 'delete_address', 'list_addresses', 'not_understood', 'registration', 'greeting', 'goodbye', 'catalog', 'buy', 'basket', 'favorites', 'contacts']
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=model.input_shape[1], padding='post')

    pred = model.predict(padded)
    print(pred)
    
    print("-----=----")
    ming = []
    for i in pred:
        ming.append(np.argmax(pred)-i)
        
    print(pred)
    
    print("-----=----")
    print(ming)
    
    print("-----=----")
    pred_label = answers[np.argmax(pred)]
    return pred_label