from lingua import Language, LanguageDetectorBuilder

# Sample text to detect the language

TEXT = "hello today is a great day"

languages = [Language.ENGLISH, 
             Language.FRENCH, 
             Language.GERMAN, 
             Language.SPANISH, 
             Language.CHINESE, 
             Language.JAPANESE,
             Language.KOREAN,
             Language.HINDI,
             Language.PORTUGUESE,
             Language.RUSSIAN,
             Language.BULGARIAN,
             Language.ARABIC,
             Language.INDONESIAN,
             Language.THAI,
             Language.TURKISH,
             Language.VIETNAMESE,
             Language.GERMAN,
    ] # 17 Languages to total or you can choose ALL

# Build the language detector considering all supported languages
detector = LanguageDetectorBuilder.from_languages(*languages).build()

def TopLang(text):
    detected_language = detector.compute_language_confidence_values(text)
    return detected_language[0].language.name, detected_language[0].value 

# Output the detected language

if __name__ == '__main__':
    text = TEXT # You can change it to any language that is in the languages list
    detected_language = TopLang(text)
    confidence_values = detector.compute_language_confidence_values(text)
    for confidence in confidence_values:
        print(f"The detected language is: {confidence.language.name}, {confidence.value:.2f}")