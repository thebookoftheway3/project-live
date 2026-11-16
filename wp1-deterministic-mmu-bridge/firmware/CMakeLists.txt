# Bench model can be compiled as an ESP-IDF component; no app_main/device driver.
idf_component_register(
    SRCS "conflict_monitor.cpp" "basal_ledger.cpp" "ble_dual_manager.cpp" "ltem_failover.cpp"
    INCLUDE_DIRS "."
)
target_compile_features(${COMPONENT_LIB} PUBLIC cxx_std_17)
