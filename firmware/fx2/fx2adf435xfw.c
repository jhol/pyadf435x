/*
 * This file is part of the fx2ad4351fw project.
 *
 * Copyright (C) 2011-2012 Uwe Hermann <uwe@hermann-uwe.de>
 * Copyright (C) 2017 Joel Holdsworth <joel@airwebreathe.org.uk>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <http://www.gnu.org/licenses/>.
 */

/*
 * fx2ad4351fw is an open-source firmware for a Cypress FX2 based USB
 * interface to the Analog Devices ADF435x series of chips.
 *
 * It is written in C, using fx2lib as helper library, and sdcc as compiler.
 * The code is licensed under the terms of the GNU GPL, version 2 or later.
 *
 */

#include <autovector.h>
#include <fx2regs.h>
#include <fx2macros.h>
#include <delay.h>
#include <setupdat.h>
#include <eputils.h>
#include <command.h>

/* ... */
volatile __bit got_sud;
BYTE vendor_command;

BOOL handle_get_descriptor() {
  return FALSE;
}

BOOL handle_vendorcommand(BYTE cmd)
{
	/* Protocol implementation */
	switch (cmd) {
	case CMD_SET_REG:
		vendor_command = cmd;
		EP0BCL = 0;
		return TRUE;
	}

	return FALSE;
}

BOOL handle_get_interface(BYTE ifc, BYTE *alt_ifc)
{
	/* We only support interface 0, alternate interface 0. */
	if (ifc != 0)
		return FALSE;

	*alt_ifc = 0;
	return TRUE;
}

BOOL handle_set_interface(BYTE ifc, BYTE alt_ifc)
{
	/* We only support interface 0, alternate interface 0. */
	if (ifc != 0 || alt_ifc != 0)
		return FALSE;

	return TRUE;
}

BYTE handle_get_configuration(void)
{
	/* We only support configuration 1. */
	return 1;
}

BOOL handle_set_configuration(BYTE cfg)
{
	/* We only support configuration 1. */
	return (cfg == 1) ? TRUE : FALSE;
}

void sudav_isr(void) __interrupt SUDAV_ISR
{
	got_sud = TRUE;
	CLEAR_SUDAV();
}

void sof_isr(void) __interrupt SOF_ISR __using 1
{
	CLEAR_SOF();
}

void usbreset_isr(void) __interrupt USBRESET_ISR
{
	handle_hispeed(FALSE);
	CLEAR_USBRESET();
}

void hispeed_isr(void) __interrupt HISPEED_ISR
{
	handle_hispeed(TRUE);
	CLEAR_HISPEED();
}

void fx2adf435xfw_init(void)
{
	/* Set DYN_OUT and ENH_PKT bits, as recommended by the TRM. */
	REVCTL = bmNOAUTOARM | bmSKIPCOMMIT;

	got_sud = FALSE;
	vendor_command = 0xff;

	/* Renumerate. */
	RENUMERATE_UNCOND();

	SETCPUFREQ(CLK_48M);

	USE_USB_INTS();

	/* TODO: Does the order of the following lines matter? */
	ENABLE_SUDAV();
	ENABLE_SOF();
	ENABLE_HISPEED();
	ENABLE_USBRESET();

	/* Global (8051) interrupt enable. */
	EA = 1;
}

void fx2adf435xfw_poll(void)
{
	if (got_sud) {
		handle_setupdata();
		got_sud = FALSE;
	}

	switch (vendor_command) {
	case CMD_SET_REG:
		if ((EP0CS & bmEPBUSY) != 0)
			break;

		if (EP0BCL == 5) {
		}

		/* Acknowledge the vendor command. */
		vendor_command = 0xff;
		break;
	default:
		/* Unimplemented command. */
		vendor_command = 0xff;
		break;
	}
}

void main(void)
{
	fx2adf435xfw_init();
	while (1)
		fx2adf435xfw_poll();
}
