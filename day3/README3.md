# 12th June Note
## 1. 数据准备阶段

### ✅ 文件：`deal_with_datasets.py`
- **作用**：将原始图片划分为 `train/` 和 `val/` 子目录（按照比例随机划分）。
- **命令**：
  ```bash
  python deal_with_datasets.py
  ```
- **输出结构**：
  ```
  image2/train/class_x/*.jpg
  image2/val/class_x/*.jpg
  ```
- **用途**：为后续训练和验证集制作数据目录结构。

---

### ✅ 文件：`prepare.py`
- **作用**：生成训练集和验证集的索引文件 `train.txt` 和 `val.txt`，每行包含图片相对路径和类别标签。
- **命令**：
  ```bash
  python prepare.py
  ```
- **输出**：
  ```
  train.txt / val.txt
  # 文件内容示例：
  class1/img001.jpg 0
  class2/img045.jpg 1
  ```
- **用途**：供 PyTorch 自定义 Dataset 类读取，构建训练集和验证集。

---

## 2. 模型定义阶段

### ✅ 文件：`vit_model.py`
- **作用**：定义 Vision Transformer (ViT) 模型结构，包括：
  - `PatchEmbedding`（图像切分成 patch）
  - `Multi-head Attention`（多头注意力）
  - `Transformer Encoder`（编码器堆）
  - `MLP` 分类头
- **用途**：被 `train.py` 导入并实例化为训练模型。

---

## 3. 模型训练阶段

### ✅ 文件：`train.py`
- **作用**：
  - 加载训练集和验证集（使用 `train.txt` / `val.txt`）
  - 初始化 ViT 模型
  - 执行训练和验证过程
  - 输出 Loss 和 Accuracy
- **命令**：
  ```bash
  python train.py
  ```
- **输出示例**：
  ```
  [Epoch 1] Loss: 2075.35, Accuracy: 28.53%
  Validation Accuracy: 35.67%
  ```
- **用途**：训练 ViT 模型，并评估其在验证集上的表现。

---

## 📁 文件一：图像版 ViT 实现（以 2D 图像为输入）

### 🔧 架构说明

#### PatchEmbedding
- 功能：将图像分割为 patch 并展开为向量，再投影到 `dim` 维。
- 输入尺寸：`[B, 3, H, W]`
- 输出尺寸：`[B, N_patches, dim]`
- 实现方式：
  ```python
  Rearrange('b c (h p1) (w p2) -> b (h w) (p1 p2 c)', p1=patch_size, p2=patch_size)
  ```

#### Attention
- 功能：实现多头自注意力机制。
- 特点：
  - QKV 全部由一个线性层得到。
  - 使用 `einops` 处理维度，增强可读性。

#### Transformer
- 组成：
  - 多个 encoder block（每个含 LayerNorm + Attention + FeedForward）
  - 残差连接和 LayerNorm 顺序与标准 Transformer 一致（Post-LN）。

#### ViT 主类
- 输入：图像张量 `[B, 3, 256, 256]`
- 步骤：
  1. Patch 嵌入。
  2. 加入分类 token `cls_token`。
  3. 加上位置编码 `pos_embedding`。
  4. Transformer 编码。
  5. 分类头输出预测。

### 🧪 示例用法
```python
model = ViT(image_size=256, patch_size=16, num_classes=100, ...)
img = torch.randn(1, 3, 256, 256)
logits = model(img)  # 输出 [1, 100]
```

---

## 📁 文件二：一维时间序列版 ViT 实现（用于 1D 信号）

### 📌 输入结构
- 输入 shape：`[B, C, L]`，例如 `[4, 3, 256]`
- 将一维信号划分为 `patch_size` 长度的片段。
- 每个 patch 是 `[patch_size × C]`，后接 Linear 映射到 `dim`。

### 🔧 PatchEmbedding（时间序列版）
```python
Rearrange('b c (n p) -> b n (p c)', p=patch_size)
```

### 🔄 分类 Token 拼接方式
- 由于输入是序列，分类 token 是 `[dim]`，直接通过 `repeat` 扩展为 `[B, dim]`。
- 使用 `einops.pack` 和 `unpack` 来组合和提取分类 token。

### 🧠 Transformer 与 FeedForward
结构与图像版本一致。

### ✅ 输出
返回 `[B, num_classes]` 的 logits 预测。

