### 12thJune Note
## reference：https://github.com/lucidrains/vit-pytorch/blob/main/vit_pytorch/vit_1d.py


# 🌟 Vision Transformer (ViT) 结构与实现笔记

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

---
