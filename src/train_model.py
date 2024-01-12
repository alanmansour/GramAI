from datasets import load_from_disk
from happytransformer import HappyTextToText, TTTrainArgs
from happytransformer import TTSettings

def train(train_data_path):
    model = HappyTextToText('t5-small')
    args = TTTrainArgs(batch_size=8)

    model.train(train_data_path, args=args)
    beam_settings =  TTSettings(num_beams=5, min_length=1, max_length=100)
    input_text_1 = "grammar: I I wants to codes."
    output_text_1 = model.generate_text(input_text_1, args=beam_settings)
    print(output_text_1.text)
    model.save("model/")

if __name__=='__main__':
    PATH='data/processed/train.csv'
    train(PATH)
