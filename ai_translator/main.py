import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import ArgumentParser, ConfigLoader, LOG
from model import GLMModel, OpenAIModel
from translator import PDFTranslator
from gui import AITranslatorGUI

if __name__ == "__main__":
    # argument_parser = ArgumentParser()
    # args = argument_parser.parse_arguments()
    config_loader = ConfigLoader('config.yaml')

    config = config_loader.load_config()

    model_name = config['OpenAIModel']['model']
    api_key =  config['OpenAIModel']['api_key']
    model = OpenAIModel(model=model_name, api_key=api_key)
    
    app = AITranslatorGUI(model)
    app.mainloop()

