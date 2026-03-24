# Ultimate Guide
## Design and Optimization of a 5-Stage RISC Processor with DSP Instruction Extension (Software Simulation)

Version: 1.0  
Prepared for: ECE Minor Project (3rd Year)  
Project Type: VLSI + Computer Architecture + DSP-Oriented Extension

---

## 1. Executive Summary

This project starts from a classic 5-stage pipelined RISC processor and extends it with a DSP-oriented instruction set feature: a Multiply-Accumulate (MAC) instruction. The baseline processor already includes hazard handling and forwarding. The extension adds a MAC execution path in the EX stage, updates control decoding, and evaluates performance on signal-processing workloads.

The full implementation is software-only (RTL simulation). No FPGA board is required.

---

## 2. Why This Project Is Strong

1. It demonstrates core architecture concepts used in real CPUs.
2. It shows practical pipeline optimization (CPI, stalls, forwarding efficiency).
3. It introduces domain-specific acceleration (DSP extension).
4. It creates a clear "before vs after" performance story.
5. It is suitable for VLSI interviews, architecture discussions, and ECE project evaluation.

---

## 3. Problem Statement

General-purpose RISC instructions execute DSP kernels (FIR, convolution) with high instruction count. MAC-heavy loops spend extra cycles on separate MUL + ADD + ACC operations.

Target: reduce cycle count and improve throughput by executing multiply-and-accumulate behavior through a single DSP-oriented instruction.

---

## 4. Aim and Objectives

### Aim

Design, simulate, and optimize a 5-stage pipelined RISC processor with a DSP instruction extension to accelerate MAC-intensive workloads.

### Objectives

1. Build/validate baseline 5-stage RISC datapath and control.
2. Ensure functional hazard detection and forwarding.
3. Add MAC instruction and MAC execution unit.
4. Integrate MAC support without changing pipeline depth.
5. Run DSP kernels in baseline and extended modes.
6. Measure instruction count, cycles, CPI, stalls, and runtime reduction.
7. Present results with tables/graphs and architectural analysis.

---

## 5. Scope and Non-Scope

### In Scope

1. RTL design in Verilog (or VHDL equivalent).
2. 5-stage pipeline: IF, ID, EX, MEM, WB.
3. Hazard handling for data/control hazards.
4. MAC instruction path in EX stage.
5. Software simulation, waveform analysis, and metrics.

### Out of Scope

1. ASIC physical design (floorplan, place and route).
2. FPGA timing closure and hardware deployment.
3. Out-of-order execution or superscalar extensions.
4. Floating-point DSP acceleration.

---

## 6. Recommended Toolchain

### Primary (Academic Standard)

1. HDL language: Verilog
2. Simulator: ModelSim or Vivado Simulator
3. Waveform viewer: ModelSim wave window or GTKWave
4. Scripting: Python 3.x (for result parsing and plotting)
5. Plots: matplotlib / spreadsheet charts
6. Documentation: Markdown + PDF report

### Open-Source Alternative Stack

1. Verilog simulation: Icarus Verilog (iverilog + vvp)
2. Waveforms: GTKWave
3. Synthesis check (optional): Yosys

---

## 7. High-Level Architecture

### Baseline Datapath

1. IF: fetch instruction from instruction memory.
2. ID: decode, register read, immediate generation.
3. EX: ALU operation / branch compare / address calculation.
4. MEM: data memory read/write.
5. WB: write result back to register file.

### New DSP Extension

1. Add MAC unit in EX stage.
2. Add select mux: ALU result vs MAC result.
3. Add ACC register (or architected destination register policy).
4. Add control signal `is_mac` from decoder.
5. Reuse existing forwarding and hazard framework with minimal updates.

---

## 8. Instruction Set Extension

### New Instruction

Example semantic form:

MAC rd, rs1, rs2

Meaning:

ACC <- ACC + (R[rs1] * R[rs2])
R[rd] <- ACC  (implementation choice: immediate writeback or separate read)

### Encoding Strategy

1. Reserve unused opcode/funct combination.
2. Decoder identifies MAC and drives `is_mac = 1`.
3. ALU control extended with operation `ALU_MAC`.

### Design Choice Note

You may choose one of two policies:

1. Dedicated hidden accumulator register (simpler for DSP loops).
2. Destination register as accumulator (more ISA explicit).

Pick one policy and keep it consistent in ISA doc and test programs.

---

## 9. Detailed Build Guide (End-to-Start)

## Phase 0: Setup

1. Create project folders:
   - rtl/
   - tb/
   - sim/
   - programs/
   - docs/
   - scripts/
2. Confirm simulator installation.
3. Define coding conventions and signal naming.

## Phase 1: Baseline Processor

1. Build modules:
   - pc.v
   - instr_mem.v
   - reg_file.v
   - alu.v
   - data_mem.v
   - control_unit.v
   - hazard_unit.v
   - forwarding_unit.v
   - pipeline registers (if_id, id_ex, ex_mem, mem_wb)
2. Integrate top module `risc5_top.v`.
3. Validate with arithmetic and load/store programs.

