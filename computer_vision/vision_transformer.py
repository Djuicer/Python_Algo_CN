"""
用于图像分类的视觉 Transformer（Vision Transformer，ViT）

本模块实现以下论文所述的视觉 Transformer 架构：
"An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale"
Dosovitskiy 等人（2020）

Paper: https://arxiv.org/abs/2010.11929

视觉 Transformer 将图像划分为固定大小的图块，对每个图块进行线性嵌入，
加入位置嵌入，再将所得向量序列送入标准 Transformer 编码器。
执行分类时，会在序列前添加一个可学习的分类标记。

Author: devvratpathak
"""

import numpy as np


def create_patches(
    image: np.ndarray, patch_size: int = 16
) -> tuple[np.ndarray, tuple[int, int]]:
    """
    将图像划分为互不重叠的图块。

    参数：
        image: 形状为 (height, width, channels) 的输入图像数组
        patch_size: 每个正方形图块的大小（默认值：16）

    返回：
        A tuple containing:
        - patches: 形状为 (num_patches, patch_size, patch_size, channels) 的数组
        - grid_size: 表示网格的元组 (height_patches, width_patches)

    示例：
        >>> img = np.random.rand(32, 32, 3)
        >>> patches, grid = create_patches(img, patch_size=16)
        >>> patches.shape
        (4, 16, 16, 3)
        >>> grid
        (2, 2)

        >>> img = np.random.rand(224, 224, 3)
        >>> patches, grid = create_patches(img, patch_size=16)
        >>> patches.shape
        (196, 16, 16, 3)
        >>> grid
        (14, 14)
    """
    if len(image.shape) != 3:
        msg = f"Expected 3D image, got shape {image.shape}"
        raise ValueError(msg)

    height, width, channels = image.shape

    if height % patch_size != 0 or width % patch_size != 0:
        msg = (
            f"Image dimensions ({height}x{width}) must be divisible by "
            f"patch_size ({patch_size})"
        )
        raise ValueError(msg)

    # 计算各维度的图块数量
    num_patches_h = height // patch_size
    num_patches_w = width // patch_size

    # 将图像重塑为图块
    patches = image.reshape(
        num_patches_h, patch_size, num_patches_w, patch_size, channels
    )
    # 转置以得到图块序列
    patches = patches.transpose(0, 2, 1, 3, 4)
    # 重塑为 (num_patches, patch_size, patch_size, channels)
    patches = patches.reshape(-1, patch_size, patch_size, channels)

    return patches, (num_patches_h, num_patches_w)


def patch_embedding(patches: np.ndarray, embedding_dim: int = 768) -> np.ndarray:
    """
    将展平后的图块线性投影到嵌入维度。

    参数：
        patches: 图块数组，形状为
            (num_patches, patch_size, patch_size, channels)
        embedding_dim: 嵌入空间维度（默认值：768）

    返回：
        形状为 (num_patches, embedding_dim) 的嵌入图块

    示例：
        >>> patches = np.random.rand(4, 16, 16, 3)
        >>> embeddings = patch_embedding(patches, embedding_dim=768)
        >>> embeddings.shape
        (4, 768)

        >>> patches = np.random.rand(196, 16, 16, 3)
        >>> embeddings = patch_embedding(patches, embedding_dim=512)
        >>> embeddings.shape
        (196, 512)
    """
    num_patches = patches.shape[0]
    # 展平每个图块
    flattened = patches.reshape(num_patches, -1)

    # 线性投影（简化实现；实际应用中这是学习得到的权重矩阵）
    # 此处使用随机投影进行演示
    patch_dim = flattened.shape[1]
    rng = np.random.default_rng()
    projection_matrix = rng.standard_normal((patch_dim, embedding_dim)) * 0.02

    embedded = flattened @ projection_matrix

    return embedded


def add_positional_encoding(
    embeddings: np.ndarray, num_positions: int | None = None
) -> np.ndarray:
    """
    向图块嵌入添加可学习的位置编码。

    参数：
        embeddings: 形状为 (num_patches, embedding_dim) 的嵌入图块
        num_positions: 位置数量（若为 None，则为 CLS 标记使用 num_patches + 1）

    返回：
        形状为 (num_positions, embedding_dim) 的带位置编码嵌入

    示例：
        >>> embeddings = np.random.rand(4, 768)
        >>> pos_embeddings = add_positional_encoding(embeddings)
        >>> pos_embeddings.shape
        (5, 768)

        >>> embeddings = np.random.rand(196, 512)
        >>> pos_embeddings = add_positional_encoding(embeddings)
        >>> pos_embeddings.shape
        (197, 512)
    """
    num_patches, embedding_dim = embeddings.shape

    if num_positions is None:
    # 为 CLS 标记加 1
        num_positions = num_patches + 1

    # 创建可学习的位置编码（简化实现；通常由训练获得）
    rng = np.random.default_rng()
    positional_encodings = rng.standard_normal((num_positions, embedding_dim)) * 0.02

    # 在序列前添加 CLS 标记
    cls_token = rng.standard_normal((1, embedding_dim)) * 0.02

    # 将 CLS 标记与图块嵌入连接
    embeddings_with_cls = np.vstack([cls_token, embeddings])

    # 添加位置编码
    embeddings_with_pos = embeddings_with_cls + positional_encodings

    return embeddings_with_pos


