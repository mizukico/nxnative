# Trails in the Sky 1st Chapter (`01001E9023920000`)

The Korean/Asian release, update 1.0.7 (v458752), SDK 19.3.13, Falcom's SORA engine on NVN. Modules
`main`, `subsdk0` (NintendoSDK_movie) and `sdk`. The international release is the separate
[`01002C9022770000`](../01002C9022770000/README.md) profile; this one is built from the Korean update
NSP (`[UPD][v1.0.7][01001E9023920800][v458752].nsp`).

## What it needs

| Setting | Why |
|---|---|
| `mem_reserve 0x180000000`, `mem_alias 0xDE000000` | The engine reserves ten times its allocator capacity in virtual address space; [`patches.py`](patches.py) cuts the factor to two (2.26 GiB). The 3.46875 GiB alias region is shared with the SDK's node area (`0x3fe00000`, 0.999 GiB, and this `sdk` build has no node-area cut registered), which leaves 2.47 GiB to hand out; a factor of three asked for 3.38 GiB and the first `AllocateAddressRegion` failed on an iPhone with `0x1803` (CRASH `sig=11` in `sdk+0x15576c`, 2026-11-17). The block is 6 GiB, the iPhone's single-reservation limit without extended virtual addressing: 256 MB in front, the alias region, 256 MB of stacks and a 2.03125 GiB heap region (the 0x81200000 heap request fits). |
| `sys_resource 0x1000000` | The NPDM declares 16 MB of system resource. |
| `depth_mode zero` | At boot the game sets near depth to zero; prebuilt vertex pipelines must use `main0_z`. |
| `shader_groups` | GLSLC compiler outputs are under `/asset/nx/shader`; the split keeps the Korean/Chinese asset folder names. |

The registered build is `4f4fd1aed39eb96a649aba489ad3767d` (1.0.7, v458752). The reservation cut is
`main+0x56c1a4`: `0090641e` (`fmov d0,#10.0`) becomes `0010601e` (`fmov d0,#2.0`); the 656-byte
allocator function starts at `main+0x56c120`. (`0010611e`, the three-times cut this profile first
shipped with, is what the iPhone rejected.)

## Files and shaders

- RomFS marker: `movie_sc/mp4/sora_1st_ed.mp4`.
- The shader map has 6,602 entries: 1,271 vertex, 5,294 pixel and 37 compute, all GLSLC compiler
  outputs in `/asset/nx/shader/*.nvn` and in `main`.
- The tables are from the 1.0.7 update; the base 1.0.0 and update 1.0.7 NSPs are in the game's NSP
  folder, outside this repository.
- The tables were split again with the current `dm/gfx/tools/shader_split.py` from that extraction
  (build `4f4fd1aed39eb96a649aba489ad3767d`). The profile's first copy came from an older splitter,
  which keyed `/asset/nx/shader/light_cull.nvn` as `ece8145773ee095d` rather than `f9def5d93748a39f`,
  `main`'s compute kernel as `aecb69afbb394ff9` rather than `a370ad7eceb0897a`, and put `main`'s
  GLSLC vertex shader at `0x62f804` rather than `0x625130`; the split also writes the `#` header lines
  and the `package/index/stage/dm_ctl_sha16/source` column header the profile lacked.

## Status

- The 6 GiB layout and the two-times reservation cut are sized for an iPhone without the extended
  virtual addressing entitlement.
- Device booted 2026-11-17 (the CI's Korean 1.0.7 IPA, its `RomFS.img` pushed): the game reached
  `nnosInitialize`, opened its 2.02 GB heap and ran `main`'s initializers, then the native
  allocator's address-space reservation failed with `0x1803` under the three-times cut, followed by
  `CRASH sig=11 pc=sdk+0x15576c`. The cut is now two times (2.26 GiB), which fits the 2.47 GiB the
  alias region has left after the SDK's 1 GB node area. **A device boot of that build is the next
  step.** If the allocator later exhausts 2.26 GiB, the next lever is the `sdk` node-area cut
  (1 GB to 62 MB, `dm/tools/sdk_patches.py`) for the `sdk` build `148394139d9d26ca8afd5c9ba5d30601`,
  which would widen the alias region's usable part to 3.41 GiB.
