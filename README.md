# EVA-Space-Center-Data-Generate
## Introduction
##### Time
    - A project started from 2019 June. 
##### Goal
    - It's aims to predict the position and the pose of an aircraft from a single Moon image.
- Data consists of 100,000 moon images from random angles and distance.
- 80,000 train data；10,000 test data；10,000 valid data.
- The label(target/ground truth): `c_gamma`, `c_theta`, `c_phi`, `p_gamma`, `p_theta`, `p_phi`, `u_x`, `u_y`, `u_z`
- The global world coordinate is based on Moon center, all vectors are based on the origin of the global world coordinate. 
- We consider the spherical coordinate in physics view.   <img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/360px-3D_Spherical.svg.png"  height="20%" width="20%">
- The meaning of this 9 parameters list below:
    - `c_gamma`: gamma of the camera position.
    - `c_theta`: theta of the camera position.
    - `c_phi`: phi of the camera position.
    - `p_gamma`: gamma of the optical axis' end point. However, the setting of p_gamma doesn't cause any difference of where cemera look at nor the images, only the direction matters, you can see the experiment below.
    - `p_theta`: theta of the optical axis' end point.
    - `p_phi`: phi of the optical axis' end pount.
    - `u_x`: x componet of camera pose's normal vecter.
    - `u_y`: y componet of camera pose's normal vecter.
    - `u_z`: z componet of camera pose's normal vecter.
- The range of this 9 parameters list below:
    - `c_gamma`: [1.74308766628, 1.75292031414] in OpenGL unit --> [1737.3,  1747.1] km, 200m ~ 10,000m above Moon surface.
    - `c_theta`: [0, 2pi] radian
    - `c_phi`: [0, pi] radian
    - `p_gamma`: [0, 1.742887] in OpenGL unit --> [0, 1737.1] km, radius of the Moon.
    - `p_theta`: [0, 2pi] radian
    - `p_phi`: [0, pi] radian
    - `u_x`: [-1, 1] no unit, since the normal vector is normalized.
    - `u_y`: [-1, 1] no unit , since the normal vector is normalized.
    - `u_z`: [-1, 1] no unit, since the normal vector is normalized.
```c++
    void gluLookAt(	GLdouble eyeX, GLdouble eyeY, GLdouble eyeZ,
                        GLdouble centerX, GLdouble centerY, GLdouble centerZ,
                        GLdouble upX, GLdouble upY, GLdouble upZ
                   );
```
- gluLookAt Parameters Meaning:
    - eyeX, eyeY, eyeZ
        - Specifies the position of the eye point.
    - centerX, centerY, centerZ
        - Specifies the position of the reference point.
    - upX, upY, upZ
        - Specifies the direction of the up vector.
- See more definition of gluLookAt at https://www.khronos.org/registry/OpenGL-Refpages/gl2.1/xhtml/gluLookAt.xml

## Enviroment
- Anaconda 2
- python 3.6
- pip install
    - opencv-python==3.4.2
    - pygame==1.9.4
    - PyOpenGL==3.1.3b2
    
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
    - `LEVEL_1_INDEX`: How many part_1 do you want.
    - `LEVEL_2_INDEX`: How many part_2 do you want.
    - `IMAGE_INDEX`: How many images do you want in one part_2.
   
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
- Hierarchy of the directory
> - Dataset
>> - Level 1 directory i: 0 ~ 9
>> - i_j.targz
>> - target_i.json 
>>> - Level 2 directory i_j j: 0 ~ 9
>>>> - 1,000 images in name of "DATASETNAME_XXXXX.png"

- target_i.json:
```python
  {
    'image_name': [`c_gamma`, `c_theta`, `c_phi`, `p_gamma`, `p_thet`a, `p_phi`, `u_x`, `u_y`, `u_z`]
    }
```

## Sample
|Dataset_all_random_999.png|Dataset_all_random_9999.png|
|:---:|:---:|
|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Dataset_all_random_999.png"/>|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Dataset_all_random_9999.png"/>|
|Dataset_all_random_29999.png|Dataset_all_random_35999.png|
|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Dataset_all_random_29999.png"/>|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Dataset_all_random_35999.png"/>|

## Experiment of p_gamma
|Set p_gamma at the center of the Moon|Set p_gamma at infinite far|
|:---:|:---:|
|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Single_Image_center.png"/>|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Single_Image_infinite_far.png"/>|
|Set p_gamma at the near surface of the Moon|Set p_gamma at the far surface of the Moon|
|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Single_Image_negative_surface.png"/>|<img src="https://github.com/charleschiu2012/EVA-Space-Center-Data-Generate/blob/master/src/Single_Image_positive_surface.png"/>|
- After comparing every pixel of these images, there is zero differeence between it.

## TODO
- [ ] load images problem
- [ ] adjustment constamt penalty 
- [ ] Nan value

