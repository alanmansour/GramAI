import csv
import hydra
import os
from datasets import load_dataset, IterableDataset
from omegaconf import DictConfig

def generate_csv(csv_path: str | os.PathLike,
                 dataset: IterableDataset
                 ) -> None:
    
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["input", "target"])
        for example in dataset:
            input_text = f"grammar: {example['input']}"
            target_text = example['output']
            writer.writerow([input_text, target_text])

@hydra.main(config_path='.', config_name="config.yaml", version_base = None)
def make_dataset(cfg: DictConfig) -> None:
    """Downloads dataset from huggingface hub and """
    if not cfg:
        raise ValueError("Configuration file must be present.")
    if cfg.n_examples <= 0:
        raise ValueError("n_examples must be a non-zero, positive integer.")
    dataset_train = load_dataset('liweili/c4_200m', split='train', streaming=True, trust_remote_code=True)
    dataset_train = dataset_train.take(cfg.n_examples)
    print(os.getcwd())
    # dataset_path = os.path.join(hydra.utils.get_original_cwd(), cfg.dataset_path) #Hydra changes cwd
    generate_csv(cfg.dataset_path, dataset_train)

if __name__=='__main__':
    make_dataset()
