import nltk
import os


class Configurator:
    @staticmethod
    def init():
        # Configurator.download_nltk_deps()
        Configurator.download_spacy_models()

    @staticmethod
    def download_nltk_deps():
        """
        Download NLTK deps
        """

        nltk.download('wordnet')
        nltk.download('punkt')

    @staticmethod
    def download_spacy_models():
        """
        Download spacy models
        """

        os.system("python3 -m spacy download en_core_web_sm")
        os.system("python3 -m spacy download en_core_web_md")
        os.system("python3 -m spacy download en_core_web_trf")


Configurator.init()