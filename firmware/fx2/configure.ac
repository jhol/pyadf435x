##
## This file is part of the pyadf435x project.
##
## Copyright (C) 2013 Uwe Hermann <uwe@hermann-uwe.de>
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

# We require at least autoconf 2.63 (AC_INIT format changed there).
AC_PREREQ([2.63])

AC_INIT([fx2adf4351fw], [0.1])
AC_CONFIG_AUX_DIR([autostuff])

# We require at least automake 1.11 (needed for 'silent rules').
AM_INIT_AUTOMAKE([1.11 -Wall -Werror no-define subdir-objects check-news])
AM_SILENT_RULES([yes])

AC_PROG_INSTALL
AC_PROG_LN_S

# On Fedora, all sdcc tools have an 'sdcc-' prefix in the filename.
AC_CHECK_PROGS([SDCC], [sdcc sdcc-sdcc])
AS_IF([test "x$SDCC" = x],
	[AC_MSG_ERROR([cannot find sdcc.])])

AC_CHECK_PROGS([SDAR], [sdar sdcc-sdar])
AS_IF([test "x$SDAR" = x],
	[AC_MSG_ERROR([cannot find sdar.])])

sf_sdcc_version=`$SDCC --version | sed -n 's/.* \([[0-9]][[0-9]]*\.[[0-9]][[0-9]]*\.[[0-9]][[0-9]]*\) .*/\1/p;q' 2>&AS_MESSAGE_LOG_FD`
AS_VERSION_COMPARE([$sf_sdcc_version], [2.9.0],
	[AC_MSG_ERROR([At least version 2.9.0 of sdcc is required.])])

AC_CHECK_PROGS([OBJCOPY], [objcopy])
AC_CHECK_PROGS([MAKEBIN], [makebin sdcc-makebin])
AS_IF([test "x$OBJCOPY$MAKEBIN" = x],
	[AC_MSG_ERROR([cannot find objcopy or makebin.])])

AM_CONDITIONAL([FOUND_OBJCOPY], [test "x$OBJCOPY" != x])
AM_CONDITIONAL([FOUND_MAKEBIN], [test "x$MAKEBIN" != x])

# The sdcc 8051 assembler binary has/had different names:
# Newer sdcc, Debian / Ubuntu: sdas8051
# Newer sdcc, Fedora: sdcc-sdas8051
# Older sdcc: asx8051
AC_CHECK_PROGS([SDAS8051], [sdas8051 sdcc-sdas8051 asx8051])
AS_IF([test "x$SDAS8051" = x],
	[AC_MSG_ERROR([cannot find sdas8051.])])

AC_CONFIG_FILES([Makefile])
AC_OUTPUT

cat >&AS_MESSAGE_FD <<_EOF

fx2adf4351fw configuration summary:
 - Package version................. $PACKAGE_VERSION
 - Prefix.......................... $prefix

Compile configuration:
 - C compiler...................... $SDCC
 - C compiler version.............. $sf_sdcc_version

_EOF
