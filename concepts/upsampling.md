**Upsampling** is a process used in signal processing, image processing, and machine learning (especially in deep learning) to **increase the resolution or size** of data—such as an image, audio signal, or feature map—by **adding more samples or pixels**.

### In simpler terms:
- **For images**: Upsampling makes a small image larger by inserting new pixels. Common methods include:
  - **Nearest-neighbor interpolation** (copies nearby pixel values)
  - **Bilinear or bicubic interpolation** (averages surrounding pixels for smoother results)
  - **Transposed convolution** (also called deconvolution, often used in neural networks like U-Net)

- **For audio**: Upsampling increases the sampling rate (e.g., from 22 kHz to 44.1 kHz) by inserting new samples between existing ones, often followed by filtering to smooth the signal.

- **In deep learning**: Upsampling is frequently used in **encoder-decoder architectures** (e.g., for semantic segmentation) to restore spatial dimensions after downsampling (e.g., via pooling or strided convolutions).

### Key point:
Upsampling **does not add new information**—it estimates or interpolates missing data based on existing samples. The goal is to reconstruct a higher-resolution version while preserving important features as accurately as possible.

> 📌 **Opposite term**: *Downsampling* (reducing resolution or size).
