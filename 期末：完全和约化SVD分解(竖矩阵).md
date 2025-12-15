## 考题

给定矩阵 A：
$$ A = \begin{bmatrix} 1 & 1 \\ 1 & 1 \\ 0 & 0 \end{bmatrix} $$

SVD 的基本形式是 **A = UΣVᵀ**，其中：
*   **U** 是一个 m x m 的正交矩阵 (左奇异向量)。
*   **Σ** 是一个 m x n 的对角矩阵，对角线上的元素是奇异值 σ。
*   **V** 是一个 n x n 的正交矩阵 (右奇异向量)。

这里 m=3, n=2。

### SVD分解考场解法 

**目标：** 将矩阵 A (m x n) 分解为 `A = UΣVᵀ`，关键：$AV=U \Sigma$，$VV^T=I$

#### 第0步：如果A是横着的，可以求Aᵀ的SVD分解

如果矩阵 $A$ 的SVD分解是：
$$ A = U \Sigma V^T $$
那么它的转置矩阵 $A^T$ 的SVD分解就是：
$$ A^T = (U \Sigma V^T)^T = (V^T)^T \Sigma^T U^T = V \Sigma^T U^T $$

所以，求出Aᵀ的SVD分解，然后**U、V互换，Σ取转置**，就可以得到A的U、V、Σ。

#### **第一步：求 V 和 Σ₁**

1.  **计算 `B = AᵀA`**。(提示：**AᵀA和AAᵀ的**非零特征值是相同的，所以可以先把**AᵀA和AAᵀ**都求出来放着)
2.  **求 `B` 的特征值 `λ`**，并**从大到小**排列：`λ₁ ≥ λ₂ ≥ ... ≥ λᵣ > 0`，以及 `r` 个之后的零特征值。
3.  **求非零奇异值 `σᵢ = √λᵢ`**。
4.  **构造核心的 $Σ_1$ 矩阵**：
    *   这是一个 `r x r` 的**对角方阵**，对角线元素为 `σ₁`, `σ₂`, ...$σ_r$。
    *   计算它的逆 $Σ_1^{⁻¹}$ (这很简单，只需将对角线元素取倒数即可)。
5.  **求 `V` 矩阵**：
    *   求出所有特征值 `λᵢ` 对应的**单位化**特征向量 `vᵢ`。
    *   将这些 `vᵢ` **按 `λ` 的顺序**作为**列向量**，组成正交矩阵 `V`。
    *   **切分 `V`**：将 `V` 分为两部分，`V = [V₁ | V₂]`。
        *   `V₁` (n x r): 对应**非零**特征值的前 `r` 个列向量。
        *   `V₂` (n x (n-r)): 对应**零**特征值的后 `n-r` 个列向量。

#### **第二步：求 U₁ 和 U₂**

1.  **计算 `U₁` (对应非零奇异值的部分)**：
    *   使用矩阵公式： **`U₁ = AV₁Σ₁⁻¹`**
    *   `U₁` 是一个 `m x r` 的矩阵，它的列向量是标准正交的。

2.  **计算 `U₂` (有多少个0奇异值，U2就含有多少个向量。如果所有奇异值非0，就不需要求U2了)**：
    *   `U₂` 的列向量构成了 `Aᵀ` 的零空间 (`Null(Aᵀ)`) 的一组标准正交基。
    *   **求解方程组 `AAᵀy = 0`**，得到其基础解系。
    *   将这组基础解系**单位正交化** (Gram-Schmidt)，得到的列向量就组成了 `U₂`。
    *   `U₂` 是一个 `m x (m-r)` 的矩阵。

#### **第三步：组装最终结果**

1.  **组合 `U` 矩阵**：
    *   将 `U₁` 和 `U₂` 按列合并：**`U = [U₁ | U₂]`**。
    *   `U` 是一个 `m x m` 的正交矩阵。

2.  **构造最终的 `Σ` 矩阵**：
    *   创建一个 `m x n` 的全零矩阵 (与A同型)。
    *   将奇异值从大到小填在对角线上。

