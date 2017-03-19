/*
 * This file is part of the libopencm3 project.
 *
 * Copyright (C) 2011 Gareth McMullin <gareth@blacksphere.co.nz>
 * Copyright (C) 2017 Joel Holdsworth <joel@airwebreathe.org.uk>
 *
 * This library is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this library.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <libopencm3/cm3/nvic.h>
#include <libopencm3/stm32/dma.h>
#include <libopencm3/stm32/gpio.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/spi.h>
#include <libopencm3/usb/usbd.h>

#define PORT_LED GPIOC
#define PIN_LED GPIO13

#define PORT_SPI GPIOA
#define PIN_LE GPIO4
#define PIN_CLK GPIO5
#define PIN_DAT GPIO7

#define SPI SPI1

#define USB_REQ_SET_REG 0x40

const struct usb_device_descriptor dev = {
	.bLength = USB_DT_DEVICE_SIZE,
	.bDescriptorType = USB_DT_DEVICE,
	.bcdUSB = 0x0200,
	.bDeviceClass = 0,
	.bDeviceSubClass = 0,
	.bDeviceProtocol = 0,
	.bMaxPacketSize0 = 64,
	.idVendor = 0x0456,
	.idProduct = 0xb40d,
	.bcdDevice = 0x0000,
	.iManufacturer = 1,
	.iProduct = 2,
	.iSerialNumber = 0,
	.bNumConfigurations = 1,
};

const struct usb_interface_descriptor iface = {
	.bLength = USB_DT_INTERFACE_SIZE,
	.bDescriptorType = USB_DT_INTERFACE,
	.bInterfaceNumber = 0,
	.bAlternateSetting = 0,
	.bNumEndpoints = 0,
	.bInterfaceClass = 0xFF,
	.bInterfaceSubClass = 0,
	.bInterfaceProtocol = 0,
	.iInterface = 0,
};

const struct usb_interface ifaces[] = {{
	.num_altsetting = 1,
	.altsetting = &iface,
}};

const struct usb_config_descriptor config = {
	.bLength = USB_DT_CONFIGURATION_SIZE,
	.bDescriptorType = USB_DT_CONFIGURATION,
	.wTotalLength = 0,
	.bNumInterfaces = 1,
	.bConfigurationValue = 1,
	.iConfiguration = 0,
	.bmAttributes = 0x80,
	.bMaxPower = 0x32,

	.interface = ifaces,
};

const char *usb_strings[] = {
	"ANALOG DEVICES",
	"ADF4xxx USB Eval Board"
};

uint32_t usbd_control_buffer[32];

bool have_reg = false;
uint32_t reg = 0;

static void setup(void)
{
	/* Clock setup */
	rcc_clock_setup_in_hse_8mhz_out_72mhz();

	rcc_periph_clock_enable(RCC_DMA1);
	rcc_periph_clock_enable(RCC_AFIO);
	rcc_periph_clock_enable(RCC_GPIOA);
	rcc_periph_clock_enable(RCC_GPIOC);
	rcc_periph_clock_enable(RCC_SPI1);
	rcc_periph_clock_enable(RCC_OTGFS);

	/* LED output */
	gpio_set_mode(PORT_LED, GPIO_MODE_OUTPUT_2_MHZ,
		GPIO_CNF_OUTPUT_PUSHPULL, PIN_LED);

	/* SPI1 NSS, SCK, MOSI */
	gpio_set_mode(PORT_SPI, GPIO_MODE_OUTPUT_50_MHZ,
		GPIO_CNF_OUTPUT_PUSHPULL, PIN_LE);
	gpio_set(PORT_SPI, PIN_LE);
	gpio_set_mode(PORT_SPI, GPIO_MODE_OUTPUT_50_MHZ,
		GPIO_CNF_OUTPUT_ALTFN_PUSHPULL, PIN_CLK | PIN_DAT);

	spi_init_master(SPI, 0, SPI_CR1_CPOL_CLK_TO_0_WHEN_IDLE,
		SPI_CR1_CPHA_CLK_TRANSITION_1, SPI_CR1_DFF_8BIT,
                SPI_CR1_MSBFIRST);
	spi_set_baudrate_prescaler(SPI, SPI_CR1_BR_FPCLK_DIV_64);

	spi_enable_software_slave_management(SPI1);
	spi_set_nss_high(SPI1);
	spi_enable(SPI1);

	/* DMA */
	nvic_set_priority(NVIC_DMA1_CHANNEL3_IRQ, 0);
	nvic_enable_irq(NVIC_DMA1_CHANNEL3_IRQ);
}


