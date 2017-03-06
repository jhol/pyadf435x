from math import ceil, floor, log


class DeviceType:
    ADF4350 = 0,
    ADF4351 = 1


class LowNoiseSpurMode:
    LowNoiseMode = 0
    LowSpurMode = 1


class MuxOut:
    ThreeState = 0
    DVdd = 1
    DGND = 2
    RCounterOuput = 3
    NDividerOutput = 4
    AnalogLockDetect = 5
    DigitalLockDetect = 6


class PDPolarity:
    Negative = 0
    Positive = 1


class BandSelectClockMode:
    Low = 0
    High = 1


class ClkDivMode:
    ClockDividerOff = 0
    FastLockEnable = 1
    ResyncEnable = 2


class FeedbackSelect:
    Divider = 0
    Fundamental = 1


class AuxOutputSelect:
    DividedOutput = 0
    Fundamental = 1


class LDPinMode:
    Low = 0
    DigitalLockDetect = 1
    High = 3


def calculate_regs(
        device_type=DeviceType.ADF4351,
        freq=50.0,
        ref_freq=25.0,
        r_counter=1,
        ref_doubler=False,
        ref_div2=False,
        feedback_select=FeedbackSelect.Fundamental,
        band_select_clock_divider=None,
        band_select_clock_mode=BandSelectClockMode.Low,
        enable_gcd=True):
    def gcd(a, b):
        while True:
            if a == 0:
                return b
            elif b == 0:
                return a
            elif a > b:
                a = a % b
            else:
                b = b % a


    pfd_freq = ((ref_freq * (2 if ref_doubler else 1)) /
        ((2 if ref_div2 else 1) * r_counter))

    for log2_output_divider in range(7):
        output_divider = 2 ** log2_output_divider
        if 2200.0 / output_divider <= freq:
            break

    if feedback_select == FeedbackSelect.Fundamental:
        N = freq * output_divider / pfd_freq
    else:
        N = freq / pfd_freq

    INT = int(floor(N))
    MOD = int(round(1000.0 * pfd_freq))
    FRAC = int(round((N - INT) * MOD))

    if enable_gcd:
        div = gcd(MOD, FRAC)
        MOD = MOD / div
        FRAC = FRAC / div

    if MOD == 1:
        MOD = 2

    if pfd_freq > 32.0:
        if FRAC != 0:
            raise ValueError('Maximum PFD frequency in Frac-N mode (FRAC != 0)'
                    ' is 32MHz.')
        if FRAC == 0 and device_type == DeviceType.ADF4351:
            if pfd_freq > 90.0:
                raise ValueError('Maximum PFD frequency in Int-N mode '
                        '(FRAC = 0) is 90MHz.')
            if band_select_clock_mode == BandSelectClockMode.Low:
                raise ValueError('Band Select Clock Mode must be set to High '
                        'when PFD is >32MHz in Int-N mode (FRAC = 0).')

    if not band_select_clock_divider:
        pfd_scale = 8 if band_select_clock_mode == BandSelectClockMode.Low else 2
        if band_select_clock_mode == BandSelectClockMode.Low:
            band_select_clock_divider = min(ceil(8 * pfd_freq), 255)

    band_select_clock_freq = 1000.0 * pfd_freq / band_select_clock_divider

    if band_select_clock_freq > 500.0:
        raise ValueError('Band Select Clock Frequency is too High. It must be '
                '500kHz or less.')
    elif band_select_clock_freq > 125.0:
        if device_type == DeviceType.ADF4351:
            if band_select_clock_mode == BandSelectClockMode.Low:
                raise ValueError('Band Select Clock Frequency is too high. '
                        'Reduce to 125kHz or less, or set Band Select Clock '
                        'Mode to High.')
        else:
            raise ValueError('Band Select Clock Frequency is too high. Reduce '
                    'to 125kHz or less.')

    return (int(INT), int(MOD), int(FRAC), output_divider, band_select_clock_divider)


