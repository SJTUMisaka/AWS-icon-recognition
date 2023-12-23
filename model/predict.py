import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from torchvision import models
from dataloader import get_data_loaders

num_classes = 838
model = models.resnet18(pretrained=False)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, num_classes)


model.load_state_dict(torch.load('best_model.pth'))

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)

model.eval()

def preprocess(image_path):
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = transform(image).unsqueeze(0) # add batch dimension
    image = image.to(device)
    return image


def predict(image_path, model, class_to_idx):
    image = preprocess(image_path)
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        probability, class_idx = probabilities.topk(1)
        print(class_idx, probability)

    idx_to_class = {v: k for k, v in class_to_idx.items()}
    predicted_class = idx_to_class[class_idx.item()]

    return predicted_class, probability.item()

image_path = '../../data/predict/eksdistro2.png'
train_dataloader, _ = get_data_loaders()
predicted_class, probability = predict(image_path, model, train_dataloader.dataset.class_to_idx)
print(f'Predicted Class: {predicted_class}, Probability: {probability:.4f}')
