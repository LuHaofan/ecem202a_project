#include <string.h>
#include <stdio.h>
#include <sys/param.h>
// #include "structures.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "protocol_examples_common.h"
#include "addr_from_stdin.h"
#include "lwip/err.h"
#include "lwip/sockets.h"
#include "lwip/sys.h"
#include "esp_wifi_types.h"

// Null Data frame: carry the power management bit in the frame controlled field.
// can only receive ACK from AP
/* Commonly used MAC address
  T15 Laptop: 0xF4, 0x4E, 0xE3, 0x96, 0x96, 0x82
  AP: 0x00, 0x5F, 0x67, 0xEA, 0x74, 0x2B
  Pixel 5a: 0x60, 0xB7, 0x6E, 0x44, 0xA8, 0x62
  L13 Laptop: 0x64, 0x6E, 0xE0, 0x92, 0xC3, 0xEF
*/
uint8_t Packet[24] = {
/* Packet Type/subtype */ 0x48, 0x01, 
/* Duration of transmission*/ 0x00, 0x00,
/* Receiver addr */ 0x00, 0x5F, 0x67, 0xEA, 0x74, 0x2B,        // L13 Laptop
/* Transmitter addr */ 0xAA, 0xBB, 0xBB, 0xBB, 0xBB, 0xBB,      // fake address
/* Destination addr */ 0x00, 0x5F, 0x67, 0xEA, 0x74, 0x2B,      // L13 Laptop
               0x00, 0x00
};

// Non-QoS data frame
// uint8_t Packet[] = {
// /* Packet Type/subtype */ 0x08, 0x00, 
// /* Duration of transmission*/ 0x00, 0x00,
// /* Receiver addr */ 0x60, 0xB7, 0x6E, 0x44, 0xA8, 0x62,        // L13 Laptop
// /* Transmitter addr */ 0xAA, 0xBB, 0xBB, 0xBB, 0xBB, 0xBB,      // fake address
// /* Destination addr */ 0xAA, 0xBB, 0xBB, 0xBB, 0xBB, 0xBB,      // L13 Laptop
//                0x00, 0x00//, 0x00, 0x00, 0x00, 0x00, 0x01,
//               //  0x00, 0x00, 0x00, 0x49, 0xa2, 0xd7, 0xab, 0x67, 0xf0, 0xc0, 0x7d,
//               //  0xff, 0x08, 0x06, 0x01, 0x38, 0x6f, 0x14, 0x5b, 0x0b, 0xe3, 0x04, 0xa1, 0x7d, 0x08, 0x40, 0xbd,   
//               //  0x59, 0x78, 0xc5, 0x72, 0xbc, 0x17, 0x50, 0x6d, 0xf8, 0xad, 0x4f, 0x10, 0x59, 0xd4, 0xed, 0xf9,   
//               //  0x05, 0xb6, 0x22, 0x15, 0xc9, 0x98, 0x6e, 0x9c
// };

static const char *TAG = "[ESP32]";
typedef struct {
  unsigned frame_ctrl:16;
  unsigned duration_id:16;
  uint8_t addr1[6]; /* receiver address */
  uint8_t addr2[6]; /* sender address */
  uint8_t addr3[6]; /* filtering address */
  unsigned sequence_ctrl:16;
  uint8_t addr4[6]; /* optional */
} wifi_ieee80211_mac_hdr_t;

typedef struct {
  wifi_ieee80211_mac_hdr_t hdr;
  uint8_t payload[0]; /* network data ended with 4 bytes csum (CRC32) */
} wifi_ieee80211_packet_t;

void promi_cb(void *buff, wifi_promiscuous_pkt_type_t type) {
    //if (type != WIFI_PKT_MGMT) return;
    uint32_t cycle_counts;
	RSR(CCOUNT, cycle_counts);
    
    const wifi_promiscuous_pkt_t *ppkt = (wifi_promiscuous_pkt_t *)buff;
    const wifi_ieee80211_packet_t *ipkt = (wifi_ieee80211_packet_t *)ppkt->payload;
    const wifi_ieee80211_mac_hdr_t *hdr = &ipkt->hdr;
    char addr[18];
    char target_addr[] = "aa:bb:bb:bb:bb:bb";
    sprintf(addr, "%02x:%02x:%02x:%02x:%02x:%02x",
            hdr->addr1[0], hdr->addr1[1], hdr->addr1[2],
            hdr->addr1[3], hdr->addr1[4], hdr->addr1[5]);

    if (strcmp(target_addr, addr) == 0) {
        /* Received ACK, record timestamp and send to server */
        // char timestamp[20];
        ESP_LOGI(TAG, "ACK received at %u\n", cycle_counts); 
        // sprintf(timestamp, "recv: %u\n", cycle_counts);
        // int err = send(sock_fd, timestamp, strlen(timestamp), 0);
        // if (err < 0) {
        //     ESP_LOGE(TAG, "Error occurred during sending: errno %d", errno);
        // }
        ///////////////////////////////////////////////////////
    }
}


