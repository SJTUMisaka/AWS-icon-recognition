import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models
from dataloader import get_data_loaders

train_loader, test_loader = get_data_loaders()
num_classes = 838
num_epochs = 300 

# Use pretrained resnet
model = models.resnet18(pretrained=True)

# Make output layer suit our data
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)

# Define loss func and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

best_acc = 0.0
best_model_wts = model.state_dict()

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)
        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    epoch_loss = running_loss / len(train_loader)
    print(f"Epoch {epoch+1}/{num_epochs}, Training loss: {epoch_loss}")

    model.eval()
    running_corrects = 0
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)

            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            running_corrects += torch.sum(preds == labels.data)

    epoch_acc = running_corrects.double() / len(test_loader.dataset)
    print(f"Epoch {epoch+1}/{num_epochs}, Validation Accuracy: {epoch_acc}")

    # save best model
    if epoch_acc > best_acc:
        best_acc = epoch_acc
        best_model_wts = model.state_dict()
        torch.save(best_model_wts, 'best_model.pth')

print("Training complete")
