from PIL import Image
import torch
import torch.nn as nn
from torchvision import models, transforms


class Predictor:
    def __init__(self, model_file: str, input_size: int):
        self._set_model(model_file)
        self._set_transform(input_size)

    def _set_model(self, model_file: str):
        def set_parameter_requires_grad(model, feature_extracting):
            if feature_extracting:
                for param in model.parameters():
                    param.requires_grad = False

        device = torch.device("cpu")
        self._model = models.squeezenet1_0(pretrained=True)
        set_parameter_requires_grad(self._model, True)
        self._model.classifier[1] = nn.Conv2d(
            512, 2,
            kernel_size=(1, 1),
            stride=(1, 1)
        )
        self._model.num_classes = 2
        self._model.load_state_dict(
            torch.load(model_file, map_location=device)
        )
        self._model.eval()

    def _set_transform(self, input_size: int):
        self._transform = transforms.Compose([
            transforms.Resize(input_size),
            transforms.CenterCrop(input_size),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, input_file: str) -> (int, list):
        im = Image.open(input_file)
        data = torch.stack([self._transform(im)])

        outputs = self._model(data)
        probs = nn.Softmax()(outputs)
        _, preds = torch.max(probs, 1)

        return preds.numpy()[0], probs.tolist()