## Phase 2: Hazard and Forwarding Validation

1. Create directed tests for RAW hazards.
2. Confirm forwarding paths EX/MEM -> EX and MEM/WB -> EX.
3. Validate load-use stall behavior.
4. Validate branch flush behavior.

## Phase 3: DSP Extension Design

1. Define MAC opcode and control decode.
2. Implement `mac_unit.v`.
3. Add EX-stage mux and control path.
4. Add accumulator handling logic.
5. Update writeback selection logic if needed.

## Phase 4: Integrate MAC with Pipeline

1. Ensure MAC instruction fits normal pipeline travel.
2. Review hazard behavior when MAC writes destination.
3. Add forwarding source for MAC result if unique path exists.
4. Ensure no unintended structural hazards in EX stage.

## Phase 5: DSP Program Development

1. Create baseline (non-MAC) versions:
   - FIR tap accumulation loops
   - 1D convolution loops
2. Create MAC-optimized versions with equivalent outputs.
3. Keep test vectors deterministic.

## Phase 6: Simulation and Verification

1. Run all tests and log pass/fail.
2. Capture waveforms for key instructions.
3. Verify numerical output equivalence between baseline and MAC versions.

## Phase 7: Performance Measurement

1. For each workload record:
   - total instructions
   - total cycles
   - CPI = cycles / instructions
   - stall count
   - estimated execution time = cycles / clock_freq
2. Compare baseline vs DSP-extended.
3. Create improvement table and chart.

## Phase 8: Documentation and Viva Readiness

1. Prepare report and architecture diagrams.
2. Add timing/waveform snapshots.
3. Prepare concise result story and trade-off discussion.
4. Rehearse demo flow and viva Q&A.

---

## 10. Suggested Folder Structure

project_root/
- rtl/
- tb/
- sim/
- programs/
- docs/
- scripts/

Minimum files:

1. rtl/risc5_top.v
2. rtl/control_unit.v
3. rtl/alu.v
4. rtl/mac_unit.v
5. rtl/hazard_unit.v
6. rtl/forwarding_unit.v
7. tb/tb_risc5_top.v
8. programs/fir_baseline.mem
9. programs/fir_mac.mem
10. docs/report.pdf

---

## 11. MAC Unit RTL Blueprint (Conceptual)

Inputs:

1. clk, rst
2. enable_mac
3. src_a, src_b
4. acc_in

Output:

1. mac_out = acc_in + (src_a * src_b)

Notes:

1. Integer multiply is enough for the minor project.
2. Define overflow behavior clearly (wrap/saturate). Wrap is simpler.

---

## 12. Control Unit Updates

Add/extend control outputs:

1. is_mac
2. ex_result_sel (ALU or MAC)
3. wb_sel update if required

Decoder pseudocode:

if opcode == OPC_MAC:
- is_mac = 1
- reg_write = 1
- mem_read = 0
- mem_write = 0
- branch = 0
- alu_op = ALU_MAC

---

## 13. Hazard and Forwarding Impact

Expected behavior:

1. Existing RAW hazard logic continues to work if MAC writes to register file like other ALU ops.
2. Load-use hazards remain unchanged.
3. Branch hazards remain unchanged.
4. If ACC is dedicated hidden state, ensure dependencies are tracked or constrained by ISA usage.

Recommendation:

Use destination register accumulation policy first, then optional dedicated ACC as advanced version.

---

## 14. DSP Workloads to Implement

## Workload A: FIR Filter

Equation:

y[n] = sum(k=0 to M-1) h[k] * x[n-k]

Execution plan:

1. Baseline: MUL + ADD loop.
2. Extended: MAC loop.
3. Compare output and cycles.

## Workload B: 1D Convolution

Equation:

y[n] = sum(k) x[k] * h[n-k]

Execution plan:

1. Baseline nested loops.
2. MAC-enabled loops.
3. Compare metrics.

## Workload C: Dot Product

Equation:

dot = sum(i=0 to N-1) a[i] * b[i]

This is the cleanest benchmark for MAC impact.

---

## 15. Performance Metrics and Formulas

1. Instruction count reduction (%) = ((I_base - I_mac) / I_base) * 100
2. Cycle reduction (%) = ((C_base - C_mac) / C_base) * 100
3. Speedup = C_base / C_mac
4. CPI = cycles / instructions
5. Stall ratio = stalls / cycles

Expected trend:

1. Instruction count decreases significantly in MAC loops.
2. Cycles decrease proportionally, with minor differences due to hazards.
3. CPI may improve moderately.

---

## 16. Expected Results (Typical Academic Range)

Depending on code quality and memory behavior:

1. Instruction count reduction: 20% to 45%
2. Cycle reduction: 15% to 40%
3. Speedup: 1.2x to 1.7x
4. Stall count: same or slightly reduced (depends on scheduling)

Sample result template:

- FIR baseline: instructions=1200, cycles=1450, CPI=1.21
- FIR MAC: instructions=760, cycles=930, CPI=1.22
- Speedup = 1450/930 = 1.56x

---

## 17. Verification Strategy

