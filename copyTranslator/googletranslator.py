# -*- coding: utf-8 -*-


from googletrans import Translator

import copyTranslator.translator as  MyTranslator

GoogleLanguages = {'Afrikaans': 'af',
                   'Albanian': 'sq',
                   'Amharic': 'am',
                   'Arabic': 'ar',
                   'Armenian': 'hy',
                   'Azerbaijani': 'az',
                   'Basque': 'eu',
                   'Belarusian': 'be',
                   'Bengali': 'bn',
                   'Bosnian': 'bs',
                   'Bulgarian': 'bg',
                   'Catalan': 'ca',
                   'Cebuano': 'ceb',
                   'Chichewa': 'ny',
                   'Chinese (Simplified)': 'zh-cn',
                   'Chinese (Traditional)': 'zh-tw',
                   'Corsican': 'co',
                   'Croatian': 'hr',
                   'Czech': 'cs',
                   'Danish': 'da',
                   'Dutch': 'nl',
                   'English': 'en',
                   'Esperanto': 'eo',
                   'Estonian': 'et',
                   'Filipino': 'fil',
                   'Finnish': 'fi',
                   'French': 'fr',
                   'Frisian': 'fy',
                   'Galician': 'gl',
                   'Georgian': 'ka',
                   'German': 'de',
                   'Greek': 'el',
                   'Gujarati': 'gu',
                   'Haitian creole': 'ht',
                   'Hausa': 'ha',
                   'Hawaiian': 'haw',
                   'Hebrew': 'he',
                   'Hindi': 'hi',
                   'Hmong': 'hmn',
                   'Hungarian': 'hu',
                   'Icelandic': 'is',
                   'Igbo': 'ig',
                   'Indonesian': 'id',
                   'Irish': 'ga',
                   'Italian': 'it',
                   'Japanese': 'ja',
                   'Javanese': 'jw',
                   'Kannada': 'kn',
                   'Kazakh': 'kk',
                   'Khmer': 'km',
                   'Korean': 'ko',
                   'Kurdish (kurmanji)': 'ku',
                   'Kyrgyz': 'ky',
                   'Lao': 'lo',
                   'Latin': 'la',
                   'Latvian': 'lv',
                   'Lithuanian': 'lt',
                   'Luxembourgish': 'lb',
                   'Macedonian': 'mk',
                   'Malagasy': 'mg',
                   'Malay': 'ms',
                   'Malayalam': 'ml',
                   'Maltese': 'mt',
                   'Maori': 'mi',
                   'Marathi': 'mr',
                   'Mongolian': 'mn',
                   'Myanmar (burmese)': 'my',
                   'Nepali': 'ne',
                   'Norwegian': 'no',
                   'Pashto': 'ps',
                   'Persian': 'fa',
                   'Polish': 'pl',
                   'Portuguese': 'pt',
                   'Punjabi': 'pa',
                   'Romanian': 'ro',
                   'Russian': 'ru',
                   'Samoan': 'sm',
                   'Scots gaelic': 'gd',
                   'Serbian': 'sr',
                   'Sesotho': 'st',
                   'Shona': 'sn',
                   'Sindhi': 'sd',
                   'Sinhala': 'si',
                   'Slovak': 'sk',
                   'Slovenian': 'sl',
                   'Somali': 'so',
                   'Spanish': 'es',
                   'Sundanese': 'su',
                   'Swahili': 'sw',
                   'Swedish': 'sv',
                   'Tajik': 'tg',
                   'Tamil': 'ta',
                   'Telugu': 'te',
                   'Thai': 'th',
                   'Turkish': 'tr',
                   'Ukrainian': 'uk',
                   'Urdu': 'ur',
                   'Uzbek': 'uz',
                   'Vietnamese': 'vi',
                   'Welsh': 'cy',
                   'Xhosa': 'xh',
                   'Yiddish': 'yi',
                   'Yoruba': 'yo',
                   'Zulu': 'zu'}

GoogleLangList = list(GoogleLanguages.keys())
GoogleCodes = {v: k for k, v in GoogleLanguages.items()}


class GoogleTranslator(MyTranslator.Translator):

    def __init__(self):
        self.translator = Translator(service_urls=['translate.google.cn'])

    def get_langlist(self):
        return GoogleLangList

    def lang2code(self, lang):
        return GoogleLanguages[lang]

    def translate(self, string, src, dest):
        return self.translator.translate(string, src=self.lang2code(src), dest=self.lang2code(dest)).text

    def detect(self, string):
        return GoogleCodes[self.translator.detect(string).lang.lower()]
