# Machine-Code-Converter
项目简介
本项目是一个基于 Python 实现的 RISC-V 汇编器（Assembler），用于将汇编语言代码自动转换为对应的机器码。
它支持 RISC-V 指令集中的多种指令格式（R、I、S、SB、U、UJ 类型），并实现了常见伪指令（如 li、mv、nop 等）的自动解析与转换。

主要功能

支持 RISC-V 核心指令类型：R / I / S / SB / U / UJ

实现伪指令到真实指令的展开与编码

输出机器码的二进制或十六进制表示

包含多组示例汇编文件与单元测试脚本

模块化设计，核心代码集中在 assembler.py 与 pseudoinstruction_handler.py
