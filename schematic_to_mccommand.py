#!/usr/bin/env python
# -*- coding: utf-8 -*-

from blockmodel import BlockModel
from blockmodel.mapper import MinecraftBlockMapper


class Command(BlockModel):
    def __init__(self, reader):
        super().__init__(reader)
        self.commands

    # Tinkercad uses only 36 ids
    block_names = {
        1: "stone",
        3: "dirt",
        7: "bedrock",
        9: "water",
        10: "flowing_lava",
        17: "log",
        18: "leaves",
        19: "sponge",
        21: "lapis_ore",
        22: "lapis_block",
        24: "sandstone",
        41: "gold_block",
        42: "iron_block",
        45: "brick_block",
        46: "tnt",
        49: "obsidian",
        56: "diamond_ore",
        57: "diamond_block",
        73: "redstone_ore",
        79: "ice",
        80: "snow",
        86: "pumpkin",
        87: "netherrack",
        88: "soul_sand",
        89: "glowstone",
        129: "emerald_ore",
        133: "emerald_block",
        138: "beacon",
        152: "redstone_block",
        155: "quartz_block",
        159: "stained_hardened_clay",
        162: "log2",
        165: "slime",
        168: "prismarine",
        172: "hardened_cray",
        174: "packed_ice"
    }

    def print_com(self, x1, y1, z1, x2, y2, z2, blockname):
        return "fill %d %d %d %d %d %d minecraft:%s\n" % (x1, y1, z1, x2, y2, z2, blockname)

    def _as_command(self):
        # Origin
        origin_x = 84
        origin_y = 63
        origin_z = 124

        bufs = []
        for z in range(self.depth + 1):
            commands = []
            for x in range(self.width + 1):
                sv_y = -1
                for y in range(self.height + 1):
                    block_id, block_data = self.reader.get(
                        x, self.height - y, z)
                    if block_id != 0:
                        if sv_y == -1:
                            sv_y = self.height - y
                        blockname = self.block_names[block_id]
                    else:
                        if sv_y != -1:
                            commands.append(
                                self.print_com(x+origin_x, sv_y+origin_y, z+origin_z, x+origin_x, self.height - y + origin_y+1, z+origin_z, blockname))
                        sv_y = -1
                if sv_y != -1:
                    commands.append(
                        self.print_com(x+origin_x, sv_y+origin_y, z+origin_z, x+origin_x, self.height - y + origin_y, z+origin_z, blockname))
            bufs.append("".join(commands))

        return "".join(bufs)

    commands = property(_as_command)


file_name = "budha"
command = Command.from_schematic_file(file_name + ".schematic")
with open(file_name + ".txt", "w") as f:
    f.write(command.commands)
