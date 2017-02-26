;;
;; This file is part of the sigrok-firmware-fx2lafw project.
;;
;; Copyright (C) 2012 Uwe Hermann <uwe@hermann-uwe.de>
;; Copyright (C) 2016 Stefan Brüns <stefan.bruens@rwth-aachen.de>
;; Copyright (C) 2012-2017 Joel Holdsworth <joel@airwebreathe.org.uk>
;;
;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation; either version 2 of the License, or
;; (at your option) any later version.
;;
;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.
;;
;; You should have received a copy of the GNU General Public License
;; along with this program; if not, see <http://www.gnu.org/licenses/>.
;;

VID = 0x5604	; Manufacturer ID (0x0456)
PID = 0x0db4	; Product ID (0xb40d)

.macro string_descriptor_a n,str
_string'n:
	.nchr	len,"'str"
	.db	len * 2 + 2
	.db	3
	.irpc	i,^"'str"
		.db	''i, 0
	.endm
.endm

.macro string_descriptor_lang n,l
_string'n:
	.db	4
	.db	3
	.dw	>l + (<l * 0x100)
.endm

.module DEV_DSCR

; Descriptor types
DSCR_DEVICE_TYPE	= 1
DSCR_CONFIG_TYPE	= 2
DSCR_STRING_TYPE	= 3
DSCR_INTERFACE_TYPE	= 4
DSCR_ENDPOINT_TYPE	= 5
DSCR_DEVQUAL_TYPE	= 6

; Descriptor lengths
DSCR_INTERFACE_LEN	= 9

; Endpoint types
ENDPOINT_TYPE_CONTROL	= 0
ENDPOINT_TYPE_ISO	= 1
ENDPOINT_TYPE_BULK	= 2
ENDPOINT_TYPE_INT	= 3

.globl _dev_dscr, _dev_qual_dscr, _highspd_dscr, _fullspd_dscr, _dev_strings, _dev_strings_end
.area DSCR_AREA (CODE)

; -----------------------------------------------------------------------------
; Device descriptor
; -----------------------------------------------------------------------------
_dev_dscr:
	.db	dev_dscr_end - _dev_dscr
	.db	DSCR_DEVICE_TYPE
	.dw	0x0002			; USB 2.0
	.db	0 			; Class (defined at interface level)
	.db	0			; Subclass (defined at interface level)
	.db	0			; Protocol (defined at interface level)
	.db	64			; Max. EP0 packet size
	.dw	VID			; Manufacturer ID
	.dw	PID			; Product ID
	.dw	0x0000			; Product version (0.00)
	.db	1			; Manufacturer string index
	.db	2			; Product string index
	.db	0			; Serial number string index (none)
	.db	1			; Number of configurations
dev_dscr_end:

; -----------------------------------------------------------------------------
; Device qualifier (for "other device speed")
; -----------------------------------------------------------------------------
_dev_qual_dscr:
	.db	dev_qualdscr_end - _dev_qual_dscr
	.db	DSCR_DEVQUAL_TYPE
	.dw	0x0002			; USB 2.0
	.db	0			; Class (vendor specific)
	.db	0			; Subclass (vendor specific)
	.db	0			; Protocol (vendor specific)
	.db	64			; Max. EP0 packet size
	.db	1			; Number of configurations
	.db	0			; Extra reserved byte
dev_qualdscr_end:

; -----------------------------------------------------------------------------
; High-Speed configuration descriptor
; -----------------------------------------------------------------------------
_highspd_dscr:
	.db	highspd_dscr_end - _highspd_dscr
	.db	DSCR_CONFIG_TYPE
	; Total length of the configuration (1st line LSB, 2nd line MSB)
	.db	(highspd_dscr_realend - _highspd_dscr) % 256
	.db	(highspd_dscr_realend - _highspd_dscr) / 256
	.db	1			; Number of interfaces
	.db	1			; Configuration number
	.db	0			; Configuration string (none)
	.db	0xa0			; Attributes (bus powered, remote wakeup)
	.db	0x32			; Max. power (100mA)
highspd_dscr_end:

	; Interfaces (only one in our case)
	.db	DSCR_INTERFACE_LEN
	.db	DSCR_INTERFACE_TYPE
	.db	0			; Interface index
	.db	0			; Alternate setting index
	.db	0			; Number of endpoints
	.db	0xff			; Class (vendor specific)
	.db	0			; Subclass
	.db	0			; Protocol
	.db	0			; String index (none)

highspd_dscr_realend:

	.even

; -----------------------------------------------------------------------------
; Full-Speed configuration descriptor
; -----------------------------------------------------------------------------
_fullspd_dscr:
	.db	fullspd_dscr_end - _fullspd_dscr
	.db	DSCR_CONFIG_TYPE
	; Total length of the configuration (1st line LSB, 2nd line MSB)
	.db	(fullspd_dscr_realend - _fullspd_dscr) % 256
	.db	(fullspd_dscr_realend - _fullspd_dscr) / 256
	.db	1			; Number of interfaces
	.db	1			; Configuration number
	.db	0			; Configuration string (none)
	.db	0xa0			; Attributes (bus powered, remote wakeup)
	.db	0x32			; Max. power (100mA)
fullspd_dscr_end:

	; Interfaces (only one in our case)
	.db	DSCR_INTERFACE_LEN
	.db	DSCR_INTERFACE_TYPE
	.db	0			; Interface index
	.db	0			; Alternate setting index
	.db	0			; Number of endpoints
	.db	0xff			; Class (vendor specific)
	.db	0			; Subclass
	.db	0			; Protocol
	.db	0			; String index (none)

fullspd_dscr_realend:

	.even

; -----------------------------------------------------------------------------
; Strings
; -----------------------------------------------------------------------------

_dev_strings:

; See http://www.usb.org/developers/docs/USB_LANGIDs.pdf for the full list.
string_descriptor_lang 0 0x0409 ; Language code 0x0409 (English, US)

string_descriptor_a 1,^"ANALOG DEVICES"
string_descriptor_a 2,^"ADF4xxx USB Eval Board"
_dev_strings_end:
	.dw	0x0000