1. Unit test each module: ALU, MAC, decoder, forwarding, hazard.
2. Integration test with short instruction sequences.
3. Randomized mini-program test (optional advanced).
4. Golden model comparison using Python script for DSP outputs.
5. Regression script to run all programs automatically.

Checklist:

1. Reset behavior correct
2. Pipeline flush/stall behavior correct
3. MAC arithmetic correctness
4. No incorrect writes on bubbles/flushes

---

## 18. Build and Run Commands (Examples)

## ModelSim (example flow)

1. vlib work
2. vlog rtl/*.v tb/tb_risc5_top.v
3. vsim -c tb_risc5_top -do "run -all; quit"

## Icarus Verilog (example flow)

1. iverilog -g2012 -o sim/risc_tb.out rtl/*.v tb/tb_risc5_top.v
2. vvp sim/risc_tb.out
3. gtkwave sim/wave.vcd

---

## 19. Timeline (8-Week Plan)

Week 1:
1. Finalize ISA subset and pipeline scope.
2. Setup simulator and repository structure.

Week 2:
1. Implement baseline datapath modules.
2. Basic arithmetic program verification.

Week 3:
1. Integrate hazard and forwarding units.
2. Validate RAW/load-use/branch scenarios.

Week 4:
1. Add MAC instruction encoding and decoder updates.
2. Implement MAC unit and EX-stage integration.

Week 5:
1. Develop DSP kernels baseline + MAC versions.
2. Functional correctness testing.

Week 6:
1. Performance measurement automation.
2. Collect cycles/CPI/stall data.

Week 7:
1. Prepare report figures and architecture diagrams.
2. Final regression and cleanup.

Week 8:
1. PPT + demo script + viva preparation.
2. Buffer for bug fixes.

---

## 20. Report Structure (College Submission)

1. Abstract
2. Introduction
3. Literature background (pipeline and DSP acceleration)
4. Baseline processor architecture
5. DSP extension design (MAC)
6. Implementation details (RTL modules)
7. Verification methodology
8. Results and performance analysis
9. Conclusion and future work
10. References
11. Appendix (test programs, waveforms)

---

## 21. PPT Structure (10-12 Slides)

1. Problem and motivation
2. Baseline 5-stage pipeline
3. Hazards and existing optimization
4. Why DSP extension
5. MAC instruction and datapath updates
6. Control and hazard compatibility
7. Test workloads
8. Performance comparison table/graph
9. Demo waveform/result snapshot
10. Conclusion and future scope

---

## 22. Viva Questions (High Probability)

1. Why 5-stage pipeline and not single-cycle design?
2. Difference between throughput and latency?
3. What is a RAW hazard and how did you solve it?
4. Why is forwarding better than only stalling?
5. What is branch penalty in your implementation?
6. Why MAC matters for DSP kernels?
7. How did you encode the MAC instruction?
8. Did MAC create new hazards?
9. How did you verify MAC correctness?
10. Why is simulation-only still valid academically?
11. How would you extend to fixed-point saturation?
12. What are power/area implications in real silicon?

---

## 23. Real-World Applications

1. Audio equalization and noise suppression
2. Speech enhancement pipelines
3. Biomedical signal processing (ECG/EEG)
4. Radar and communication filtering stages
5. Edge inference pre-processing (feature extraction)

This project demonstrates how domain-specific instruction support improves compute efficiency for these classes of workloads.

---

## 24. Risks and Mitigation

Risk: Wrong hazard behavior after MAC integration  
Mitigation: Directed hazard tests + wave-level debug

Risk: Instruction encoding conflicts  
Mitigation: Freeze ISA map early and document opcode table

Risk: Baseline and MAC outputs mismatch  
Mitigation: Golden reference script and deterministic vectors

Risk: Late report preparation  
Mitigation: Maintain running documentation weekly

---

## 25. Future Work

1. Add SIMD instruction support.
2. Add fixed-point saturation arithmetic.
3. Add hardware loop support for DSP kernels.
4. Explore dual-issue or deeper pipelining.
5. Move from simulation to FPGA prototype.

---

## 26. Final Outcome Statement

By completing this project, you can confidently present:

"We designed and optimized a 5-stage pipelined RISC processor, then extended it with a DSP-oriented MAC instruction in the EX stage. The extension reduced instruction count and execution cycles for signal-processing workloads while preserving pipeline compatibility with hazard detection and forwarding."

This is a strong and interview-relevant minor project for ECE students.

---

## 27. Submission Checklist

1. Clean RTL codebase with comments
2. Testbench and instruction memories
3. At least 3 DSP workloads (baseline and MAC)
4. Result tables and graphs
5. Waveform evidence
6. Final report PDF
7. PPT
8. Viva prep sheet

---

## 28. Quick Start Action Plan (Today)

1. Freeze ISA subset and MAC encoding.
2. Build baseline processor sanity tests.
3. Implement MAC datapath and decode signal.
4. Run dot-product benchmark first.
5. Measure cycles baseline vs MAC.
6. Expand to FIR/convolution.
7. Finalize documentation and presentation.

End of guide.
