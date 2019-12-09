##
## This file is part of the pyadf435x project.
##
## Copyright (C) 2013 Uwe Hermann <uwe@hermann-uwe.de>
## Copyright (C) 2015 Daniel Elstner <daniel.kitta@gmail.com>
## Copyright (C) 2017 Joel Holdsworth <joel@airwebreathe.org.uk>
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, see <http://www.gnu.org/licenses/>.
##

GNUMAKEFLAGS = --no-print-directory
SUFFIXES = .a51 .c .fw .ihx .rel

# Flags for firmware hex file generation
SDCC_LINK_FLAGS = --code-size 0x1c00 --xram-size 0x0200 --xram-loc 0x1c00 -Wl"-b DSCR_AREA=0x1e00" -Wl"-b INT2JT=0x1f00"

# Include paths
as_includes = -I$(srcdir)/include
c_includes = -I$(srcdir)/include -I$(srcdir)/fx2lib/include

# Binary firmware tarball basename
distdir_bin = $(PACKAGE)-bin-$(VERSION)

# Basename of directory stamp files
dirstamp = .dirstamp

dirstamps = \
	fx2lib/lib/$(dirstamp) \
	fx2lib/lib/interrupts/$(dirstamp)

firmware_binaries = \
	fx2adf435xfw.fw

fx2adf435xfw_sources = \
	dscr.a51 \
	fx2adf435xfw.c

fx2adf435xfw_objects = \
	dscr.rel \
	fx2adf435xfw.rel

fx2lib_headers = \
	fx2lib/include/autovector.h \
	fx2lib/include/delay.h \
	fx2lib/include/eputils.h \
	fx2lib/include/fx2ints.h \
	fx2lib/include/fx2macros.h \
	fx2lib/include/fx2regs.h \
	fx2lib/include/fx2types.h \
	fx2lib/include/gpif.h \
	fx2lib/include/i2c.h \
	fx2lib/include/lights.h \
	fx2lib/include/serial.h \
	fx2lib/include/setupdat.h

fx2lib_sources = \
	fx2lib/lib/delay.c \
	fx2lib/lib/eputils.c \
	fx2lib/lib/gpif.c \
	fx2lib/lib/i2c.c \
	fx2lib/lib/serial.c \
	fx2lib/lib/setupdat.c \
	fx2lib/lib/usbav.a51

fx2lib_objects = \
	fx2lib/lib/delay.rel \
	fx2lib/lib/eputils.rel \
	fx2lib/lib/gpif.rel \
	fx2lib/lib/i2c.rel \
	fx2lib/lib/serial.rel \
	fx2lib/lib/setupdat.rel \
	fx2lib/lib/usbav.rel

fx2lib_ints_sources = \
	fx2lib/lib/interrupts/ep0ack_isr.c \
	fx2lib/lib/interrupts/ep0in_isr.c \
	fx2lib/lib/interrupts/ep0out_isr.c \
	fx2lib/lib/interrupts/ep0ping_isr.c \
	fx2lib/lib/interrupts/ep1in_isr.c \
	fx2lib/lib/interrupts/ep1out_isr.c \
	fx2lib/lib/interrupts/ep1ping_isr.c \
	fx2lib/lib/interrupts/ep2ef_isr.c \
	fx2lib/lib/interrupts/ep2ff_isr.c \
	fx2lib/lib/interrupts/ep2isoerr_isr.c \
	fx2lib/lib/interrupts/ep2_isr.c \
	fx2lib/lib/interrupts/ep2pf_isr.c \
	fx2lib/lib/interrupts/ep2ping_isr.c \
	fx2lib/lib/interrupts/ep4ef_isr.c \
	fx2lib/lib/interrupts/ep4ff_isr.c \
	fx2lib/lib/interrupts/ep4isoerr_isr.c \
	fx2lib/lib/interrupts/ep4_isr.c \
	fx2lib/lib/interrupts/ep4pf_isr.c \
	fx2lib/lib/interrupts/ep4ping_isr.c \
	fx2lib/lib/interrupts/ep6ef_isr.c \
	fx2lib/lib/interrupts/ep6ff_isr.c \
	fx2lib/lib/interrupts/ep6isoerr_isr.c \
	fx2lib/lib/interrupts/ep6_isr.c \
	fx2lib/lib/interrupts/ep6pf_isr.c \
	fx2lib/lib/interrupts/ep6ping_isr.c \
	fx2lib/lib/interrupts/ep8ef_isr.c \
	fx2lib/lib/interrupts/ep8ff_isr.c \
	fx2lib/lib/interrupts/ep8isoerr_isr.c \
	fx2lib/lib/interrupts/ep8_isr.c \
	fx2lib/lib/interrupts/ep8pf_isr.c \
	fx2lib/lib/interrupts/ep8ping_isr.c \
	fx2lib/lib/interrupts/errlimit_isr.c \
	fx2lib/lib/interrupts/gpifdone_isr.c \
	fx2lib/lib/interrupts/gpifwf_isr.c \
	fx2lib/lib/interrupts/hispeed_isr.c \
	fx2lib/lib/interrupts/ibn_isr.c \
	fx2lib/lib/interrupts/sof_isr.c \
	fx2lib/lib/interrupts/spare_isr.c \
	fx2lib/lib/interrupts/sudav_isr.c \
	fx2lib/lib/interrupts/suspend_isr.c \
	fx2lib/lib/interrupts/sutok_isr.c \
	fx2lib/lib/interrupts/usbreset_isr.c

