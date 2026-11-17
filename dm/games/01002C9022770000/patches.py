# Trails in the Sky 1st Chapter (01002C9022770000): the rewriter's patches of this game's own builds.
# dm/tools/patch_nso.py loads every profile's patches.py; MATCH_CUTS as described there ("Registered
# patches"). Patches of Nintendo SDK module builds are in dm/tools/sdk_patches.py.
#
# 1.0.7 main: Falcom's SORA engine gives its "native allocator" a virtual address region of ten times the
# allocator's own capacity. In the reviewed build below, main+0x56c1a4 is `fmov d0,#10.0`; the capacity
# is 0x48200000, and the product is rounded up to 2 MB: 0x2d1400000 (11.27 GiB of virtual address
# space). The engine only maps what it uses (about 0.4 GB through the opening), so a factor of 3
# (0x2d1400000 / 10 * 3 = 3.38 GiB) is enough and fits the alias region of the iPhone profile in
# game.tsv. The reservation is virtual address space only; the pages it commits come from the alias
# region and the memory the game actually uses (a 2.02 GB heap) is reported separately.
#
# The cut was reviewed on the only 1.0.7 main available in this checkout, the Korean/Asian build
# 4f4fd1aed39eb96a649aba489ad3767d (function at main+0x56c120, cut at +0x84). The international 1.0.7
# update NSP (build 8963a531fa7f27a52323081ace0f2f6e) is not in the checkout, so that build's exact
# offset is not known here and is deliberately not written down: the rule finds the 656-byte allocator
# function by size and SHA-256 fingerprint (dm/tools/nso_match.py) on any build that carries it
# unchanged, and a miss is a red line rather than a cut at the wrong address. Pin the offset with a
# build-keyed CUTS entry once a dump of that main is at hand.
CUTS = {}

MATCH_CUTS = {'main': [
    {'name': 'virtual address reservation',
     'size': 656,
     'fingerprints': ['44493ad09e5fbd1ceeefa51ff48ac812553878c36b108a35a4d35021563c0411'],
     'cuts': [
         (132, '0090641e', '0010611e',
          'virtual address reservation: fmov d0,#10.0 -> fmov d0,#3.0 (11.27 GiB -> 3.38 GiB)'),
     ]},
]}

# How general each patch is and could be (dm/tools/docs_patches.py "Binding", listed in
# docs/agents/game-patches.md): what, its binding now, the loosest it could have (goal), purpose, why;
# blocked or kept: why the gap stays open (cannot close yet, or left open on purpose); checked: what was
# checked on game files (else a judgement)
BINDING = [
    {'what': 'virtual address reservation', 'now': 'game', 'goal': 'game',
     'purpose': 'address space',
     'why': 'the engine only maps what it uses; 3x is 3.38 GiB, inside the 3.46875 GiB alias region. '
            'The exact 8963a531 offset is not pinned: its update NSP is missing here, so the cut is '
            'function-matched and fails closed',
     'checked': 'the rule locates main+0x56c1a4 once on 4f4fd1ae (Korean/Asian 1.0.7); 8963a531 is '
                'not in this checkout'},
]
