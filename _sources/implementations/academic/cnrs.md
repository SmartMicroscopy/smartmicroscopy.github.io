#  The EnderScope as an educational platform for Smart Microscopy
**Erwan Grandgirard** (IGBMC: Illkirch-Graffenstaden, France), **Jerome Mutterer** (CNRS, Strasbourg University, Strasbourg, France)

## Specific Focus and scientific questions asked
The smart microscopy field is rapidly expanding and users are expected to appropriate its base concepts to take full advantage of the available new imaging approaches. Commercial often exemplify classical smart workflows which can limit the potential applications that users can envision. Moreover, practical learning about smart microscopy can be hindered by the current low number of available systems, or by costly access fees when highend devices actually are available. As discussed in the associated article, a further barrier is that developing smart microscopy workflows often requires learning at least some notions of programming or algorithmics, device control, image acquisition and image processing principles. The EnderScope with its matching control library aims to address these issues by providing a low cost, easy to learn ecosystem to teach, learn and develop smart microscopy {cite:p}`Gharbi2025`.

## Methodology, Implementation details
### Hardware setup
The hardware setup of the EnderScope is built around the frame of an cartesian 3D printer, which provides a reliable and precise 3-axis motorized stage for positioning. A Raspberry Pi serves as the central computational unit, coordinating the system and hosting the control software. Imaging is performed using interchangeable Raspberry Pi camera modules, ranging from the standard Camera Module v2 to the High Quality Camera and even third-party options such as the Arducam 64 MP autofocus camera, allowing flexibility in resolution, optics, and field of view. Other cameras also are an option, provided they have a device driver for RaspberryPi. Illumination is delivered by an array of RGB LEDs controlled by an Arduino microcontroller, which replaces the earlier manual switch with programmable lighting modes and adjustable intensity. All components communicate via serial over USB or the Pi’s camera connector, creating a compact, low-cost, and customizable imaging platform that can be assembled from widely available, low cost, parts.

### Software library
The [`enderscope.py` software library](https://github.com/mutterer/enderscopy/) provides the core interface that makes the EnderScope both accessible and versatile. Written in Python, it abstracts low-level device control into intuitive, high-level functions for the stage, illumination, and camera. The library includes dedicated classes such as Stage for precise axis movements using G-code, Enderlights for programmable multi-color LED illumination, and helper tools like SerialDevice for seamless USB communication. Synchronization mechanisms ensure that commands—such as moving the stage, setting illumination, and capturing images—execute in the proper sequence, preventing motion blur or misaligned acquisitions. Beyond code, the library also integrates simple graphical interfaces via iPywidgets, giving users manual control for exploration and setup. By combining structured programmatic access with hands-on examples and Jupyter notebooks, `enderscope.py` enables both beginners and advanced users to design, test, and expand smart microscopy workflows with ease.

## Contributions to Interoperability
Using Python for the EnderScope library matches the dominant language in smart microscopy. Most imaging tools such as scikit-image, Napari, and Micro-Manager bindings, are Python-based, ensuring easy integration and interoperability. Its simplicity lowers the entry barrier for beginners while offering advanced capabilities for researchers, making the system both accessible and powerful.
To facilitate user onboarding, examples are provided for tasks of basic or intermediate complexity to programmatically control all system elements, or perform classical computational imaging tasks. This includes: Stage movements along 3 axis; Illumination settings in various modes; Image capture using the Raspberry camera; Autofocus (using Laplacian variance on a Z-stack); Shadow/reflection removal with multi-angle illumination; SmartScan: overview scan + optimized region-of-interest imaging using TSP optimization.
Scripts developed using the `enderscope.py` library can easily be translated to other
smart microscopy APIs that typically provide identical or similar objects and associated functions.

## Limitations
- Mechanical precision: The used printer stage, while low-cost, lacks the nanometer accuracy and stability of professional microscope stages, limiting resolution and repeatability.
- Optical constraints: Standard Raspberry Pi or Arducam cameras and simple optics cannot match the sensitivity, dynamic range, or optical flexibility of scientific-grade cameras.
- Illumination: Although the LED array enables multi-angle and color variation, it cannot provide the coherence, polarization, or spectral specificity required for advanced fluorescence techniques.
- Speed and synchronization: Stepper-driven stage movements are relatively slow, and command execution through serial communication can introduce latency compared to dedicated hardware controllers.
- Software complexity: While Python lowers barriers, meaningful customization still requires coding skills, which may discourage users without programming backgrounds.
- Scalability: The open-source and DIY nature makes it excellent for prototyping and education, but less suited for high-throughput or research grade smart microscopy applications without further redesign and ruggedisation.


----

```{bibliography}
:style: plain
:filter: docname in docnames
```