3.  **写出最终答案**：
    *   **完全SVD**：`A = UΣVᵀ`，`A(m x n) = U(m x m) Σ(m x n) Vᵀ(n x n)`。其中U和V都是方阵，Σ和A同形。
    *   **约化SVD** ：移除 $\Sigma$ 中比方阵多出的为0的行或列，并同时移除 $U$ 或 $V$ 中对应的列，具体移除哪一个取决于如何让矩阵乘法可以正常进行。 对于竖矩阵：`A(m x n) = U(m x n) Σ(n x n) Vᵀ(n x n)`。
    *   **截断SVD(k=r)**：`A = U₁Σ₁V₁ᵀ`，等价于约化SVD基础上移除为0的$\sigma_i$，以及对应的$u_i$和$v_i$。`A(m x n) = U(m x r) Σ(r x r) Vᵀ(r x n)`。

### 分解步骤

#### 第 1 步：计算 V 和 Σ

我们首先计算 `AᵀA`：
$$ A^T A = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 1 & 0 \end{bmatrix} \begin{bmatrix} 1 & 1 \\ 1 & 1 \\ 0 & 0 \end{bmatrix} = \begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix} $$

接下来，我们求 `AᵀA` 的特征值 (λ) 和特征向量 (v)。
特征方程为 `det(AᵀA - λI) = 0`：
$$ \det \begin{pmatrix} 2-\lambda & 2 \\ 2 & 2-\lambda \end{pmatrix} = (2-\lambda)^2 - 4 = \lambda^2 - 4\lambda + 4 - 4 = \lambda(\lambda - 4) = 0 $$
解得特征值为 `λ₁ = 4`, `λ₂ = 0`。

奇异值 σ 是特征值的平方根，按降序排列：
*   `σ₁ = √λ₁ = √4 = 2`
*   `σ₂ = √λ₂ = √0 = 0`

现在我们求对应的特征向量：
*   **对于 λ₁ = 4**:
    `(AᵀA - 4I)v = 0`
    $$ \begin{bmatrix} -2 & 2 \\ 2 & -2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} $$
    得到 `-2x + 2y = 0`，即 `x = y`。单位化的特征向量为 **v₁ = [1/√2, 1/√2]ᵀ**。

*   **对于 λ₂ = 0**:
    `(AᵀA - 0I)v = 0`
    $$ \begin{bmatrix} 2 & 2 \\ 2 & 2 \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} $$
    得到 `2x + 2y = 0`，即 `x = -y`。单位化的特征向量为 **v₂ = [1/√2, -1/√2]ᵀ**。

矩阵 **V** 由这些特征向量构成：
$$ V = \begin{bmatrix} v_1 & v_2 \end{bmatrix} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} $$

#### 第 2 步：计算 U

矩阵 **U** 的列向量 uᵢ 可以通过公式 `uᵢ = (1/σᵢ) * A * vᵢ` (对于 σᵢ > 0) 计算。

*   **对于 σ₁ = 2**:
    $$ u_1 = \frac{1}{2} A v_1 = \frac{1}{2} \begin{bmatrix} 1 & 1 \\ 1 & 1 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix} = \frac{1}{2} \begin{bmatrix} 2/\sqrt{2} \\ 2/\sqrt{2} \\ 0 \end{bmatrix} = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \\ 0 \end{bmatrix} $$

*   由于 σ₂ = 0，我们不能用上述公式。U 的剩余列向量 `u₂`, `u₃` 需要构成一个与 `u₁` 正交的标准正交基。
    我们需要找到两个与 `u₁` 正交的单位向量。
    *   一个简单的选择是 **u₂ = [1/√2, -1/√2, 0]ᵀ**，它与 `u₁` 正交 (`u₁ᵀu₂ = 0`) 且是单位向量。
    *   第三个向量 `u₃` 需要与 `u₁` 和 `u₂` 都正交。通过观察或计算可以发现 **u₃ = [0, 0, 1]ᵀ** 满足条件。

所以，矩阵 **U** 为：
$$ U = \begin{bmatrix} u_1 & u_2 & u_3 \end{bmatrix} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \\ 0 & 0 & 1 \end{bmatrix} $$

---

### 三种 SVD 分解结果

现在我们来组装这三种 SVD 分解。

#### 1. 完全 SVD (Full SVD)

在完全 SVD 中，U 是 m x m 矩阵，Σ 是 m x n 矩阵，Vᵀ 是 n x n 矩阵。

