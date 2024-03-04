import torch
from torch.utils.data import DataLoader
from data_loader_test import SoundDS
from Model import AudioClassifier


def load_model(model_path):
    model = AudioClassifier()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


test_data_path = 'Samples/Orka_test'
model_path = 'audio_classifier_weights.pth'
input_data = SoundDS(test_data_path)
valid_dl = torch.utils.data.DataLoader(input_data, batch_size=8, shuffle=True)


def test_model(model, input_data):
    correct = 0
    total = 0
    with torch.no_grad():
        for data in input_data:
            inputs, labels = data[0], data[1]
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy of the model on the test audio files: {100 * correct / total}%')


model = load_model(model_path)
test_model(model, valid_dl)
