# Abstract

In this project, we will use Channel State Information (CSI) of WiFi for motion detection. ESP32 board is used as the embedded system devices in this project to collect CSI data. CSI is essentially the channel frequency response of a wireless channel, which characterize the channel properties, such as propagation delay, amptitude attenuation and phase rotation of the transmitted signal. In this project, we leverage the fact that people's movement near a WiFi-enabled device will change the wireless channel. These changes can be captured by CSI data and can be further processed to obtain information about the movement. Different from existing research projects using WiFI for motion detection [2-5], our project will leverage a newly-discovered property of WiFi, polite-WiFi [1], which enables us to collect CSI without directly connecting to the WiFi Access Point (AP). With this property, we can further collecting CSI from any WiFi-enabled device to extend the range of sensing. 

# Team

* Haofan Lu

# Required Submissions

* [Proposal](proposal)
* [Midterm Checkpoint Presentation Slides](https://drive.google.com/file/d/18RR0y9czv83Gx9dg8D67BZgh3Cry99_d/view?usp=sharing)
* [Final Presentation Slides](https://drive.google.com/file/d/1A0gdpzgnfYgBQ-FfNs9Pqryt9QZ9sFUC/view?usp=sharing)
* [Final Presentation Video](https://www.dropbox.com/s/86l5hg0eqhhl65u/GMT20211212-224127_Recording_1920x1080.mp4?dl=0)
* [Final Report](report)

# Reference
[1] Ali Abedi and Omid Abari. 2020. WiFi Says "Hi!" Back to Strangers! In Proceedings of the 19th ACM Workshop on Hot Topics in Networks (HotNets '20). Association for Computing Machinery, New York, NY, USA, 132–138. DOI:https://doi.org/10.1145/3422604.3425951

[2] Fadel Adib and Dina Katabi. 2013. See through walls with WiFi! In Proceedings oftheACMSIGCOMM2013 Conference on SIGCOMM (SIGCOMM’13). 75–86. DOI:https://doi.org/10.1145/2486001.2486039

[3] Liangyi Gong, Wu Yang, Zimu Zhou, Dapeng Man, Haibin Cai, Xiancun Zhou, and Zheng Yang. 2016. An adap- tive wireless passive human detection via fine-grained physical layer information. Ad Hoc Netw. 38 (2016), 38–50. DOI:https://doi.org/10.1016/j.adhoc.2015.09.005

[4] Sameera Palipana, Piyush Agrawal, and Dirk Pesch. 2016. Channel state information based human presence de- tection using non-linear techniques. In Proceedings ofthe 3rd ACM International Conference on Systems for Energy- Efficient Built Environments (BuildSys’16). 177–186. DOI:https://doi.org/10.1145/2993422.2993579

[5] Chenshu Wu, Zheng Yang, Zimu Zhou, Xuefeng Liu, Yunhao Liu, and Jiannong Cao. 2015. Non-invasive detection ofmoving and stationary human with WiFi. IEEE J. Select. Areas Commun. 33, 11 (Nov. 2015), 2329–2342. DOI:https: //doi.org/10.1109/JSAC.2015.2430294