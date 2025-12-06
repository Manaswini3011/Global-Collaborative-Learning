# Translation Setup Guide

## Current Implementation

The platform now includes automatic message translation based on each user's selected language preference. When a user views messages in a discussion room, all messages are automatically translated to their preferred language.

## How It Works

1. **User Language Preference**: Each user selects their preferred language during registration
2. **Message Storage**: Messages are stored with the sender's original language
3. **On-Demand Translation**: When retrieving messages, they are translated to the viewing user's language
4. **Display**: Users see messages in their language, with option to view original

## Current Status: Demo Mode

The current implementation uses a placeholder translation function. For production use, you need to integrate a real translation API.

## Integration Options

### Option 1: Google Translate (Free, No API Key)

Uses the `googletrans` library which is free and doesn't require an API key.

**Installation:**
```bash
pip install googletrans==4.0.0rc1
```

**Update `app.py`:**
```python
from googletrans import Translator

translator = Translator()

def translate_text(text, from_lang, to_lang):
    if from_lang == to_lang or not from_lang or not to_lang:
        return text
    
    try:
        result = translator.translate(text, src=from_lang, dest=to_lang)
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text  # Fallback to original text
```

### Option 2: Google Cloud Translation API (Paid, More Reliable)

Requires Google Cloud account and API key.

**Installation:**
```bash
pip install google-cloud-translate
```

**Setup:**
1. Create a Google Cloud project
2. Enable Translation API
3. Create service account and download JSON key
4. Set environment variable: `export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"`

**Update `app.py`:**
```python
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def translate_text(text, from_lang, to_lang):
    if from_lang == to_lang or not from_lang or not to_lang:
        return text
    
    try:
        result = translate_client.translate(
            text, 
            source_language=from_lang, 
            target_language=to_lang
        )
        return result['translatedText']
    except Exception as e:
        print(f"Translation error: {e}")
        return text
```

### Option 3: DeepL API (High Quality, Paid)

Known for high-quality translations.

**Installation:**
```bash
pip install deepl
```

**Setup:**
1. Sign up at https://www.deepl.com/pro-api
2. Get API key

**Update `app.py`:**
```python
import deepl

translator = deepl.Translator("YOUR_API_KEY")

def translate_text(text, from_lang, to_lang):
    if from_lang == to_lang or not from_lang or not to_lang:
        return text
    
    try:
        # DeepL uses different language codes
        result = translator.translate_text(text, source_lang=from_lang.upper(), target_lang=to_lang.upper())
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text
```

### Option 4: LibreTranslate (Open Source, Self-Hosted)

Free and open-source, can be self-hosted.

**Installation:**
```bash
pip install libretranslate
```

**Update `app.py`:**
```python
from libretranslate import LibreTranslate

lt = LibreTranslate(api_url="https://libretranslate.de/")

def translate_text(text, from_lang, to_lang):
    if from_lang == to_lang or not from_lang or not to_lang:
        return text
    
    try:
        result = lt.translate(text, from_lang, to_lang)
        return result
    except Exception as e:
        print(f"Translation error: {e}")
        return text
```

## Language Code Mapping

The platform uses standard language codes:
- `en` - English
- `es` - Spanish
- `fr` - French
- `pt` - Portuguese
- `ja` - Japanese
- `zh` - Chinese
- `de` - German
- `hi` - Hindi

## Features

### Automatic Translation
- Messages are automatically translated when retrieved
- Translation happens server-side for security
- Each user sees messages in their preferred language

### Original Text View
- Users can click to view the original message
- Shows language indicator (e.g., "EN → ES")
- Preserves original message for reference

### Language Indicators
- Message headers show translation status
- Badge indicates source and target languages
- Clear visual feedback for translated content

## Performance Considerations

1. **Caching**: Consider caching translations to reduce API calls
2. **Rate Limiting**: Implement rate limiting for translation API
3. **Batch Translation**: For multiple messages, consider batch API calls
4. **Fallback**: Always fallback to original text if translation fails

## Testing

To test translation:
1. Create two users with different languages (e.g., English and Spanish)
2. Add them to the same team
3. Create a discussion room
4. Send messages from each user
5. Verify each user sees messages in their language

## Current Limitations

- Placeholder translation function (shows indicator but doesn't actually translate)
- No caching of translations
- No batch translation support
- Single translation per message retrieval

## Future Enhancements

- Real-time translation as messages are sent
- Translation caching for performance
- Voice message translation
- Multi-language support in UI
- Translation quality indicators

