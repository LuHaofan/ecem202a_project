# Project Proposal

## 1. Motivation & Objective

WiFi is playing a more and more important role in our life nowadays. With the popularization of WiFi-enabled IoT devices and increasing coverage of WiFi, the WiFi signals, while invisible, is well-engaged in our life. People within the WiFi coverage area are constantly interacting with these signals, which makes these signals carry information about people's locations, movement and even respiration rate. 

In this project, we will look into the variations of WiFi signals caused by the movement of surrounding people to extract information about the motion of these people. 

## 2. State of the Art & Its Limitations

Sensing with WiFi signals is getting more and more attention in wireless research community recently, for the ubiquity of signals from well-deployed infrastructures. Channel State Information (CSI) has been proved effective for various sensing purpose. For example, human presence detection applications [1-4] can identify the number of people in a room and their relative locations; human event detection applications can infer typical events such as fall[5], walking[6], intrusion[7], sleeping[8], keystroke[9], posture change[10] and school violence [11], etc.. More fine-grained sensing applications can even recognize human gesture [12-15] and estimate respiration rate [10,16]. 

However, the existing works either require modifications to the existing WiFi Access Point, or call for well-established connection between transmitter and receiver. Those restrictions make the systems less practical and thus hinder the popularization of relevant products in the market. 


## 3. Novelty & Rationale

In this project, we take an advantage of a newly-discovered property of WiFi, polite-WiFi [17], to do WiFi sensing. Polite-WiFi indicates that today's WiFi devices acknowledge any frame they receive as long as the destination address matches their MAC address. With this property, we can acquire the channel state information, from the ACK packet, without establishing any connnections between AP and mobile device. Also, no modification to the AP is required in this situation. 

The advantage of this design scheme could be better illustrated in a real application scenario. Imagine you are in a big mall, where WiFi infrastructure is well-deployed. You have a phone in your hand, but you do not know the passwords for the WiFi APs, so you cannot connect to any of these APs. With our design, your phone could still acquire the CSI data from these APs for various application purpose without establishing any connection with any AP. 

The generality of our appoarch could further be supported by the fact that more and more IoT devices are going to appear in our life. These IoT devices, as long as is wifi-enabled, can be used by our application to acquire CSI. The further processing of ubiquitous CSI data could help us get better sensing accuracy.

## 4. Potential Impact

This project takes a different approach in WiFi-based wireless sensing by gathering CSI data from multiple sources instead of only one established connection between the device and AP. It does not require any modification to the AP; thus, is more practical in real world application. 

## 5. Challenges

1. Multipath: multipath effect is a common challenge in most of the wireless sensing application. The reflected wireless signal from walls and other objects in the environment create multiple signal path from transmitter to receiver. These multipaths will add noise to the wireless channel and thus become a challenge for signal processing and inference. 

2.  Processing Subcarrier Information: ESP32 WiFi module can extract the CSI from the ACK packets. However, the CSI contains 52 subcarriers and the quality of them varies drastically. An efficient and accurate algorithm is needed to analyze all 52 subcarriers. 

## 6. Requirements for Success

In this project, we will be using ESP32 Board to collect CSI data. ESP32 is developing board designed by Espressif company. They also provide the software development toolkit, Espressif IoT Development Framework (ESP-IDF) [18]. Being familiar in ESP-IDF is required for success in this project. Basic knowledge about signal processing algorithms is also needed to process the CSI data and infer information about people's movement. 

## 7. Metrics of Success

Whether or not the system can detect the motion of human is the first metric we will try to meet. Specifically, the system should indicate that there is motion happening if the user makes a movement with his/her arms or legs.

Whether or not the system can infer the position of the user in the room is the second criterion we will try to reach. Specifically, if the user walks along a trajectory in the room, our system should be able to identify that trajectory. 

## 8. Execution Plan

1. Install and test the CSI-collecting firmware to ESP32 board. Plot the CSI amplitude and phase versus time.

2. Develop program to send dummy packets to a nearby AP and get ACK back to extract CSI data.

3. Deploy multiple ESP32 in the room to detect human motion.

## 9. Related Work

### 9.a. Papers

"WiFi Says 'Hi!' Back to Strangers!" [17] is the paper that presents the polite-wifi property. This porperty is the backbone technique we will be using in this project.

"Wi-ESP—A tool for CSI-based Device-Free Wi-Fi
Sensing (DFWS)" [19] presents the method of using ESP32 as a tool to collecting CSI data. 

"Performing WiFi Sensing with Off-the-shelf Smartphones" [20] presents the method to use ESP32 to collect CSI data and stream to the mobile phone. The authors developed an Android application for labeling and processing CSI data in mobile phone.

### 9.b. Datasets

We will collect data by ourselves using ESP32 board in this project. We are not going to use any online datasets.

### 9.c. Software

We will use the ESP-IDF [] for software development in this project. Common Python libraries such as NumPy, SciPy and Matplotlib will also be adopted in processing the data.

## 10. References

[1] Fadel Adib and Dina Katabi. 2013. See through walls with WiFi! In Proceedings oftheACMSIGCOMM2013 Conference on SIGCOMM (SIGCOMM’13). 75–86. DOI:https://doi.org/10.1145/2486001.2486039

[2] Liangyi Gong, Wu Yang, Zimu Zhou, Dapeng Man, Haibin Cai, Xiancun Zhou, and Zheng Yang. 2016. An adap- tive wireless passive human detection via fine-grained physical layer information. Ad Hoc Netw. 38 (2016), 38–50. DOI:https://doi.org/10.1016/j.adhoc.2015.09.005

[3] Sameera Palipana, Piyush Agrawal, and Dirk Pesch. 2016. Channel state information based human presence de- tection using non-linear techniques. In Proceedings ofthe 3rd ACM International Conference on Systems for Energy- Efficient Built Environments (BuildSys’16). 177–186. DOI:https://doi.org/10.1145/2993422.2993579

