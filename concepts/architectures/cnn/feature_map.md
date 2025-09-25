A **feature map** (also called an **activation map**) is a fundamental concept in **convolutional neural networks (CNNs)** used in deep learning, especially for computer vision tasks.

### Definition:
A feature map is the **output of a convolutional layer** when a set of learnable filters (also called kernels) is applied to an input image or to the output of a previous layer. Each filter detects specific patterns or features (like edges, corners, textures, or more complex structures in deeper layers), and the resulting 2D (or 3D) grid of responses is the feature map.

---

### How It Works:
1. **Input**: An image (e.g., height × width × channels, like 224×224×3 for RGB).
2. **Filter/Kernels**: Small learnable matrices (e.g., 3×3×3) that slide (convolve) across the input.
3. **Convolution**: At each position, the filter computes a dot product with the local region of the input.
4. **Output**: A 2D array (for one filter) representing where the pattern encoded by the filter appears in the input. This is **one feature map**.
5. **Multiple Filters**: A convolutional layer typically uses many filters (e.g., 64), producing **64 feature maps**, often stacked into a 3D volume (height × width × number_of_filters).

---

### Example:
- Input image: 32×32×3 (RGB)
- Conv layer with 10 filters of size 5×5×3
- Output: 28×28×10 → **10 feature maps**, each 28×28

Each of the 10 feature maps highlights different learned features (e.g., one might respond to vertical edges, another to red blobs, etc.).

---

### Key Points:
- **Early layers** detect simple features (edges, colors).
- **Deeper layers** detect complex, high-level features (object parts, faces, etc.).
- Feature maps are passed through **non-linear activation functions** (like ReLU) and possibly **pooling layers** to reduce spatial size.
- They form the basis for hierarchical feature learning in CNNs.

In summary, a **feature map is a representation of where specific visual features occur in the input**, as learned by the network during training.