### 题目复述

**1. 用 Householder 变换将矩阵 $A = \begin{bmatrix} 1 & -4 \\ 2 & 3 \\ 2 & 2 \end{bmatrix}$ 进行完全 QR 分解和约化 QR 分解。（20分）**

### 注意：

| 分解类型          |  原矩阵 $A$  |      矩阵 $Q$ (正交部分)       |   矩阵 $R$ (上三角部分)   |
| :---------------- | :----------: | :----------------------------: | :-----------------------: |
| **方阵**          | $n \times n$ |          $n \times n$          |       $n \times n$        |
| **非方阵 (完全)** | $m \times n$ |   **$m \times m$** (大方阵)    | **$m \times n$** (带零行) |
| **非方阵 (约化)** | $m \times n$ | **$m \times n$** (同 $A$ 大小) | **$n \times n$** (小方阵) |

---

### 题解

我们需要找到正交矩阵 $Q$ 和上三角矩阵 $R$，使得 $A = QR$。

#### 第一步：构建第一个 Householder 矩阵 $H_1$

目标是将矩阵 $A$ 的第一列 $[1, 2, 2]^T$ 变换为 $[*, 0, 0]^T$ 的形式。

1.  **选取向量 $x$**：
    $x = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix}$

2.  **计算范数 $\|x\|_2$**：
    $\|x\|_2 = \sqrt{1^2 + 2^2 + 2^2} = \sqrt{9} = 3$

3.  **构造 Householder 向量 $v$**：
    为了数值稳定性（避免对消），我们选择 $v = x - \alpha e_1$，其中 $\alpha = -sign(x_1)\|x\|_2$。
    这里 $x_1 = 1 > 0$，所以 $\alpha = -3$。
    $v = x - (-3)e_1 = \begin{bmatrix} 1 \\ 2 \\ 2 \end{bmatrix} + \begin{bmatrix} 3 \\ 0 \\ 0 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \\ 2 \end{bmatrix}$
    为简化计算，提取公因子（不影响 Householder 矩阵），令 $u = \begin{bmatrix} 2 \\ 1 \\ 1 \end{bmatrix}$。

4.  **计算 $H_1$**：
    $H_1 = I - 2 \frac{uu^T}{u^Tu}$
    $u^Tu = 2^2 + 1^2 + 1^2 = 6$
    $H_1 = I - \frac{2}{6} \begin{bmatrix} 2 \\ 1 \\ 1 \end{bmatrix} \begin{bmatrix} 2 & 1 & 1 \end{bmatrix} = I - \frac{1}{3} \begin{bmatrix} 4 & 2 & 2 \\ 2 & 1 & 1 \\ 2 & 1 & 1 \end{bmatrix}$
    $H_1 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{bmatrix} - \begin{bmatrix} 4/3 & 2/3 & 2/3 \\ 2/3 & 1/3 & 1/3 \\ 2/3 & 1/3 & 1/3 \end{bmatrix} = \begin{bmatrix} -1/3 & -2/3 & -2/3 \\ -2/3 & 2/3 & -1/3 \\ -2/3 & -1/3 & 2/3 \end{bmatrix}$

5.  **计算 $A^{(1)} = H_1 A$**：
    $A^{(1)} = \begin{bmatrix} -1/3 & -2/3 & -2/3 \\ -2/3 & 2/3 & -1/3 \\ -2/3 & -1/3 & 2/3 \end{bmatrix} \begin{bmatrix} 1 & -4 \\ 2 & 3 \\ 2 & 2 \end{bmatrix} = \begin{bmatrix} -3 & -2 \\ 0 & 4 \\ 0 & 3 \end{bmatrix}$
    *(注：第一列变为 $[-3, 0, 0]^T$，第二列计算：$Row1: (-1/3)(-4)+(-2/3)(3)+(-2/3)(2) = -2$; $Row2: (-2/3)(-4)+(2/3)(3)+(-1/3)(2) = 4$; $Row3: (-2/3)(-4)+(-1/3)(3)+(2/3)(2) = 3$)*

#### 第二步：构建第二个 Householder 矩阵 $H_2$

目标是将 $A^{(1)}$ 第二列对角线以下的元素归零。也就是处理子向量 $[4, 3]^T$。

1.  **选取子向量 $x'$**：
    $x' = \begin{bmatrix} 4 \\ 3 \end{bmatrix}$

