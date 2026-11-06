# Computer Vision – Object Detection and Contour Extraction

## Candidate

**Name:** Luiza Teixeira Barcellos Rosauro de Almeida

## Project Overview

This project was developed as part of a technical selection process involving Python, computer vision, and image processing.

The goal of Challenge 1 was to detect multiple objects in an image, identify their categories, extract their contours, calculate geometric information, and generate an annotated image and a CSV file containing the results.

## Challenge Status

| Challenge | Description | Status |
|---|---|---|
| Challenge 1 | Object Detection and Contour Extraction | Completed |
| Challenge 2 | Data Diagnosis and Cleaning | Not started |
| Challenge 3 | Regression and Evaluation | Not started |

*Statuses will be updated as the project progresses.*

## Technologies and Libraries

- **Python 3.13**
- **Ultralytics YOLO11** – Pre-trained object segmentation model.
- **OpenCV** – Image processing and contour extraction.
- **NumPy** – Numerical operations and image mask processing.
- **Pandas** – Data organization and CSV generation.
- **Matplotlib** – Installed as a project dependency.

## Project Structure

```text
computer-vision-object-detection/
│
├── DESAFIO_1/
│   ├── imagens/
│   │   └── imagem_original.png
│   │
│   ├── resultados/
│   │   ├── imagem_contornos.png
│   │   └── objetos_identificados.csv
│   │
│   └── desafio_1.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Make sure Python 3.13 and Git are installed.

Clone the repository:

```bash
git clone https://github.com/LuizaAlmeida-2002/computer-vision-object-detection.git
```

Navigate to the project directory:

```bash
cd computer-vision-object-detection
```

Create a virtual environment:

```bash
py -3.13 -m venv .venv
```

Activate the virtual environment (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Execution

Run the following command from the project root directory:

```powershell
python .\DESAFIO_1\desafio_1.py
```

The YOLO11 segmentation model weights (`yolo11s-seg.pt`) are downloaded automatically by Ultralytics when needed. An internet connection may be required on the first execution.

## Challenge 1 – Methodology

### 1. Image Loading

The original image is loaded using OpenCV.

The program displays the image dimensions, including width, height, and number of color channels.

### 2. Object Detection and Segmentation

A pre-trained YOLO11 segmentation model is used to detect and classify objects in the image.

The model generates segmentation masks for the detected objects.

The selected model is `yolo11s-seg.pt`, provided by Ultralytics.

### 3. Contour Extraction

The segmentation masks are converted into binary images and resized to match the original image dimensions.

OpenCV's `findContours()` function is then used to extract the external contours.

Contours with an area smaller than 100 pixels² are discarded.

For each detected object, the largest contour is selected.

### 4. Geometric Information

The contour area is calculated using `cv2.contourArea()`.

The centroid coordinates are obtained using image moments through `cv2.moments()`.

### 5. Annotation and Results

The detected contours are drawn over a copy of the original image.

The corresponding object categories are displayed near their contours.

The program generates:

- An annotated image (`imagem_contornos.png`).
- A CSV file (`objetos_identificados.csv`) containing:
  - Object ID
  - Object category
  - Contour area in pixels²
  - Centroid X coordinate
  - Centroid Y coordinate

## Results

The model identified five relevant objects:

| Object | Detected Category |
|---|---|
| 1 | Cup |
| 2 | Bottle |
| 3 | Book |
| 4 | Mouse |
| 5 | Cell phone |

Two additional detections classified as `dining table` were excluded from the final results.

The original image has a resolution of 417 × 667 pixels.

## Limitations and Technical Considerations

- Object detection depends on the categories recognized by the pre-trained model.
- Overlapping objects may affect segmentation accuracy.
- Shadows, reflections, and complex backgrounds can interfere with object detection.
- Small objects may produce incomplete or inaccurate contours.
- The model may incorrectly classify objects with unusual shapes or appearances.
- The minimum contour area threshold may exclude very small objects.

No model training from scratch was performed. A pre-trained segmentation model was used.

## Data and Model Sources

- **Image:** Original image selected and provided for this challenge.
- **Segmentation model:** Ultralytics YOLO11 (`yolo11s-seg.pt`).
- **Documentation:** [Ultralytics Documentation](https://docs.ultralytics.com/)

## Artificial Intelligence Tools

AI tools were used as learning and development support, including assistance with understanding programming concepts, debugging, and organizing project documentation.

The implementation and execution of the code were performed in Python.

## Development Time and Next Steps

**Estimated development time:** Approximately 5 hours.

**Next steps:**
- Complete the remaining technical challenges.
- Improve project documentation.
- Review the final results and reproducibility of the solution.