def make_regs(
        device_type=DeviceType.ADF4351,
        INT=100,
        FRAC=0,
        MOD=2,
        phase_value=None,
        band_select_clock_divider=200,
        band_select_clock_mode=BandSelectClockMode.Low,
        prescaler='8/9',
        low_noise_spur_mode=LowNoiseSpurMode.LowNoiseMode,
        mux_out=MuxOut.ThreeState,
        ref_doubler=False,
        ref_div_2=False,
        r_counter=1,
        double_buff_r4=False,
        charge_pump_current=2.50,
        ldp=10.0,
        pd_polarity=PDPolarity.Positive,
        powerdown=False,
        cp_three_state=False,
        counter_reset=False,
        abp=10,
        charge_cancel=False,
        csr=False,
        clk_div_mode=ClkDivMode.ClockDividerOff,
        clock_divider_value=150,
        feedback_select=FeedbackSelect.Fundamental,
        output_divider=1,
        vco_powerdown=False,
        mute_till_lock_detect=False,
        aux_output_select=AuxOutputSelect.DividedOutput,
        aux_output_enable=False,
        aux_output_power=-4.0,
        output_enable=True,
        output_power=5.0,
        ld_pin_mode=LDPinMode.DigitalLockDetect):

    ChargePumpCurrent = {0.31:0, 0.63:1, 0.94:2, 1.25:3,
            1.56:4, 1.88:5, 2.19:6, 2.50:7,
            2.81:8, 3.13:9, 3.44:10, 3.75:11,
            4.06:12, 4.38:13, 4.49:14, 5.00:15}
    ABP = {10:0, 6:0}
    OutputPower = {-4:0, -1:1, +2:2, +5:3}

    def check_uint_val(val_name, val, max):
        if type(val) != int or val < 0 or val > max:
            raise ValueError('%s value must be an integer greater than or '
                    'equal to 0, and less than %d' % (val_name, max))

    def check_lookup_val(val_name, val, lut):
        if val not in lut.keys():
            raise ValueError('%s value must be one of the following: %r' %
                    (val_name, lut.keys()))

    check_uint_val('INT', INT, 65535)
    check_uint_val('FRAC', FRAC, 4095)
    check_uint_val('MOD', MOD, 4095)
    check_lookup_val('charge_pump_current', charge_pump_current,
            ChargePumpCurrent)
    check_lookup_val('abp', abp, ABP)
    check_lookup_val('aux_output_power', aux_output_power, OutputPower)
    check_lookup_val('output_power', output_power, OutputPower)

    output_divider_select = int(log(output_divider, 2))
    if (output_divider_select < 0 or output_divider_select > 64 or
            floor(output_divider_select) != output_divider_select):
        raise ValueError('Output Divider must be a positive integer power of '
            '2, not greater than 64.')

    regs = [0] * 6

    # R0
    regs[0] = (INT << 15 |
        FRAC << 3 |
        0x0)

    # R1
    regs[1] = ((1 if phase_value != None else 0) << 28 |
        (1 if prescaler == '8/9' else 0) << 27 |
        (1 if phase_value == None else phase_value) << 15 |
        MOD << 3 |
        0x1)
    if device_type == DeviceType.ADF4351:
        regs[1] |= (1 if phase_value != None else 0) << 28

    # R2
    regs[2] = (low_noise_spur_mode << 29 |
        mux_out << 26 |
        (1 if ref_doubler else 0) << 25 |
        (1 if ref_div_2 else 0) << 24 |
        r_counter << 14 |
        (1 if double_buff_r4 else 0) << 13 |
        ChargePumpCurrent[charge_pump_current] << 9 |
        (0 if FRAC == 0 else 1)  << 8 |
        (0 if ldp == 10.0 else 1) << 7 |
        pd_polarity << 6 |
        (1 if powerdown else 0) << 5 |
        (1 if cp_three_state else 0) << 4 |
        (1 if counter_reset else 0) << 3 |
        0x2)

    # R3
    regs[3] = ((1 if csr else 0) << 18 |
        clk_div_mode << 15 |
        clock_divider_value << 3 |
        0x3)
    if device_type == DeviceType.ADF4351:
        regs[3] |= ((band_select_clock_mode << 23 |
            ABP[abp] << 22 |
            (1 if charge_cancel else 0) << 21))

    # R4
    regs[4] = (feedback_select << 23 |
        output_divider_select << 20 |
        band_select_clock_divider << 12 |
        (1 if vco_powerdown else 0) << 11 |
        (1 if mute_till_lock_detect else 0) << 10 |
        aux_output_select << 9 |
        (1 if aux_output_enable else 0) << 8 |
        OutputPower[aux_output_power] << 6 |
        (1 if output_enable else 0) << 5 |
        OutputPower[output_power] << 3 |
        0x4)

    # R5
    regs[5] = (ld_pin_mode << 22 |
        3 << 19 |
        0x5)

    return regs
