import cv2
import numpy as np
import torch

from .backbones import get_model


def test():
    print("test feature extraction")


@torch.no_grad()
class FeatureExtraction(object):
    def __init__(self, network, weight, use_cuda=True):
        self.network = network
        self.weight = weight
        self.use_cuda = use_cuda
        if self.use_cuda == True:
            self.cpu = False
        else:
            self.cpu = True

        self.net = get_model(self.network, fp16=False)
        self.net.load_state_dict(
            torch.load(
                self.weight,
                torch.device("cpu" if self.cpu else "cuda"),
            )
        )
        self.net.eval()

    def face_encodings(self, image):
        h, w, _ = image.shape
        if h != 112 or w != 112:
            img = cv2.resize(image, (112, 112))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.transpose(img, (2, 0, 1))
        img = torch.from_numpy(img).unsqueeze(0).float()
        img.div_(255).sub_(0.5).div_(0.5)
        try:
            features = self.net(img).numpy()
        except:
            features = self.net(img).detach().numpy()
        return features