2.  **计算范数 $\|x'\|_2$**：
    $\|x'\|_2 = \sqrt{4^2 + 3^2} = 5$

3.  **构造 Householder 向量 $v'$**：
    取 $\alpha = -sign(4) \times 5 = -5$。
    $v' = \begin{bmatrix} 4 \\ 3 \end{bmatrix} - \begin{bmatrix} -5 \\ 0 \end{bmatrix} = \begin{bmatrix} 9 \\ 3 \end{bmatrix}$
    简化向量 $u' = \begin{bmatrix} 3 \\ 1 \end{bmatrix}$。

4.  **构造 $\tilde{H}_2$ 和 $H_2$**：
    $u'^T u' = 3^2 + 1^2 = 10$
    $\tilde{H}_2 = I_2 - \frac{2}{10} \begin{bmatrix} 3 \\ 1 \end{bmatrix} \begin{bmatrix} 3 & 1 \end{bmatrix} = I_2 - \frac{1}{5} \begin{bmatrix} 9 & 3 \\ 3 & 1 \end{bmatrix} = \begin{bmatrix} 1-1.8 & -0.6 \\ -0.6 & 1-0.2 \end{bmatrix} = \begin{bmatrix} -4/5 & -3/5 \\ -3/5 & 4/5 \end{bmatrix}$
    扩充为 $3 \times 3$ 矩阵：
    $H_2 = \begin{bmatrix} 1 & 0 & 0 \\ 0 & -4/5 & -3/5 \\ 0 & -3/5 & 4/5 \end{bmatrix}$

5.  **计算 $R = H_2 A^{(1)}$**：
    $R = \begin{bmatrix} 1 & 0 & 0 \\ 0 & -4/5 & -3/5 \\ 0 & -3/5 & 4/5 \end{bmatrix} \begin{bmatrix} -3 & -2 \\ 0 & 4 \\ 0 & 3 \end{bmatrix} = \begin{bmatrix} -3 & -2 \\ 0 & -5 \\ 0 & 0 \end{bmatrix}$

#### 第三步：计算 $Q$

$Q = H_1^T H_2^T = H_1 H_2$ （因为 Householder 矩阵是对称且正交的）。

$Q = \begin{bmatrix} -1/3 & -2/3 & -2/3 \\ -2/3 & 2/3 & -1/3 \\ -2/3 & -1/3 & 2/3 \end{bmatrix} \begin{bmatrix} 1 & 0 & 0 \\ 0 & -4/5 & -3/5 \\ 0 & -3/5 & 4/5 \end{bmatrix}$

进行矩阵乘法：
- 第一列：保持 $H_1$ 第一列不变 $\to \begin{bmatrix} -1/3 \\ -2/3 \\ -2/3 \end{bmatrix}$
- 第二列：$(-4/5) \cdot (H_1 \text{第2列}) + (-3/5) \cdot (H_1 \text{第3列}) \to \begin{bmatrix} 14/15 \\ -1/3 \\ -2/15 \end{bmatrix}$
- 第三列：$(-3/5) \cdot (H_1 \text{第2列}) + (4/5) \cdot (H_1 \text{第3列}) \to \begin{bmatrix} -2/15 \\ -2/3 \\ 11/15 \end{bmatrix}$

即：
$Q = \begin{bmatrix} -1/3 & 14/15 & -2/15 \\ -2/3 & -1/3 & -2/3 \\ -2/3 & -2/15 & 11/15 \end{bmatrix}$

---

### 最终结果

#### 1. 完全 QR 分解
$$A = QR$$
$$Q = \begin{bmatrix} -1/3 & 14/15 & -2/15 \\ -2/3 & -1/3 & -2/3 \\ -2/3 & -2/15 & 11/15 \end{bmatrix}, \quad R = \begin{bmatrix} -3 & -2 \\ 0 & -5 \\ 0 & 0 \end{bmatrix}$$

#### 2. 约化 QR 分解 (Thin QR)
取 $Q$ 的前 2 列和 $R$ 的前 2 行：
$$A = Q_1 R_1$$
$$Q_1 = \begin{bmatrix} -1/3 & 14/15 \\ -2/3 & -1/3 \\ -2/3 & -2/15 \end{bmatrix}, \quad R_1 = \begin{bmatrix} -3 & -2 \\ 0 & -5 \end{bmatrix}$$