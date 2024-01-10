import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
from torchvision import models
from model import get_data_loaders

num_classes = 838

def preprocess(image: Image):
    transform = transforms.Compose([
        transforms.Resize((64, 64)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image = transform(image).unsqueeze(0) # add batch dimension
    return image


def predict(image: Image, model_path: str='best_model.pth'):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, num_classes)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)

    model.eval()
    train_dataloader, _ = get_data_loaders()
    class_to_idx = train_dataloader.dataset.class_to_idx
    image = preprocess(image)
    image = image.to(device)
    with torch.no_grad():
        outputs = model(image)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        probability, class_idx = probabilities.topk(1)
        print(class_idx, probability)

    idx_to_class = {v: k for k, v in class_to_idx.items()}
    predicted_class = idx_to_class[class_idx.item()]

    return predicted_class, probability.item()

def predict_by_path(image_path: str, model_path: str):
    image = Image.open(image_path)
    return predict(image, model_path)

def main():
    image_path = '../../data/predict/eksdistro2.png'
    model_path = 'best_model.pth'
    predicted_class, probability = predict_by_path(image_path, model_path)
    print(f'Predicted Class: {predicted_class}, Probability: {probability:.4f}')

if __name__ == "__main__":
    main()