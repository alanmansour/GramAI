import csv
from datasets import load_dataset
import click

def generate_csv(csv_path, dataset):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["input", "target"])
        for example in dataset:
            input_text = f"grammar: {example['input']}"
            target_text = example['output']
            writer.writerow([input_text, target_text])


@click.command()
@click.argument("number_of_examples", type=click.INT, default= 10000)
@click.argument("data_path", type=click.Path(exists=True), default='data/processed/train.csv')
def main(number_of_examples, data_path):
    dataset_train = load_dataset('liweili/c4_200m', split='train', streaming=True, trust_remote_code=True)
    print(dataset_train)
    dataset_train = dataset_train.take(number_of_examples)
    generate_csv(data_path, dataset_train)

if __name__=='__main__':
    main()
