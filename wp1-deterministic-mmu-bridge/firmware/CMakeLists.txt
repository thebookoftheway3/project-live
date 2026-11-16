# SPDX-License-Identifier: AGPL-3.0-only
cmake_minimum_required(VERSION 3.20.0)
# NCS owns the board definitions; see hardware-vendor/MANIFEST.md for the pin.
set(DTC_OVERLAY_FILE "${CMAKE_CURRENT_SOURCE_DIR}/../hardware-vendor/overlays/thingy91x_nrf5340_cpuapp.overlay")
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(live_thingy91x C)
set_property(TARGET app PROPERTY C_STANDARD 99)
set_property(TARGET app PROPERTY C_STANDARD_REQUIRED ON)
target_sources(app PRIVATE src/main.c src/conflict_monitor.c)
