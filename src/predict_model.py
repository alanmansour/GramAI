import os
import os.path as path

import click
import matplotlib.pyplot as plt
import torch
import wandb

from models.model import MyAwesomeModel
from happytransformer import TTSettings
from happytransformer import  HappyTextToText




@click.command()
@click.argument("trained_model", type=click.Path(exists=True),default="models/model")
@click.argument("data", type=click.STRING, default= "grammar: I I wants to codes.")
def main(trained_model, data):
    model = HappyTextToText('t5-small',trained_model)
    beam_settings =  TTSettings(num_beams=5, min_length=1, max_length=100)
    input_text_1 = data
    output_text_1 = model.generate_text(input_text_1, args=beam_settings)
    print(output_text_1.text)
  

if __name__ == "__main__":
    main()
