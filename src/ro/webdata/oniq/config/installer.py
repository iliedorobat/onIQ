import os


class Installer:
    @staticmethod
    def init():
        # Installer.init_spacy()
        # Installer.init_nltk()
        Installer.install_deps()

    @staticmethod
    def init_spacy():
        """
        Install <b>spacy</b>, its dependencies.
        """

        os.system("pip3 install --user -U setuptools wheel")
        os.system("pip3 install --user -U spacy")
        # TODO: to read: https://towardsdatascience.com/named-entity-recognition-with-spacy-and-the-mighty-roberta-97d879f981#c19e
        os.system("pip3 install --user spacy-transformers")
        os.system("pip3 install --user spacy-wordnet")

    @staticmethod
    def init_nltk():
        """
        Install <b>NLTK</b>.
        """

        os.system("pip3 install --user nltk==3.5")

    @staticmethod
    def install_deps():
        """
        Install dependencies.
        """

        # TODO: textacy?
        os.system("pip3 install pip-autoremove")
        os.system("pip3 install gensim")
        os.system("pip3 install --user -U numpy")
        os.system("pip3 install --user parse")
        os.system("pip3 install --user langdetect")
        os.system("pip3 install --user SPARQLWrapper")
        os.system("pip3 install --user iteration-utilities")
        os.system("pip3 install --user progress")
        os.system("pip3 install --user pydash")
        os.system("pip3 install --user sphinx")


Installer.init()