*   **U (3x3)**:
    $$ U = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \\ 0 & 0 & 1 \end{bmatrix} $$
*   **Σ (3x2)**:
    $$ \Sigma = \begin{bmatrix} \sigma_1 & 0 \\ 0 & \sigma_2 \\ 0 & 0 \end{bmatrix} = \begin{bmatrix} 2 & 0 \\ 0 & 0 \\ 0 & 0 \end{bmatrix} $$
*   **Vᵀ (2x2)**:
    $$ V^T = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} $$

分解形式为：
$$ A = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix} 2 & 0 \\ 0 & 0 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} $$

#### 2. 约化 SVD (Reduced SVD / Thin SVD)

在约化 SVD 中，我们移除 Σ 矩阵中多余的全零行或列，并相应地调整 U 和 V 的维度，使得 Σ 成为一个方阵。
对于 m > n 的情况，U 变为 m x n，Σ 变为 n x n，Vᵀ 保持 n x n。

*   **U_reduced (3x2)**: (取 U 的前 n 列)
    $$ U_{reduced} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \\ 0 & 0 \end{bmatrix} $$
*   **Σ_reduced (2x2)**: (取 Σ 的前 n 行)
    $$ \Sigma_{reduced} = \begin{bmatrix} 2 & 0 \\ 0 & 0 \end{bmatrix} $$
*   **Vᵀ (2x2)**: (保持不变)
    $$ V^T = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} $$

分解形式为：
$$ A = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \\ 0 & 0 \end{bmatrix} \begin{bmatrix} 2 & 0 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} $$

#### 3. 截断 SVD (Truncated SVD)

截断 SVD 用于数据降维和矩阵近似。我们只保留前 k 个最大的奇异值，其中 `k < rank(A)`。
原矩阵 A 的秩 (rank) 是 1 (因为只有一个非零奇异值)。因此，唯一有意义的截断是 `k=1`。当 `k=1` 时，我们得到对原矩阵的最佳秩-1 近似。在这种特殊情况下，这个近似是完美的，因为它本身就是秩-1 矩阵。

我们取前 k=1 个奇异值、奇异向量：
*   **U₁ (3x1)**: (取 U 的第 1 列)
    $$ U_1 = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \\ 0 \end{bmatrix} $$
*   **Σ₁ (1x1)**: (取 Σ 的左上角 1x1 部分)
    $$ \Sigma_1 = \begin{bmatrix} 2 \end{bmatrix} $$
*   **V₁ᵀ (1x2)**: (取 Vᵀ 的第 1 行)
    $$ V_1^T = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \end{bmatrix} $$

分解形式为 (A₁ 是 A 的秩-1 近似)：
$$ A \approx A_1 = U_1 \Sigma_1 V_1^T = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \\ 0 \end{bmatrix} \begin{bmatrix} 2 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \end{bmatrix} $$
如果我们将其乘开，会发现它精确地重构了原始矩阵 A：
$$ A_1 = \begin{bmatrix} 2/\sqrt{2} \\ 2/\sqrt{2} \\ 0 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \end{bmatrix} = \begin{bmatrix} (2/\sqrt{2})(1/\sqrt{2}) & (2/\sqrt{2})(1/\sqrt{2}) \\ (2/\sqrt{2})(1/\sqrt{2}) & (2/\sqrt{2})(1/\sqrt{2}) \\ 0 & 0 \end{bmatrix} = \begin{bmatrix} 1 & 1 \\ 1 & 1 \\ 0 & 0 \end{bmatrix} = A $$
这说明当 k 等于矩阵的秩时，截断SVD可以精确地重构原矩阵。

## 考题，改版：矩阵横着放

好的，我们来处理横着放的矩阵。

令新矩阵为 $A_{new}$：
$$ A_{new} = \begin{bmatrix} 1 & 1 & 0 \\ 1 & 1 & 0 \end{bmatrix} $$
我们可以观察到，这个新矩阵 $A_{new}$ 正是原始矩阵 $A$ 的转置，即 $A_{new} = A^T$。

### 利用已有结果直接推导

根据SVD分解的性质，如果原始矩阵 $A$ 的分解是：
$$ A = U \Sigma V^T $$
那么其转置矩阵 $A^T$ 的分解就是：
$$ A^T = (U \Sigma V^T)^T = V \Sigma^T U^T $$

