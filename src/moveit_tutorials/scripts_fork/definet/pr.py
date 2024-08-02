import random
import torch

error = torch.arange(70).reshape(10,7)
print(error)

# 0.001より小さいインデックスを削除
# condition = torch.all(torch.abs(error) < 0.005, dim=1)
condition = torch.all(torch.cat([torch.abs(error[:, :3]) > 10, torch.abs(error[:, 3:]) < 40], dim=1), dim=1)
print(condition)