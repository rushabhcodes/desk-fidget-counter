# Firmware dependencies

Firmware 6.0.0 uses the original Raspberry Pi Pico SDK 2.2.0 startup, boot2, clock, peripheral and runtime code, plus TinyUSB 0.21.0. Full upstream BSD3/MIT notices are retained in `licenses/` and the dependency trees fetched by `bootstrap.sh`. The original BSD3 notice is also retained at the top of `quadrature_encoder.pio`, taken from Raspberry Pi's official pico-examples quadrature encoder program. No vendor dependency source is patched.

The bootstrap records and verifies the SDK/TinyUSB commit IDs and Arm GNU compiler archive SHA256. Arm GNU's toolchain licences and runtime exceptions remain in the downloaded `.deps/toolchain/` distribution; the toolchain itself is not republished in the fabrication package.
