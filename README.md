# EVA-Space-Center-Data-Generate
## Introduction
- `Time`: A project started from 2019 June. 
- `Goal`: It's aims to predict the position and the pose of an aircraft from a single Moon image.
- Data consists of 100,000 moon images from random angles and distance.
- 80,000 train data；10,000 test data；10,000 valid data.
- The label(target/ground truth): `c_gamma`, `c_theta`, `c_phi`, `p_gamma`, `p_theta`, `p_phi`, `u_x`, `u_y`, `u_z`
- If not mentioned, the world ball coordinate is based on Moon center.  
- The meaning of this 9 parameters list below:
    - `c_gamma`: gamma of the camera position.
    - `c_theta`: theta of the camera position.
    - `c_phi`: phi of the camera position.
    - `p_gamma`: gamma of the optical axis' end point.
    - `p_theta`: theta of the optical axis' end point.
    - `p_phi`: phi of the optical axis' end pount.
    - `u_x`: x componet of camera's normal vecter, the coordinate is based on cemera's center.
    - `u_y`: y componet of camera's normal vecter, the coordinate is based on cemera's center.
    - `u_z`: z componet of camera's normal vecter, the coordinate is based on cemera's center.
- The range of this 9 parameters list below:
    - `c_gamma`: [1737.3,  1747.1] km, 200m ~ 10,000m above Moon surface.
    - `c_theta`: [0, 2pi] radian
    - `c_phi`: [0, pi] radian
    - `p_gamma`: [0, 1737.1] km, radius of the Moon.
    - `p_theta`: [0, 2pi] radian
    - `p_phi`: [0, pi] radian
    - `u_x`: [-1, 1] no unit, since the normal vector is normalized.
    - `u_y`: [-1, 1] no unit , since the normal vector is normalized.
    - `u_z`: [-1, 1] no unit, since the normal vector is normalized.

## Enviroment
- Anaconda 2
- python 3.7
- pip install
    - opencv-python==
- conda install
    - pygame==
    - opengl==
    
## Config
> Before generating dataset, you have to adjust config.py.
- Set logger
    - Which level of logger you want to show.
- Dateset name
    - Name the dataset.
- Units
    - Units of the Moon and the openGL world.
- Constraints:
    - Set your image size, field of view and the range of `c_gamma`.
    - `VIEWPORT`: The size of the image.
    - `FOVY`: The field of view angle, in degrees, in the y direction.
    - `Z_NEAR`: The distance from the viewer to the near clipping plane (always positive).
    - `Z_FAR`: The distance from the viewer to the far clipping plane (always positive).
    - <img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/FOV.png" height="50%" width="50%">
    - `LOWER_BOUND`: The lower bound of the `c_gamma`.
    - `UPPER_BOUND`: The upper bound of the `c_gamma`.
- PATH
    - The path you save your dataset.
- hyperparameters
    - `IMAGE_INDEX`: How many image do you want in one part.
    - `PART_INDEX`: How many part do you want.
   
## Setting up OpenGL Envoriment
- set_viewport():
    - Set view port.
- set_light_property():
    - Set light poroperty.
- set_filed_of_vision():
    - Set FOV.
- set_camera_position():
    - Set camera position. c_gamma, c_theta, c_phi are sampled with `random.uniform` in their own range.
- set_optical_axis_look_at():
    - Set optical axis' end point. p_gamma, p_theta, p_phi are sampled with `random.uniform` in their own range.
- camera_direction():
    - Set direction of the camera. u_x, u_y, u_z are sampled with `random.uniform` between 0~1.
    
## JSON File Format
- Each JSON file contains 10,000 images/tagets.
- imageX.json (X: 0~9):
  {
    'image_name': cv2 ndarray[height, width, channels] in list form.
    }
- targetX.json (X: 0~9):
  {
    'image_name': [`c_gamma`, `c_theta`, `c_phi`, `p_gamma`, `p_thet`a, `p_phi`, `u_x`, `u_y`, `u_z`]
    }
    
