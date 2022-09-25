# rpi4-i2c-userspace-rpm
An set of 3 RPMs that configure a RPI4 i2c for userspace use.

- `rpi4-i2c-userspace` - configures i2c to be enabled and makes an i2c group
- `rpi4-i2c-userspace-i2c0` - configures the i2c0 port to be enabled
- `rpi4-i2c-userspace-i2c1` - configures the i2c1 port to be enabled

Then add your user to the i2c group, reboot and you're ready to go as non-root.

```bash
groupadd -U ${USER} i2c
```

## Building

```bash
rpmbuild -ba rpi4-i2c-userspace.spec
```
