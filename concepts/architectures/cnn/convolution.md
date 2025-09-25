**Convolution** is a mathematical operation widely used in **Convolutional Neural Networks (CNNs)** to extract features from input data—especially images. It involves sliding a small matrix called a **filter** (or **kernel**) over the input and computing the **dot product** between the filter and local regions of the input.

---

### 🎯 Purpose of Convolution:
- Detect patterns like edges, textures, or shapes.
- Reduce the number of parameters compared to fully connected layers.
- Preserve spatial relationships in the data.

---

### 🔧 How Convolution Works (Step by Step):

#### 1. **Input**:  
An image (or feature map), usually represented as a 2D or 3D grid of numbers (pixel values).

#### 2. **Filter (Kernel)**:  
A small learnable matrix (e.g., 3×3) that detects a specific feature.

#### 3. **Sliding & Dot Product**:  
The filter moves (slides) across the input, typically left-to-right and top-to-bottom. At each position, it computes the **element-wise multiplication** followed by **summing** the results.

#### 4. **Output**:  
A **feature map** (or activation map) showing where the filter’s pattern appears strongly in the input.

---

### 📌 Simple Example:

**Input Image** (5×5 grayscale):
```
1  1  1  0  0  
0  1  1  1  0  
0  0  1  1  1  
0  0  0  1  1  
0  0  0  0  1  
```

**Filter (3×3)** — designed to detect a diagonal edge from top-left to bottom-right:
```
1  0  0  
0  1  0  
0  0  1  
```

We'll use **no padding** and **stride = 1** (filter moves 1 pixel at a time).

---

### Step-by-Step Calculation:

**Top-left position**:
```
Input region:     Filter:
1 1 1             1 0 0
0 1 1       ×     0 1 0
0 0 1             0 0 1
```
Dot product = (1×1) + (1×0) + (1×0) + (0×0) + (1×1) + (1×0) + (0×0) + (0×0) + (1×1)  
= 1 + 0 + 0 + 0 + 1 + 0 + 0 + 0 + 1 = **3**

**Next position (slide right)**:
Input region:
```
1 1 0
1 1 1
0 1 1
```
Dot product = (1×1)+(1×0)+(0×0)+(1×0)+(1×1)+(1×0)+(0×0)+(1×0)+(1×1) = 1 + 0 + 0 + 0 + 1 + 0 + 0 + 0 + 1 = **3**

Continue this across all valid positions.

---

### Final Output (Feature Map, 3×3):
After sliding the 3×3 filter over the 5×5 input with stride 1 and no padding, the output size is **(5−3+1) × (5−3+1) = 3×3**:

```
3  3  2  
1  3  3  
0  1  3  
```

> 🔍 **Interpretation**: Higher values (like 3) indicate strong matches with the diagonal pattern the filter is looking for.

---

### 📏 Output Size Formula:
For a square input of size **N × N**, filter size **F × F**, padding **P**, and stride **S**:

\[
\text{Output size} = \left\lfloor \frac{N + 2P - F}{S} + 1 \right\rfloor
\]

In our example:  
\( N = 5, F = 3, P = 0, S = 1 \) → \( (5 + 0 - 3)/1 + 1 = 3 \)

---

### 💡 Real-World Context:
- In CNNs, filters are **learned during training** (not hand-coded like above).
- Early layers learn edges and blobs; deeper layers learn complex features (eyes, wheels, etc.).
- Multiple filters are used in parallel → multiple feature maps.

---

### Summary:
> **Convolution** = sliding a small filter over an image and computing local dot products to highlight where specific patterns occur. The result is a **feature map** that helps the network understand visual content.