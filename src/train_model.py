import os
import hydra
from happytransformer import HappyTextToText, TTTrainArgs
from omegaconf import DictConfig


os.environ["WANDB_PROJECT"] = "mlops-proj47"
os.environ["WANDB_LOG_MODEL"] = "checkpoint"

@hydra.main(config_path='models/config', config_name="config.yaml")
def train(cfg: DictConfig) -> None:
    """ Train the model using the provided configuration. """
    model = HappyTextToText('t5-small')
    args = TTTrainArgs(batch_size=cfg.batch_size, report_to='wandb')

    model.train(cfg.dataset_path, args=args)

if __name__=='__main__':
    train()
