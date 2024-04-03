import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


def clean_text(text, stop_words):
    # Remove stop words and non-alphabetic characters
    cleaned_text = ' '.join([word.lower() for word in word_tokenize(text) if word.isalpha() and word.lower() not in stop_words])
    return cleaned_text

def calculate_sentiment_scores(text, positive_words, negative_words):
    positive_score = sum(1 for word in word_tokenize(text) if word.lower() in positive_words)
    negative_score = -1 * sum(1 for word in word_tokenize(text) if word.lower() in negative_words)
    
    polarity_score = (positive_score - negative_score) / (positive_score + negative_score + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(word_tokenize(text)) + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score

def calculate_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    
    average_sentence_length = len(words) / len(sentences)
    percentage_complex_words = sum(1 for word in words if len(word) > 2) / len(words)
    
    fog_index = 0.4 * (average_sentence_length + percentage_complex_words)
    average_words_per_sentence = len(words) / len(sentences)
    complex_word_count = sum(1 for word in words if len(word) > 2)
    word_count = len(words)
    
    syllable_count_per_word = calculate_syllable_count(words)
    
    personal_pronouns_count = count_personal_pronouns(text)
    
    average_word_length = sum(len(word) for word in words) / len(words)
    
    return (
        average_sentence_length, percentage_complex_words, fog_index,
        average_words_per_sentence, complex_word_count, word_count,
        syllable_count_per_word, personal_pronouns_count, average_word_length
    )

def calculate_syllable_count(words):
    syllable_count = 0
    for word in words:
        syllable_count += sum(1 for char in word if char.lower() in 'aeiou')
        
        # Handle exceptions
        if word.endswith(('es', 'ed')):
            syllable_count -= 1
    
    return syllable_count

def count_personal_pronouns(text):
    personal_pronouns = re.findall(r'\b(?:I|we|my|ours|us)\b', text, flags=re.IGNORECASE)
    return len(personal_pronouns)

def main():
    # Load stop words, positive words, and negative words
    stop_words = set(stopwords.words('english'))
    
    with open('StopWords/positive-words.txt', 'r') as file:
        positive_words = set(file.read().splitlines())

    with open('StopWords/negative-words.txt', 'r') as file:
        negative_words = set(file.read().splitlines())
    
    # Replace 'YourTextHere' with the actual text you want to analyze
    your_text = 'Output Data Structure.xlsx'
    
    # Cleaning
    cleaned_text = clean_text(your_text, stop_words)
    
    # Sentiment Analysis
    positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment_scores(cleaned_text, positive_words, negative_words)
    
    # Readability Analysis
    readability_results = calculate_readability(cleaned_text)
    
    # Output Results
    print(f"Positive Score: {positive_score}")
    print(f"Negative Score: {negative_score}")
    print(f"Polarity Score: {polarity_score}")
    print(f"Subjectivity Score: {subjectivity_score}")
    
    print("\nReadability Analysis:")
    print(f"Average Sentence Length: {readability_results[0]}")
    print(f"Percentage of Complex Words: {readability_results[1]}")
    print(f"Fog Index: {readability_results[2]}")
    print(f"Average Words Per Sentence: {readability_results[3]}")
    print(f"Complex Word Count: {readability_results[4]}")
    print(f"Word Count: {readability_results[5]}")
    print(f"Syllable Per Word: {readability_results[6]}")
    print(f"Personal Pronouns Count: {readability_results[7]}")
    print(f"Average Word Length: {readability_results[8]}")

if __name__ == "__main__":
    main()
