#include <string.h>
#include <stdio.h>
#include <sys/param.h>
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

#define LEN_MAC_ADDR 20

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

int promi_count = 0;


void promi_cb(void *buff, wifi_promiscuous_pkt_type_t type) {
    //if (type != WIFI_PKT_MGMT) return;
    uint32_t cycle_counts;
	RSR(CCOUNT, cycle_counts);
    
    const wifi_promiscuous_pkt_t *ppkt = (wifi_promiscuous_pkt_t *)buff;
    const wifi_ieee80211_packet_t *ipkt = (wifi_ieee80211_packet_t *)ppkt->payload;
    const wifi_ieee80211_mac_hdr_t *hdr = &ipkt->hdr;
    char addr[18];
    char attacker_addr[] = "aa:bb:bb:bb:bb:bb";
    char target_addr[] = "00:5f:67:ea:74:2b";
    sprintf(addr, "%02x:%02x:%02x:%02x:%02x:%02x",
            hdr->addr1[0], hdr->addr1[1], hdr->addr1[2],
            hdr->addr1[3], hdr->addr1[4], hdr->addr1[5]);
    if (strcmp(addr, target_addr) == 0 && hdr->frame_ctrl == 0x148) {
        printf("<inject>%u</inject>\n", cycle_counts); 
    }
    if (strcmp(addr, attacker_addr) == 0){
        printf("<ACK>%u</ACK>\n", cycle_counts);
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
  // initialize WiFi connection 
  	wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
	cfg.csi_enable = 1;
	ESP_ERROR_CHECK(esp_wifi_init(&cfg));
	ESP_ERROR_CHECK(esp_wifi_set_storage(WIFI_STORAGE_RAM));
	ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
	ESP_ERROR_CHECK(esp_wifi_start());
    ESP_LOGI(TAG, "ESP_WIFI_MODE_STA");

	wifi_promiscuous_filter_t filter_promi_ctrl;
    filter_promi_ctrl.filter_mask = WIFI_PROMIS_CTRL_FILTER_MASK_ACK;
	wifi_promiscuous_filter_t filter_promi;
	filter_promi.filter_mask = WIFI_PROMIS_FILTER_MASK_CTRL | WIFI_PROMIS_FILTER_MASK_DATA;
	ESP_ERROR_CHECK(esp_wifi_set_promiscuous_filter(&filter_promi));
	ESP_ERROR_CHECK(esp_wifi_set_promiscuous_ctrl_filter(&filter_promi_ctrl));
	// ESP_ERROR_CHECK(esp_wifi_set_channel(1,0));
	ESP_ERROR_CHECK(esp_wifi_set_promiscuous(true));
    vTaskDelay(1000 / portTICK_PERIOD_MS);
    ESP_ERROR_CHECK(esp_wifi_set_promiscuous_rx_cb(promi_cb));
    printf("Sniffer initialized!\n");
}
