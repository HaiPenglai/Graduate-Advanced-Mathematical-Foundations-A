### 题型：QR分解(Householder法)



![image-20251118100215579](./assets/image-20251118100215579.png)



![image-20251118100243646](./assets/image-20251118100243646.png)

![image-20251118100417283](./assets/image-20251118100417283.png)

![image-20251118100425118](./assets/image-20251118100425118.png)

![image-20251118100435402](./assets/image-20251118100435402.png)

![image-20251118100536568](./assets/image-20251118100536568.png)



**问题：** 对矩阵 $A = \begin{pmatrix} 0 & -3 & 1 \\ 2 & 1 & -6 \\ 0 & 4 & 2 \end{pmatrix}$ 进行 QR 分解。

QR 分解的目标是将矩阵 A 分解为 $A = QR$，其中 Q 是正交矩阵，R 是上三角矩阵。Householder 变换是一种常用的方法，它通过一系列正交变换将 A 逐步转化为上三角矩阵 R。