fx2lib_ints_objects = \
	fx2lib/lib/interrupts/ep0ack_isr.rel \
	fx2lib/lib/interrupts/ep0in_isr.rel \
	fx2lib/lib/interrupts/ep0out_isr.rel \
	fx2lib/lib/interrupts/ep0ping_isr.rel \
	fx2lib/lib/interrupts/ep1in_isr.rel \
	fx2lib/lib/interrupts/ep1out_isr.rel \
	fx2lib/lib/interrupts/ep1ping_isr.rel \
	fx2lib/lib/interrupts/ep2ef_isr.rel \
	fx2lib/lib/interrupts/ep2ff_isr.rel \
	fx2lib/lib/interrupts/ep2isoerr_isr.rel \
	fx2lib/lib/interrupts/ep2_isr.rel \
	fx2lib/lib/interrupts/ep2pf_isr.rel \
	fx2lib/lib/interrupts/ep2ping_isr.rel \
	fx2lib/lib/interrupts/ep4ef_isr.rel \
	fx2lib/lib/interrupts/ep4ff_isr.rel \
	fx2lib/lib/interrupts/ep4isoerr_isr.rel \
	fx2lib/lib/interrupts/ep4_isr.rel \
	fx2lib/lib/interrupts/ep4pf_isr.rel \
	fx2lib/lib/interrupts/ep4ping_isr.rel \
	fx2lib/lib/interrupts/ep6ef_isr.rel \
	fx2lib/lib/interrupts/ep6ff_isr.rel \
	fx2lib/lib/interrupts/ep6isoerr_isr.rel \
	fx2lib/lib/interrupts/ep6_isr.rel \
	fx2lib/lib/interrupts/ep6pf_isr.rel \
	fx2lib/lib/interrupts/ep6ping_isr.rel \
	fx2lib/lib/interrupts/ep8ef_isr.rel \
	fx2lib/lib/interrupts/ep8ff_isr.rel \
	fx2lib/lib/interrupts/ep8isoerr_isr.rel \
	fx2lib/lib/interrupts/ep8_isr.rel \
	fx2lib/lib/interrupts/ep8pf_isr.rel \
	fx2lib/lib/interrupts/ep8ping_isr.rel \
	fx2lib/lib/interrupts/errlimit_isr.rel \
	fx2lib/lib/interrupts/gpifdone_isr.rel \
	fx2lib/lib/interrupts/gpifwf_isr.rel \
	fx2lib/lib/interrupts/hispeed_isr.rel \
	fx2lib/lib/interrupts/ibn_isr.rel \
	fx2lib/lib/interrupts/sof_isr.rel \
	fx2lib/lib/interrupts/spare_isr.rel \
	fx2lib/lib/interrupts/sudav_isr.rel \
	fx2lib/lib/interrupts/suspend_isr.rel \
	fx2lib/lib/interrupts/sutok_isr.rel \
	fx2lib/lib/interrupts/usbreset_isr.rel

fx2lib_libs = \
	fx2lib/lib/fx2.lib \
	fx2lib/lib/interrupts/ints.lib

firmwaredir = $(datadir)/firmware
firmware_DATA = $(firmware_binaries)

dist_noinst_DATA = $(fx2adf435xfw_headers) $(fx2adf435xfw_sources) $(fx2lib_headers) $(fx2lib_sources) $(fx2lib_ints_sources)
dist_noinst_SCRIPTS = autogen.sh

