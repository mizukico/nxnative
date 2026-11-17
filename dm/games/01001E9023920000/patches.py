# Trails in the Sky 1st Chapter, Korean/Asian release (01001E9023920000): the rewriter's patches of
# this game's own builds. dm/tools/patch_nso.py loads every profile's patches.py and applies those of
# a module's NSO build ID ("Registered patches"); CUTS, OBS and FRAME_STEP as described there.
CUTS = {
  # 1.0.7 (v458752) main: Falcom's SORA engine gives its "native allocator" a virtual address region of
  # ten times the allocator's own capacity (main+0x56c1a4 fmov d0,#10.0: capacity 0x48200000, rounded
  # up to 2 MB, 0x2d1400000 = 12.1 GB). On the Switch the alias region is 64 GB, but the engine only
  # maps what it uses (about 0.4 GB through the opening), so the iPhone profile in game.tsv cuts the
  # factor to 2 (2.26 GiB).
  # The alias region is shared with the SDK: its AddressRegionManager takes the node area 0x3fe00000
  # (0.999 GiB) at the start of the 3.46875 GiB region, and this sdk build (14839413) has no
  # node-area cut registered in dm/tools/sdk_patches.py, so 2.47 GiB is left to hand out. A factor of
  # 3 asked for 3.38 GiB and the first AllocateAddressRegion failed on an iPhone with 0x1803 (the
  # game's own "failed to reserve virtual address" line, then CRASH sig=11 in sdk+0x15576c), which
  # a factor of 2 fits with 0.21 GiB to spare.
  # The reservation is virtual address space only: the pages it commits come from the alias region and
  # the memory the game actually uses is reported separately (a 2.02 GB heap).
  '4f4fd1aed39eb96a649aba489ad3767d': [
    (0x56c1a4, '0090641e', '0010601e',
     'virtual address reservation: fmov d0,#10.0 -> fmov d0,#2.0 (11.27 GiB -> 2.26 GiB)'),
  ],
}

# The same 656-byte allocator function (main+0x56c120 on 4f4fd1ae, cut at +0x84) carries the same
# SHA-256 fingerprint 44493ad09e5fbd1ceeefa51ff48ac812553878c36b108a35a4d35021563c0411. A future
# build can be enrolled with dm/tools/nso_match.py instead of a copied offset; this profile pins the
# reviewed 1.0.7 build exactly.

# How general each patch is and could be (dm/tools/docs_patches.py "Binding", listed in
# docs/agents/game-patches.md): what, its binding now, the loosest it could have (goal), purpose, why;
# blocked or kept: why the gap stays open (cannot close yet, or left open on purpose); checked: what was
# checked on game files (else a judgement)
BINDING = [
    {'what': 'virtual address reservation', 'now': 'build', 'goal': 'game',
     'purpose': 'address space',
     'why': 'the engine only maps what it uses; 2x is 2.26 GiB, and the 3.46875 GiB alias region '
            'leaves 2.47 GiB after the SDK node area (3x, 3.38 GiB, failed with 0x1803 on an iPhone)',
     'blocked': 'this profile packs the reviewed 1.0.7 build only; a future build needs its own offset '
                'or the function-matched rule from the same 656-byte function',
     'checked': 'the exact 1.0.7 main (4f4fd1ae): fmov d0,#10.0 at main+0x56c1a4, original bytes '
                '0090641e; the 656-byte function also locates once by fingerprint'},
]