// The following definition and funtions are needed if we want to set the physical layer bit rate for the fake packet, otherwise 1 Mbps is used.
typedef union {
     uint8_t fix_rate;
     uint8_t b5;
     uint8_t b4;

     struct {
         uint8_t b3;
         uint8_t b2;
     } b1;

     struct {
         uint32_t a1;
         uint8_t  a2;
         uint8_t  a3;
         uint8_t  a4;
         uint8_t  a5;
         struct {
             uint8_t a6;
             uint8_t a7;
         } a8[4];
         uint8_t a9;
         uint8_t a10;
         uint8_t a11;
         uint8_t a12;
     } a13;

 } wifi_internal_rate_t;

 /*
 wifi_internal_rate_t rate;
 rate.fix_rate = rate;
 esp_wifi_internal_set_rate(100, 1, 4, &rate);
 */
esp_err_t esp_wifi_internal_set_rate(int a, int b, int c, wifi_internal_rate_t *d);


esp_err_t set_wifi_fixed_rate(uint8_t value)
{
  wifi_internal_rate_t rate;
  rate.fix_rate = value;
  return esp_wifi_internal_set_rate(100, 1, 4, &rate);
}


//rates:
/*
0 - B 1Mb CCK
1 - B 2Mb CCK
2 - B 5.5Mb CCK
3 - B 11Mb CCK
4 - XXX Not working. Should be B 1Mb CCK SP
5 - B 2Mb CCK SP
6 - B 5.5Mb CCK SP
7 - B 11Mb CCK SP

8 - G 48Mb ODFM
9 - G 24Mb ODFM
10 - G 12Mb ODFM
11 - G 6Mb ODFM
12 - G 54Mb ODFM
13 - G 36Mb ODFM
14 - G 18Mb ODFM
15 - G 9Mb ODFM

16 - N 6.5Mb MCS0
17 - N 13Mb MCS1
18 - N 19.5Mb MCS2
19 - N 26Mb MCS3
20 - N 39Mb MCS4
21 - N 52Mb MCS5
22 - N 58Mb MCS6
23 - N 65Mb MCS7

24 - N 7.2Mb MCS0 SP
25 - N 14.4Mb MCS1 SP
26 - N 21.7Mb MCS2 SP
27 - N 28.9Mb MCS3 SP
28 - N 43.3Mb MCS4 SP
29 - N 57.8Mb MCS5 SP
30 - N 65Mb MCS6 SP
31 - N 72Mb MCS7 SP
*/

// Sends fake packets
void send_frame() {
  // set packetSize
  uint32_t packetSize = sizeof(Packet);

  // send packet
  esp_wifi_set_max_tx_power(0);
//   set_wifi_fixed_rate(11);  // <-- Here we can set one of the bitrates from the table above. For example 11 is 6 Mbps
  // Here we keep sending fake packets with the delay set in vTaskDelay.
  // Sending too fast will cause an issue, we need to increase the IO speed for make monitor
  int delay = 1000;
//   printf("delay is %dms\n", delay);
  while (true){
    // API: esp_err_t esp_wifi_80211_tx(wifi_interface_t ifx, const void *buffer, int len, bool en_sys_seq);
    ESP_ERROR_CHECK(esp_wifi_80211_tx(WIFI_IF_STA, Packet, packetSize, false)); 
    uint32_t cycle_counts;
	RSR(CCOUNT, cycle_counts);
    ESP_LOGI(TAG, "Inject Packet at %u\n", cycle_counts); 
    vTaskDelay(delay / portTICK_PERIOD_MS);
  }
}

void app_main(void)
{
	// Initialize NVS
	esp_err_t ret = nvs_flash_init();
	if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
		ESP_ERROR_CHECK(nvs_flash_erase());
		ret = nvs_flash_init();
	}
	ESP_ERROR_CHECK( ret );
    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
	// cfg.csi_enable = 1;
	ESP_ERROR_CHECK(esp_wifi_init(&cfg));
	ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
	ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
	ESP_ERROR_CHECK(esp_wifi_start());
    ESP_LOGI(TAG, "ESP_WIFI_MODE_STA");
	wifi_promiscuous_filter_t filter_promi_ctrl;
    filter_promi_ctrl.filter_mask = WIFI_PROMIS_CTRL_FILTER_MASK_BA | WIFI_PROMIS_CTRL_FILTER_MASK_ACK;
	wifi_promiscuous_filter_t filter_promi;
	filter_promi.filter_mask = WIFI_PROMIS_FILTER_MASK_CTRL;
	ESP_ERROR_CHECK(esp_wifi_set_promiscuous_filter(&filter_promi));
	ESP_ERROR_CHECK(esp_wifi_set_promiscuous_ctrl_filter(&filter_promi_ctrl));
	// ESP_ERROR_CHECK(esp_wifi_set_channel(1,0));
	ESP_ERROR_CHECK(esp_wifi_set_promiscuous(true));
  vTaskDelay(1000 / portTICK_PERIOD_MS);
  ESP_ERROR_CHECK(esp_wifi_set_promiscuous_rx_cb(promi_cb));
  printf("Injector initialized!\n");
	printf("Started injecting fake packet!\n");
	send_frame();
}
