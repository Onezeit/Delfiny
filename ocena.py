import torch
from torch.utils.data import DataLoader
from data_loader import SoundDS
from Model import AudioClassifier

model_path = 'Modele/4_epoch/GPT/GPT.pth'
test_data_path = ['Samples/Humbak_test']
data = SoundDS(test_data_path)
valid_dl = DataLoader(data, batch_size=1, shuffle=False)


def load_model(model_path):
    model = AudioClassifier()
    model.load_state_dict(torch.load(model_path))
    model.eval()
    return model


def predict_with_confidence_threshold(outputs, threshold=0.7):
    probabilities = torch.softmax(outputs, dim=1)
    max_probs, predictions = torch.max(probabilities, dim=1)
    uncertain = max_probs < threshold
    predictions[uncertain] = 2
    return predictions, max_probs


def test_model(model, input_data):
    correct = 0
    total = 0
    with torch.no_grad():
        for i, data in enumerate(input_data):
            inputs, labels, filenames = data
            if inputs.nelement() == 0:
                continue
            outputs = model(inputs)
            predicted, prob = predict_with_confidence_threshold(outputs)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            label = labels.item()
            predicted_label = predicted.item()
            print(f"File: {filenames[0]}, True label: {label}, Predicted label: {predicted_label}, Probability: {prob.item():.4f}")
    accuracy = 100 * correct / total
    print(f'Accuracy: {accuracy:.2f}%')


model = load_model(model_path)
test_model(model, valid_dl)
