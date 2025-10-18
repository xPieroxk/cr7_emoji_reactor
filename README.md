# Ronaldo Mood Detector ⚽️

This Python script uses your webcam to detect your facial expressions and hand gestures in real-time, displaying a corresponding image of Cristiano Ronaldo that matches your "mood."

React like Ronaldo and see the program respond!

---

## Features

* **Real-time Detection:** Uses OpenCV for video capture and MediaPipe for high-performance face and hand landmark tracking.
* **Multiple States:** Detects three different "Ronaldo moods":
    * 😄 **SIUU:** Detected when you make a round 'O' shape with your lips (like shouting "Siuu!").
    * 🖐️ **FIVE\_CHAMPIONS:** Detected when you show an open palm (five fingers) to the camera.
    * 😐 **SERIOUS:** The default state when no other gesture is detected.
* **Side-by-Side Display:** Shows your live camera feed next to the corresponding Ronaldo reaction image in a single window.
* **Assets Included:** The necessary reaction images (`serious.jpg`, `siuu.jpg`, `five_champions.jpg`) are included in the `ronaldo_images` folder.

---

## Requirements

* Python 3.x
* A webcam
* All dependencies listed in `requirements.txt`.

---

## Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/xPieroxk/cr7_mood_reactor.git
    cd cr7_mood_reactor
    ```

2.  **Install the required libraries**

    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

    Install dependencies from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

    *If a `requirements.txt` file is not available, you can install the core dependencies manually:*
    ```bash
    pip install opencv-python numpy mediapipe
    ```

---

## Usage

1.  Make sure your webcam is connected and all dependencies are installed.
2.  Run the Python script from your terminal:
    ```bash
    python ronaldo_mood_detector.py
    ```

3.  A window titled "Ronaldo Detector" will open.
    * Your camera feed will be on the left.
    * The Ronaldo mood image will be on the right.

4.  Try the gestures!
    * Make a round 'O' shape with your lips to trigger the **SIUU** state.
    * Hold up an open hand (five fingers) to trigger the **FIVE\_CHAMPIONS** state.

5.  Press **'q'** or **'Esc'** to quit the application.

---

## Configuration

You can modify the global constants at the top of the script to change its behavior:

* `WINDOW_WIDTH = 1280`: Sets the total width of the application window.
* `WINDOW_HEIGHT = 480`: Sets the height of the application window.
* `RONALDO_IMAGES = "ronaldo_images"`: The name of the folder containing the reaction images.
* `MIRROR_CAMERA = True`: Set to `True` for a "selfie view" mirror effect. Set to `False` for a true, non-mirrored view.