static int vendor_control_callback(usbd_device *usbd_dev, struct usb_setup_data *req, uint8_t **buf,
		uint16_t *len, void (**complete)(usbd_device *usbd_dev, struct usb_setup_data *req))
{
	(void)buf;
	(void)len;
	(void)complete;
	(void)usbd_dev;

	switch (req->bmRequestType) {
	case USB_REQ_SET_REG: {
		if (*len != 4)
			return USBD_REQ_NOTSUPP;

		reg = ((*buf)[0] << 24) | ((*buf)[1] << 16) |
			((*buf)[2] << 8) | (*buf)[3];

		gpio_clear(PORT_SPI, PIN_LE);

		dma_channel_reset(DMA1, DMA_CHANNEL3);

		dma_set_peripheral_address(DMA1, DMA_CHANNEL3, (uint32_t)&SPI1_DR);
		dma_set_memory_address(DMA1, DMA_CHANNEL3, (uint32_t)&reg);
		dma_set_number_of_data(DMA1, DMA_CHANNEL3, sizeof(reg));
		dma_set_read_from_memory(DMA1, DMA_CHANNEL3);
		dma_enable_memory_increment_mode(DMA1, DMA_CHANNEL3);
		dma_set_peripheral_size(DMA1, DMA_CHANNEL3, DMA_CCR_PSIZE_8BIT);
		dma_set_memory_size(DMA1, DMA_CHANNEL3, DMA_CCR_MSIZE_8BIT);
		dma_set_priority(DMA1, DMA_CHANNEL3, DMA_CCR_PL_HIGH);

		dma_enable_transfer_complete_interrupt(DMA1, DMA_CHANNEL3);
		dma_enable_channel(DMA1, DMA_CHANNEL3);

		spi_enable_tx_dma(SPI);

		return USBD_REQ_HANDLED;
	}

	default:
		return USBD_REQ_NOTSUPP;
	}
}

static void usb_set_config_cb(usbd_device *usbd_dev, uint16_t wValue)
{
	(void)wValue;
	usbd_register_control_callback(usbd_dev, USB_REQ_TYPE_VENDOR,
		USB_REQ_TYPE_TYPE, vendor_control_callback);
}

/* SPI transmit completed with DMA */
void dma1_channel3_isr(void)
{
	if (DMA1_ISR & DMA_ISR_TCIF3)
		DMA1_IFCR |= DMA_IFCR_CTCIF3;

	dma_disable_transfer_complete_interrupt(DMA1, DMA_CHANNEL3);
	spi_disable_tx_dma(SPI1);
	dma_disable_channel(DMA1, DMA_CHANNEL3);
}

static void spi_poll(void)
{
	if (!(SPI_SR(SPI) & SPI_SR_BSY))
		gpio_set(PORT_SPI, PIN_LE);
}

int main(void)
{
	setup();

	usbd_device *const usbd_dev = usbd_init(&st_usbfs_v1_usb_driver, &dev,
		&config, usb_strings, 2, (uint8_t*)usbd_control_buffer,
		sizeof(usbd_control_buffer));
	usbd_register_set_config_callback(usbd_dev, usb_set_config_cb);

	while (1) {
		usbd_poll(usbd_dev);
		spi_poll();
	}
}

