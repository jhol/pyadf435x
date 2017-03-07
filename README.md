pyadf435x
=========

`pyadf435x` is a suite of software and firmware for controlling the Analog
Devices ADF435x series of wide-band RF synthesizers.

The software suite consists of the following components:

* **adf435x** - A python library that can control the ADF4350/1 via various
  hardware interface back-ends.
* **adf435xctl** - A command line tool to control the ADF4350/1 manually.
* **fx2adf435xfw** - A firmware for the Cypress FX2 that replaces the
  proprietary firmware for the EVAL-ADF4351 board.

adf435x
-------

### Installation

1. Install depedencies:

   On Debian/Ubuntu:
   ```
   $ sudo apt install python3-setuptools python3-usb
   ```

2. Build the python module:
   ```
   $ python3 setup.py build
   ```

3. Install the python module:
   ```
   $ sudo python3 setup.py install
   ```

4. (Optional) Install udev rules:
   ```
   $ sudo cp contrib/z60_adf435x.rules /etc/udev/rules.d/
   ```

### Usage

See `examples/` sub-directory.

adf435xctl
----------

Requires **adf435x** to be installed.

### Usage Examples

Sets the output frequency to 1000MHz:

```
./adf435x --freq=1000
```

fx2adf435xfw
------------

The Cypress FX2 firmware project controls the synthesizer over SPI by
bit-banging the FX2's GPIOs.

The firmware requires the following wiring:

|  FX2 Pin  |  ADF4350/1 Pin  |
|  -------  |  -------------  |
|  PA0      |  LE             |
|  PA1      |  CLK            |
|  PA2      |  DAT            |

### Building

1. First init/update all the sub-modules within the git repository:
   ```
   $ git submodule update --init
   ```

2. Install AutoTools and the SDCC (Small Devices C Compiler).

   On Debian/Ubuntu:
   ```
   $ sudo apt install autoconf automake make sdcc
   ```

3. Build the firmware:
   ```
   $ ./autogen.sh
   $ ./configure
   $ make
   ```
   You will now have the firmware file `fx2adf435xfw.ihx`

### Usage

1. Install *cycfx2prog*.

   On Debian/Ubuntu:
   ```
   $ sudo apt install cycfx2prog
   ```

2. Load the firware on to the Cypress FX2 with the following command:
   ```
   $ cycfx2prog prg:./firmware/fx2/fx2adf435xfw.ihx
   ```

3. Run the firmware:
   ```
   $ cycfx2prog run
   ```
   The device will no renumerate as with the VID/PID `0456:b40d`, as an Analog
   Devices board.
