import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import torch
from torch import nn

class AlexNet(nn.Module):
    def __init__(self, num_classes=10):
        super(AlexNet, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 48, kernel_size=5, stride=4),  # [1, 3, 224, 224] → [1, 48, 55, 55]
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),               # → [1, 48, 27, 27]

            nn.Conv2d(48, 128, kernel_size=3),          # → [1, 128, 25, 25]
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2),               # → [1, 128, 12, 12]

            nn.Conv2d(128, 192, kernel_size=3),         # → [1, 192, 10, 10]
            nn.ReLU(inplace=True),

            nn.Conv2d(192, 192, kernel_size=3),         # → [1, 192, 8, 8]
            nn.ReLU(inplace=True),

            nn.MaxPool2d(kernel_size=2)                # → [1, 192, 4, 4]
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),                              # → [1, 192 * 4 * 4] = [1, 3072]
            nn.Linear(192 * 4 * 4, 2048),
            nn.ReLU(inplace=True),
            nn.Linear(2048, 1024),
            nn.ReLU(inplace=True),
            nn.Linear(1024, num_classes)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

if __name__ == '__main__':
    x = torch.rand(1, 3, 224, 224)
    model = AlexNet(num_classes=10)
    y = model(x)
    print(y.shape)  # 应输出: torch.Size([1, 10])
