#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019-2020 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import Xilinx7SeriesPlatform, VivadoProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk125", 0, Pins("K17"), IOStandard("LVCMOS33")),

    # Leds
    ("user_led", 0, Pins("M14"), IOStandard("LVCMOS33")),
    ("user_led", 1, Pins("M15"), IOStandard("LVCMOS33")),
    ("user_led", 2, Pins("G14"), IOStandard("LVCMOS33")),
    ("user_led", 3, Pins("D18"), IOStandard("LVCMOS33")),

    # Switches
    ("user_sw", 0, Pins("G15"), IOStandard("LVCMOS33")),
    ("user_sw", 1, Pins("P15"), IOStandard("LVCMOS33")),
    ("user_sw", 2, Pins("W13"), IOStandard("LVCMOS33")),
    ("user_sw", 3, Pins("T16"), IOStandard("LVCMOS33")),

    # Buttons
    ("user_btn", 0, Pins("R18"), IOStandard("LVCMOS33")),
    ("user_btn", 1, Pins("P16"), IOStandard("LVCMOS33")),
    ("user_btn", 2, Pins("V16"), IOStandard("LVCMOS33")),
    ("user_btn", 3, Pins("Y16"), IOStandard("LVCMOS33")),

    # Serial
    ("serial", 0,
        Subsignal("tx", Pins("T17")),
        Subsignal("rx", Pins("Y17")),
        IOStandard("LVCMOS33")
    ),
]

_ps7_io = [
    # PS7
    ("ps7_clk",   0, Pins(1)),
    ("ps7_porb",  0, Pins(1)),
    ("ps7_srstb", 0, Pins(1)),
    ("ps7_mio",   0, Pins(54)),
    ("ps7_ddram", 0,
        Subsignal("addr",    Pins(15)),
        Subsignal("ba",      Pins(3)),
        Subsignal("cas_n",   Pins(1)),
        Subsignal("ck_n",    Pins(1)),
        Subsignal("ck_p",    Pins(1)),
        Subsignal("cke",     Pins(1)),
        Subsignal("cs_n",    Pins(1)),
        Subsignal("dm",      Pins(4)),
        Subsignal("dq",      Pins(32)),
        Subsignal("dqs_n",   Pins(4)),
        Subsignal("dqs_p",   Pins(4)),
        Subsignal("odt",     Pins(1)),
        Subsignal("ras_n",   Pins(1)),
        Subsignal("reset_n", Pins(1)),
        Subsignal("we_n",    Pins(1)),
        Subsignal("vrn",     Pins(1)),
        Subsignal("vrp",     Pins(1)),
    ),
]

_usb_uart_pmod_io = [
    # USB-UART PMOD on JB:
    # - https://store.digilentinc.com/pmod-usbuart-usb-to-uart-interface/
    ("usb_uart", 0,
        Subsignal("tx", Pins("pmodb:1")),
        Subsignal("rx", Pins("pmodb:2")),
        IOStandard("LVCMOS33")
    ),
]

# Connectors ---------------------------------------------------------------------------------------

_connectors = [
    ("pmoda", "N15 L14 K16 K14 N16 L15 J16 J14"), # XADC
    ("pmodb", "V8  W8  U7  V7  Y7  Y6  V6  W6"),
    ("pmodc", "V15 W15 T11 T10 W14 Y14 T12 U12"),
    ("pmodd", "T14 T15 P14 R14 U14 U15 V17 V18"),
    ("pmode", "V12 W16 J15 H15 V13 U17 T17 Y17"),
]

ps7_config = {
    "z7-20" : {
        "PCW_UIPARAM_DDR_PARTNO"        : "MT41K256M16 RE-125",
        "PCW_FPGA_FCLK0_ENABLE"         : "1",
        "PCW_UART1_BAUD_RATE"           : "115200",
        "PCW_EN_UART1"                  : "1",
        "PCW_UART1_PERIPHERAL_ENABLE"   : "1",
        "PCW_UART1_UART1_IO"            : "MIO 48 .. 49",
        "PCW_PRESET_BANK1_VOLTAGE"      : "LVCMOS 1.8V",
        "PCW_USE_M_AXI_GP0"             : "1",
        "PCW_USE_S_AXI_GP1"             : "1",
        "PCW_USE_S_AXI_GP0"             : "1",
        "PCW_USB0_PERIPHERAL_ENABLE"    : "1",
        "PCW_USB0_USB0_IO"              : "MIO 28 .. 39",
        "PCW_USB0_RESET_ENABLE"         : "1",
        "PCW_USB0_RESET_IO"             : "MIO 46",
        "PCW_EN_USB0"                   : "1"
    }
}
# Platform -----------------------------------------------------------------------------------------

class Platform(Xilinx7SeriesPlatform):
    default_clk_name   = "clk125"
    default_clk_period = 1e9/125e6

    def __init__(self, variant="z7-20", toolchain="vivado"):
        device = {
            "z7-10": "xc7z010-clg400-1",
            "z7-20": "xc7z020-clg400-1"
        }[variant]
        Xilinx7SeriesPlatform.__init__(self, device, _io,  _connectors, toolchain=toolchain)
        self.add_extension(_ps7_io)
        self.add_extension(_usb_uart_pmod_io)
        self.ps7_config = ps7_config[variant]

    def create_programmer(self):
        return VivadoProgrammer()

    def do_finalize(self, fragment):
        Xilinx7SeriesPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("clk125", loose=True), 1e9/125e6)
