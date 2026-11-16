#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
build_dir=$(mktemp -d)
trap 'rm -rf "$build_dir"' EXIT HUP INT TERM
"${CXX:-c++}" -std=c++17 -Wall -Wextra -Werror -pedantic \
    -Iwp1-deterministic-mmu-bridge/firmware \
    wp1-deterministic-mmu-bridge/firmware/*.cpp \
    wp1-deterministic-mmu-bridge/tests/test_mmu_invariants.cpp \
    -o "$build_dir/test_mmu"
"$build_dir/test_mmu"