MOSTLYCLEANFILES = *.asm fx2lib/lib/*.asm fx2lib/lib/*.lib fx2lib/lib/interrupts/*.asm fx2lib/lib/interrupts/*.lib
CLEANFILES = $(firmware_binaries)
DISTCLEANFILES = $(dirstamps)

# Custom silent rules prefixes
SF_V_SDAS = $(sf_v_SDAS_@AM_V@)
sf_v_SDAS_ = $(sf_v_SDAS_@AM_DEFAULT_V@)
sf_v_SDAS_0 = @echo "  SDAS    " $@;
sf_v_SDAS_1 =

SF_V_SDCC = $(sf_v_SDCC_@AM_V@)
sf_v_SDCC_ = $(sf_v_SDCC_@AM_DEFAULT_V@)
sf_v_SDCC_0 = @echo "  SDCC    " $@;
sf_v_SDCC_1 =

.PHONY: dist-bin dist-changelog

all-local: $(firmware_binaries)

mostlyclean-local:
	-$(AM_V_at)find . -type f '(' -name '*.ihx' -o -name '*.lk' \
		-o -name '*.lst' -o -name '*.map' -o -name '*.mem' \
		-o -name '*.rel' -o -name '*.rst' -o -name '*.sym' ')' \
		-exec rm -f '{}' '+'

dist-hook: dist-changelog

dist-changelog:
	$(AM_V_at)if test -d '$(top_srcdir)/.git'; then \
		if git -C '$(top_srcdir)' log >.ChangeLog.tmp; \
		then mv -f .ChangeLog.tmp "$(top_distdir)/ChangeLog"; \
		else rm -f .ChangeLog.tmp; exit 1; fi; \
	else :; fi

# Creates a convenience tarball with just the generated *.fw files, so that
# the users don't have to build them manually.
dist-bin: $(firmware_binaries)
	-$(AM_V_at)rm -fr $(distdir_bin)
	$(AM_V_at)$(MKDIR_P) $(distdir_bin)
	$(AM_V_at)$(INSTALL_DATA) $(firmware_binaries) $(distdir_bin)
	$(AM_V_at)$(INSTALL_DATA) $(srcdir)/COPYING $(srcdir)/COPYING.LESSER $(srcdir)/NEWS $(srcdir)/README $(distdir_bin)
	$(AM_V_at)if test -d '$(top_srcdir)/.git'; \
	then git -C '$(top_srcdir)' log > $(distdir_bin)/ChangeLog; \
	else $(INSTALL_DATA) $(srcdir)/ChangeLog $(distdir_bin); fi
	$(AM_V_at)tar -czf $(distdir_bin).tar.gz $(distdir_bin)
	-$(AM_V_at)rm -fr $(distdir_bin)

# List dependencies
$(fx2adf435xfw_objects): $(fx2adf435xfw_headers)
$(fx2lib_objects): fx2lib/lib/$(dirstamp) $(fx2lib_headers)
$(fx2lib_ints_objects): fx2lib/lib/interrupts/$(dirstamp) $(fx2lib_headers)

# Create build subdirectories
$(dirstamps):
	@stamp='$@'; $(MKDIR_P) "$${stamp%/*}"
	@: > $@

fx2lib/lib/fx2.lib: $(fx2lib_objects)
	-$(AM_V_at)rm -f $@
	$(AM_V_GEN)$(SDAR) -rc $@ $(fx2lib_objects)

fx2lib/lib/interrupts/ints.lib: $(fx2lib_ints_objects)
	-$(AM_V_at)rm -f $@
	$(AM_V_GEN)$(SDAR) -rc $@ $(fx2lib_ints_objects)

fx2adf435xfw.ihx: $(fx2adf435xfw_objects) $(fx2lib_libs)
	$(AM_V_GEN)$(SDCC) -mmcs51 $(SDCC_LINK_FLAGS) -o $@ $(fx2adf435xfw_objects) $(fx2lib_libs)

.a51.rel:
	$(SF_V_SDAS)$(SDAS8051) -glos $(as_includes) $@ $<

.c.rel:
	$(SF_V_SDCC)$(SDCC) -mmcs51 $(c_includes) -c $< -o $@

if FOUND_OBJCOPY
.ihx.fw:
	$(AM_V_GEN)$(OBJCOPY) -Iihex $< -Obinary $@
else
if FOUND_MAKEBIN
.ihx.fw:
	$(AM_V_GEN)$(MAKEBIN) -p < $< > $@
endif
endif