这意味着，我们不需要重新计算特征值和特征向量。我们只需要将原始分解中的 **U 和 V 互换**，并**将 Σ 矩阵转置**即可。

设 $A_{new}$ 的分解为 $A_{new} = U_{new} \Sigma_{new} V_{new}^T$，则：

*   **$U_{new} = V_{old}$**
*   **$\Sigma_{new} = \Sigma_{old}^T$**
*   **$V_{new} = U_{old}$**

我们从上一题中拿到原始的 U, Σ, V 矩阵：

*   $U_{old} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \\ 0 & 0 & 1 \end{bmatrix}$
*   $\Sigma_{old} = \begin{bmatrix} 2 & 0 \\ 0 & 0 \\ 0 & 0 \end{bmatrix}$
*   $V_{old} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix}$

现在，我们直接写出新矩阵 $A_{new}$ 的SVD组件：

*   **$U_{new}$ (2x2)**:
    $$ U_{new} = V_{old} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} $$
*   **$\Sigma_{new}$ (2x3)**:
    $$ \Sigma_{new} = \Sigma_{old}^T = \begin{bmatrix} 2 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix} $$
*   **$V_{new}$ (3x3)**:
    $$ V_{new} = U_{old} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \\ 0 & 0 & 1 \end{bmatrix} $$
    其转置为：
    $$ V_{new}^T = U_{old}^T = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \\ 0 & 0 & 1 \end{bmatrix} $$

---

### 三种 SVD 分解结果

#### 1. 完全 SVD (Full SVD)

$A_{new}$ 是一个 2x3 矩阵 (m=2, n=3)。完全SVD的形式是 `A(2x3) = U(2x2) Σ(2x3) Vᵀ(3x3)`。

$$ A_{new} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} \begin{bmatrix} 2 & 0 & 0 \\ 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \\ 0 & 0 & 1 \end{bmatrix} $$

#### 2. 约化 SVD (Reduced SVD / Thin SVD)

对于 m < n 的情况，我们移除 Σ 矩阵多余的全零列，并相应地调整 V 的维度，使得 Σ 成为一个方阵。
U 变为 m x m，Σ 变为 m x m，Vᵀ 变为 m x n。

*   **U_reduced (2x2)**: (保持不变)
    $$ U_{reduced} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} $$
*   **Σ_reduced (2x2)**: (取 Σ 的前 m 列)
    $$ \Sigma_{reduced} = \begin{bmatrix} 2 & 0 \\ 0 & 0 \end{bmatrix} $$
*   **Vᵀ_reduced (2x3)**: (取 Vᵀ 的前 m 行)
    $$ V_{reduced}^T = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \end{bmatrix} $$

分解形式为：
$$ A_{new} = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} \\ 1/\sqrt{2} & -1/\sqrt{2} \end{bmatrix} \begin{bmatrix} 2 & 0 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \\ 1/\sqrt{2} & -1/\sqrt{2} & 0 \end{bmatrix} $$

#### 3. 截断 SVD (Truncated SVD)

矩阵的秩仍然是 1 (只有一个非零奇异值 σ₁ = 2)，所以我们取 k=1 进行截断。
这会得到对原矩阵的最佳秩-1 近似，也就是它本身。

我们取 k=1 对应的部分：

*   **U₁ (2x1)**: (取 $U_{new}$ 的第 1 列)
    $$ U_1 = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix} $$
*   **Σ₁ (1x1)**: (取 $\Sigma_{new}$ 的左上角 1x1 部分)
    $$ \Sigma_1 = \begin{bmatrix} 2 \end{bmatrix} $$
*   **V₁ᵀ (1x3)**: (取 $V_{new}^T$ 的第 1 行)
    $$ V_1^T = \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \end{bmatrix} $$

分解形式为：
$$ A_{new} = U_1 \Sigma_1 V_1^T = \begin{bmatrix} 1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix} \begin{bmatrix} 2 \end{bmatrix} \begin{bmatrix} 1/\sqrt{2} & 1/\sqrt{2} & 0 \end{bmatrix} $$

通过利用矩阵转置的性质，我们无需任何额外计算，直接通过交换和转置就得到了新矩阵的完整SVD分解。