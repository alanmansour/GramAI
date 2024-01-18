import os
import hydra
from happytransformer import HappyTextToText, TTTrainArgs

os.environ["WANDB_PROJECT"] = "mlops-proj47"
os.environ["WANDB_LOG_MODEL"] = "checkpoint"

def train(train_data_path, cfg):
    model = HappyTextToText('t5-small')
    args = TTTrainArgs(batch_size=8, report_to='wandb')

    model.train(train_data_path, args=args)

if __name__=='__main__':
    PATH = 'data/processed/train.csv'
    train(PATH)
