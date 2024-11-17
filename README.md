# EyeTrack2Scene
EyeTrack2Scene is a Python-based tool designed to map eye-tracking data to movie viewing data of subjects. By integrating advanced video segmentation using a panoptic model, this project enables precise analysis of where viewers focus during film playback. This repository also incorporates a collaborative panoptic model developed by (https://github.com/vant7e), which significantly enhances video segmentation accuracy .Currently, the tool supports eye-tracking data in the ASCII format exported from EyeLink 1000 systems (https://www.sr-research.com/software/).

![Screenshot from 2024-11-17 00-17-43](https://github.com/user-attachments/assets/337960d1-214c-4463-adab-c0a547f69d9e)

The eye-tracking data provides spatial coordinates from fixation events (denoted as EFIX), indicating where the participant is focusing. These gaze points are mapped onto segmentation masks generated by the panoptic model for the corresponding time frame. This mapping enables the identification and segmentation of the specific region or object in the movie frame that the participant is likely focusing on.


![Screenshot from 2024-11-17 00-19-53](https://github.com/user-attachments/assets/2b8b2f6f-2e93-4ac1-b99e-940aacbd8596)

## Example: Frame 1, 0.06 seconds into the movie

![Screenshot from 2024-11-17 00-18-37](https://github.com/user-attachments/assets/90bef6ff-f6da-4148-9f4b-305b5a06e884)

![Screenshot from 2024-11-17 00-19-02](https://github.com/user-attachments/assets/2bab7d1d-00bc-4dd3-a0b5-dbbc93101b88)


## Features
- **Eye-Tracking Integration:** Maps raw eye-tracking data to specific regions in movie frames.
- **Panoptic Video Segmentation:** Leverages state-of-the-art panoptic segmentation to identify meaningful regions in video scenes.
- **Collaborative Contribution:** Incorporates the panoptic model developed by (https://github.com/vant7e).


## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/EyeTrack2Scene.git
   cd EyeTrack2Scene


## Contribution

Feedback and contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgments

Special thanks to (https://github.com/vant7e) for their work on the panoptic model that forms the backbone of the video segmentation in this tool.
