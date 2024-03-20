from Model import AudioClassifier
import torch
import torch.nn as nn
from data_loader import SoundDS
from torch.utils.data import DataLoader, Dataset, random_split
import pandas as pd
import os


data_paths = ['Samples/Train_Orka', 'Samples/Train_Humbak']
myds = SoundDS(data_paths)

num_items = len(myds)
num_train = round(num_items * 0.8)
num_val = num_items - num_train
train_ds, val_ds = random_split(myds, [num_train, num_val])

train_dl = DataLoader(train_ds, batch_size=8, shuffle=True)
val_dl = DataLoader(val_ds, batch_size=8, shuffle=False)

myModel = AudioClassifier()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
myModel = myModel.to(device)
next(myModel.parameters()).device


def validate(model, dataloader):
    model.eval()
    running_loss = 0.0
    correct_prediction = 0
    total_prediction = 0
    criterion = nn.CrossEntropyLoss()

    with torch.no_grad():
        for data in dataloader:
            inputs, labels = data[0].float().to(device), data[1].to(device)

            inputs_m, inputs_s = inputs.mean(), inputs.std()
            if inputs_s > 0:
                inputs = (inputs - inputs_m) / inputs_s

            outputs = model(inputs)
            loss = criterion(outputs, labels)

            running_loss += loss.item()
            _, prediction = torch.max(outputs, 1)
            correct_prediction += (prediction == labels).sum().item()
            total_prediction += labels.size(0)

    avg_loss = running_loss / len(dataloader)
    accuracy = correct_prediction / total_prediction
    print(f'Validation Loss: {avg_loss:.2f}, Validation Accuracy: {accuracy:.2f}')
    model.train()


def training(model, train_dl, val_dl, num_epochs):
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)
    scheduler = torch.optim.lr_scheduler.OneCycleLR(optimizer, max_lr=0.001,
                                                    steps_per_epoch=int(len(train_dl)),
                                                    epochs=num_epochs,
                                                    anneal_strategy="linear")

    for epoch in range(num_epochs):
        running_loss = 0.0
        correct_prediction = 0
        total_prediction = 0

        for i, data in enumerate(train_dl):
            inputs, labels = data[0].float(), data[1]

            inputs_m, inputs_s = inputs.mean(), inputs.std()
            if inputs_s > 0:
                inputs = (inputs - inputs_m) / inputs_s
            optimizer.zero_grad()

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            scheduler.step()

            running_loss += loss.item()

            _, prediction = torch.max(outputs, 1)
            correct_prediction += (prediction == labels).sum().item()
            total_prediction += prediction.shape[0]

        num_batches = len(train_dl)
        avg_loss = running_loss / num_batches
        acc = correct_prediction / total_prediction
        print(f'Epoch: {epoch}, Running Loss: {running_loss}, Training Loss: {avg_loss:.2f}, Training Accuracy: {acc:.2f}')

        validate(model, val_dl)

    print('Finished Training')


def pth_to_csv(pth_file, csv_file):
    state_dict = torch.load(pth_file, map_location=torch.device('cpu'))

    for key, value in state_dict.items():
        tensor_as_list = value.numpy().flatten().tolist()

        df = pd.DataFrame(tensor_as_list)
        df.to_csv(f"{csv_file}_{key}.csv", index=False)


def save_model(model, path, model_name, num_epochs):
    directory = os.path.join(path, f"{num_epochs}_epoch", model_name)

    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    torch.save(model.state_dict(), os.path.join(directory, f"{model_name}.pth"))


num_epochs = 2
training(myModel, train_dl, val_dl, num_epochs)

model_name = "170/140"
model_path = "Modele"
save_model(myModel, model_path, model_name, num_epochs)

pth_file = os.path.join(model_path, f"{num_epochs}_epoch", model_name, f"{model_name}.pth")
csv_file = os.path.join(model_path, f"{num_epochs}_epoch", model_name, "weights")
pth_to_csv(pth_file, csv_file)