def attention_mechanism(
    query: np.ndarray,
    key: np.ndarray,
    value: np.ndarray,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """
    计算缩放点积注意力。

    Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V

    参数：
        query: 形状为 (seq_len, d_k) 的查询矩阵
        key: 形状为 (seq_len, d_k) 的键矩阵
        value: 形状为 (seq_len, d_v) 的值矩阵
        mask: 可选的注意力掩码

    返回：
        A tuple containing:
        - output: 形状为 (seq_len, d_v) 的注意力输出
        - attention_weights: 形状为 (seq_len, seq_len) 的注意力权重

    示例：
        >>> q = np.random.rand(10, 64)
        >>> k = np.random.rand(10, 64)
        >>> v = np.random.rand(10, 64)
        >>> output, weights = attention_mechanism(q, k, v)
        >>> output.shape
        (10, 64)
        >>> weights.shape
        (10, 10)
        >>> np.allclose(weights.sum(axis=1), 1.0)
        True
    """
    d_k = query.shape[-1]

    # 计算注意力分数：QK^T / sqrt(d_k)
    scores = query @ key.T / np.sqrt(d_k)

    # 若提供了掩码，则应用掩码
    if mask is not None:
        scores = np.where(mask, scores, -1e9)

    # 应用 softmax 得到注意力权重
    exp_scores = np.exp(scores - np.max(scores, axis=-1, keepdims=True))
    attention_weights = exp_scores / np.sum(exp_scores, axis=-1, keepdims=True)

    # 计算值的加权和
    output = attention_weights @ value

    return output, attention_weights


def layer_norm(embeddings: np.ndarray, epsilon: float = 1e-6) -> np.ndarray:
    """
    应用层归一化（Layer Normalization）。

    参数：
        embeddings: 形状为 (seq_len, embedding_dim) 的输入数组
        epsilon: 用于保证数值稳定性的小常数（默认值：1e-6）

    返回：
        与输入形状相同的归一化数组

    示例：
        >>> embeddings = np.random.rand(10, 768)
        >>> normalized = layer_norm(embeddings)
        >>> normalized.shape
        (10, 768)
        >>> np.allclose(normalized.mean(axis=1), 0.0, atol=1e-6)
        True
        >>> np.allclose(normalized.std(axis=1), 1.0, atol=1e-6)
        True
    """
    mean = embeddings.mean(axis=-1, keepdims=True)
    std = embeddings.std(axis=-1, keepdims=True)
    return (embeddings - mean) / (std + epsilon)


def feedforward_network(embeddings: np.ndarray, hidden_dim: int = 3072) -> np.ndarray:
    """
    应用逐位置前馈网络。

    FFN(x) = max(0, xW1 + b1)W2 + b2

    参数：
        embeddings: 形状为 (seq_len, embedding_dim) 的输入数组
        hidden_dim: 隐藏维度大小（默认值：3072，通常为 embedding_dim 的 4 倍）

    返回：
        形状为 (seq_len, embedding_dim) 的输出数组

    示例：
        >>> embeddings = np.random.rand(10, 768)
        >>> output = feedforward_network(embeddings, hidden_dim=3072)
        >>> output.shape
        (10, 768)

        >>> embeddings = np.random.rand(197, 512)
        >>> output = feedforward_network(embeddings, hidden_dim=2048)
        >>> output.shape
        (197, 512)
    """
    embedding_dim = embeddings.shape[1]
    rng = np.random.default_rng()

    # 第一个线性层
    w1 = rng.standard_normal((embedding_dim, hidden_dim)) * 0.02
    b1 = np.zeros(hidden_dim)
    hidden = embeddings @ w1 + b1

    # GELU 激活函数（近似实现）
    gelu_factor = np.sqrt(2 / np.pi) * (hidden + 0.044715 * hidden**3)
    hidden = 0.5 * hidden * (1 + np.tanh(gelu_factor))

    # 第二个线性层
    w2 = rng.standard_normal((hidden_dim, embedding_dim)) * 0.02
    b2 = np.zeros(embedding_dim)
    output = hidden @ w2 + b2

    return output


def transformer_encoder_block(
    embeddings: np.ndarray,
    num_heads: int = 12,  # noqa: ARG001
    hidden_dim: int = 3072,
) -> np.ndarray:
    """
    应用单个 Transformer 编码器块。

    该编码器块包括：
    1. 带残差连接和层归一化的多头自注意力
    2. 带残差连接和层归一化的前馈网络

    参数：
        embeddings: 形状为 (seq_len, embedding_dim) 的输入数组
        num_heads: 注意力头数量（默认值：12，为保持 API 而保留）
        hidden_dim: FFN 的隐藏维度（默认值：3072）

    返回：
        形状为 (seq_len, embedding_dim) 的输出数组

    示例：
        >>> embeddings = np.random.rand(197, 768)
        >>> output = transformer_encoder_block(
        ...     embeddings, num_heads=12, hidden_dim=3072
        ... )
        >>> output.shape
        (197, 768)

        >>> embeddings = np.random.rand(50, 512)
        >>> output = transformer_encoder_block(
        ...     embeddings, num_heads=8, hidden_dim=2048
        ... )
        >>> output.shape
        (50, 512)
    """
    # 多头自注意力（简化实现；使用单个注意力头进行演示）
    # 实际应用中会拆分为多个注意力头
    # 保留 num_heads 参数以保持 API 兼容性
    attention_output, _ = attention_mechanism(embeddings, embeddings, embeddings)

    # 添加残差连接并应用层归一化
    embeddings = layer_norm(embeddings + attention_output)

    # 前馈网络
    ffn_output = feedforward_network(embeddings, hidden_dim)

    # 添加残差连接并应用层归一化
    embeddings = layer_norm(embeddings + ffn_output)

    return embeddings


def vision_transformer(
    image: np.ndarray,
    patch_size: int = 16,
    embedding_dim: int = 768,
    num_layers: int = 12,
    num_heads: int = 12,
    hidden_dim: int = 3072,
    num_classes: int = 1000,
) -> np.ndarray:
    """
    应用视觉 Transformer 进行图像分类。

    架构：
    1. 将图像划分为图块
    2. 对展平后的图块进行线性投影
    3. 添加位置嵌入
    4. 通过 Transformer 编码器层
    5. 提取 CLS 标记并应用分类头

    参数：
        image: 形状为 (height, width, channels) 的输入图像数组
        patch_size: 每个图块的大小（默认值：16）
        embedding_dim: 嵌入维度（默认值：768）
        num_layers: Transformer 层数（默认值：12）
        num_heads: 注意力头数量（默认值：12）
        hidden_dim: FFN 的隐藏维度（默认值：3072）
        num_classes: 输出类别数量（默认值：1000）

    返回：
        形状为 (num_classes,) 的类别 logits

    示例：
        >>> img = np.random.rand(224, 224, 3)
        >>> logits = vision_transformer(img, patch_size=16, num_classes=10)
        >>> logits.shape
        (10,)

        >>> img = np.random.rand(32, 32, 3)
        >>> logits = vision_transformer(
        ...     img, patch_size=16, embedding_dim=512, num_layers=6, num_classes=100
        ... )
        >>> logits.shape
        (100,)
    """
    # 步骤 1：创建图块
    patches, _ = create_patches(image, patch_size)

    # 步骤 2：嵌入图块
    embeddings = patch_embedding(patches, embedding_dim)

    # 步骤 3：添加位置编码（包括 CLS 标记）
    embeddings = add_positional_encoding(embeddings)

    # 步骤 4：通过 Transformer 编码器层
    for _ in range(num_layers):
        embeddings = transformer_encoder_block(embeddings, num_heads, hidden_dim)

    # 步骤 5：提取 CLS 标记（第一个标记）
    cls_token = embeddings[0]

    # 步骤 6：分类头（线性层）
    rng = np.random.default_rng()
    classifier_weights = rng.standard_normal((embedding_dim, num_classes)) * 0.02
    classifier_bias = np.zeros(num_classes)
    logits = cls_token @ classifier_weights + classifier_bias

    return logits


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # 使用示例
    print("Vision Transformer Example")
    print("=" * 50)

    # 创建示例图像（ImageNet 风格输入为 224x224x3）
    rng = np.random.default_rng()
    sample_image = rng.random((224, 224, 3))
    print(f"Input image shape: {sample_image.shape}")

    # 应用视觉 Transformer
    logits = vision_transformer(
        sample_image,
        patch_size=16,
        embedding_dim=768,
        num_layers=12,
        num_heads=12,
        hidden_dim=3072,
        num_classes=1000,
    )

    print(f"Output logits shape: {logits.shape}")
    print(f"Predicted class: {np.argmax(logits)}")

    # 演示图块创建
    print("\n" + "=" * 50)
    print("Patch Creation Example")
    patches, grid = create_patches(sample_image, patch_size=16)
    print(f"Number of patches: {patches.shape[0]}")
    print(f"Patch size: {patches.shape[1:3]}")
    print(f"Grid size: {grid}")