[4] Kun Qian, Chenshu Wu, Zheng Yang, Yunhao Liu, Fugui He, and Tianzhang Xing. 2018. Enabling contactless de- tection ofmoving humans with dynamic speeds using CSI. ACMTrans.Embed.Comput. Syst. 17, 2, Article 52 (Jan. 2018), 18 pages. DOI:https://doi.org/10.1145/3157677

[5] Chunmei Han, Kaishun Wu, Yuxi Wang, and Lionel M. Ni. 2014. WiFall: Device-free fall detection by wire- less networks. In Proceedings ofthe 2014 IEEE Conference on Computer Communications (INFOCOM’14). 271–279. DOI:https://doi.org/10.1109/INFOCOM.2014.6847948

[6] Yang Xu, Wei Yang, Jianxin Wang, Xing Zhou, Hong Li, and Liusheng Huang. 2018. WiStep: Device-free step counting with WiFi signals. Proc. ACM Interact. Mob. Wear. Ubiq. Technol. 1, 4, Article 172 (Jan. 2018), 23 pages. DOI:https://doi.org/10.1145/3161415

[7] Jiguang Lv, Dapeng Man, Wu Yang, Xiaojiang Du, and Miao Yu. 2018. Robust WLAN-based indoor intrusion detec- tion using PHY layer information. IEEE Access 6, 99 (2018), 30117–30127. DOI:https://doi.org/10.1109/ACCESS.2017. 2785444

[8] Xuefeng Liu, Jiannong Cao, Shaojie Tang, and Jiaqi Wen. 2014. Wi-sleep: Contactless sleep monitoring via WiFi signals. In Proceedings ofthe 2014 IEEE Real-Time Systems Symposium. 346–355. DOI:https://doi.org/10.1109/RTSS.2014.30

[9] Kamran Ali, Alex X. Liu, Wei Wang, and Muhammad Shahzad. 2017. Recognizing keystrokes using WiFi devices. IEEE J. Select. Areas Commun. 35, 5 (May 2017), 1175–1190. DOI:https://doi.org/10.1109/JSAC.2017.2680998

[10] Xuefeng Liu, Jiannong Cao, Shaojie Tang, Jiaqi Wen, and Peng Guo. 2016. Contactless respiration monitoring via off-the-shelf WiFi devices. IEEE Trans. Mobile Comput. 15, 10 (Oct. 2016), 2466–2479. DOI:https://doi.org/10.1109/ TMC.2015.2504935

[11] Qizhen Zhou, Chenshu Wu, Jianchun Xing, Juelong Li, Zheng Yang, and Qiliang Yang. 2017. Wi-dog: Monitoring school violence with commodity WiFi devices. In Wireless Algorithms, Systems, and Applications. Springer Interna- tional Publishing, 47–59.

[12] Wenfeng He, Kaishun Wu, Yongpan Zou, and Zhong Ming. 2015. WiG: WiFi-based gesture recognition system. In Proceedings ofthe 2015 24th International Conference on Computer Communication and Networks (ICCCN’15).1–7. DOI:https://doi.org/10.1109/ICCCN.2015.7288485

[13] Pedro Melgarejo, Xinyu Zhang, Parameswaran Ramanathan, and David Chu. 2014. Leveraging directional antenna capabilities for fine-grained gesture recognition. In Proceedings ofthe 2014 ACM International Joint Conference on Pervasive and Ubiquitous Computing (UbiComp’14). 541–551. DOI:https://doi.org/10.1145/2632048.2632095

[14] Kun Qian, Chenshu Wu, Zheng Yang, Yunhao Liu, Fugui He, and Tianzhang Xing. 2018. Enabling contactless de- tection ofmoving humans with dynamic speeds using CSI. ACMTrans.Embed.Comput. Syst. 17, 2, Article 52 (Jan. 2018), 18 pages. DOI:https://doi.org/10.1145/3157677

[15] Aditya Virmani and Muhammad Shahzad. 2017. Position and orientation agnostic gesture recognition using WiFi. In Proceedings ofthe 15th Annual International Conference on Mobile Systems, Applications, and Services (MobiSys’17). 252–264. DOI:https://doi.org/10.1145/3081333.3081340

[16] Heba Abdelnasser, Khaled A. Harras, and Moustafa Youssef. 2015. UbiBreathe: A Ubiquitous non-invasive WiFi- based breathing estimator. In Proceedings ofthe 16th ACM International Symposium on Mobile Ad Hoc Networking and Computing (MobiHoc’15). 277–286. DOI:https://doi.org/10.1145/2746285.2755969

[17] Ali Abedi and Omid Abari. 2020. WiFi Says "Hi!" Back to Strangers! In Proceedings of the 19th ACM Workshop on Hot Topics in Networks (HotNets '20). Association for Computing Machinery, New York, NY, USA, 132–138. DOI:https://doi.org/10.1145/3422604.3425951

[18] https://docs.espressif.com/projects/esp-idf/en/latest/esp32/

[19] Muhammad Atif, Shapna Muralidharan, Heedong Ko, Byounghyun Yoo, Wi-ESP—A tool for CSI-based Device-Free Wi-Fi Sensing (DFWS), Journal of Computational Design and Engineering, Volume 7, Issue 5, October 2020, Pages 644–656, https://doi.org/10.1093/jcde/qwaa048

[20] S. M. Hernandez and E. Bulut, "Performing WiFi Sensing with Off-the-shelf Smartphones," 2020 IEEE International Conference on Pervasive Computing and Communications Workshops (PerCom Workshops), 2020, pp. 1-3, doi: 10.1109/PerComWorkshops48775.2020.9156194
