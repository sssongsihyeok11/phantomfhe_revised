#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "phantom::Phantom" for configuration ""
set_property(TARGET phantom::Phantom APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(phantom::Phantom PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libPhantom.so"
  IMPORTED_SONAME_NOCONFIG "libPhantom.so"
  )

list(APPEND _cmake_import_check_targets phantom::Phantom )
list(APPEND _cmake_import_check_files_for_phantom::Phantom "${_IMPORT_PREFIX}/lib/libPhantom.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
