# DCCN Viva Preparation Document - Labs 4-7

## Document: DCCN_Viva_QA_Labs4-7.pdf

### Overview
Comprehensive Q&A style viva preparation covering router configuration and routing protocols with deep cross-evaluation and conditional scenario analysis.

### Content Structure

#### Section 1: Conceptual Foundation Questions
- What is routing and why Layer 3 is essential
- Comparison: Static vs RIP vs OSPF with when/why to use each
- Conditional scenarios: Static routing network failures

#### Section 2: Router Configuration Fundamentals (Lab 4)
- Why `no shutdown` is critical
- DCE vs DTE clock rate differences
- When to configure VTY vs Console passwords

#### Section 3: Static Routing Deep Dive (Lab 5)
- Why static routing is impractical for large networks
- Default route concept: when useful, when dangerous
- Conditional scenarios: Multi-router connectivity issues
- Recursive lookup problems

#### Section 4: Distance-Vector Routing - RIP (Lab 6)
- How distance-vector algorithm works
- 15-hop limit reasoning
- RIPv1 vs RIPv2 comparison
- Convergence scenarios and troubleshooting
- Why full routing table sent every 30 seconds

#### Section 5: Link-State Routing - OSPF (Lab 7)
- Fundamental differences from RIP
- Router ID (RID) stability and configuration
- OSPF cost calculation (bandwidth-based)
- Areas and hierarchical design
- Designated Router (DR) and Backup DR election
- Hello/Dead interval matching requirements

#### Section 6: Cross-Lab Comparison & Advanced Scenarios
- RIP to OSPF migration strategy
- Hybrid static + dynamic routing approaches
- Multi-router path selection analysis

#### Section 7: Troubleshooting Across All Labs
- Interface status interpretation (up/up, up/down, down/down)
- Routing table issues and diagnostics
- Packets dropped despite routes existing
- Asymmetric routing problems

#### Section 8: Viva Quick Reference
- Key definitions with practical examples
- Exam strategy and common viva patterns
- Must-know distinctions

### Key Features

**Q&A Format:** 20+ conceptual questions with detailed answers

**If/But Scenarios:** Real-world conditional problems showing:
- What happens when configuration is wrong
- How to identify and fix issues
- Prevention strategies

**When/Why Analysis:** Explains:
- When to use each routing protocol
- Why certain design choices matter
- When protocols fail and alternatives

**Cross-Evaluation:** Compares all three routing approaches:
- Static routing vs Dynamic routing
- RIP vs OSPF characteristics
- Table-based comparisons with real metrics

### Coverage

| Lab | Topics |
|-----|--------|
| Lab 4 | Basic router config, interfaces, passwords, DCE/DTE |
| Lab 5 | Static routes, default routes, stub networks |
| Lab 6 | RIP distance-vector, convergence, hop count |
| Lab 7 | OSPF link-state, cost, areas, DR/BDR election |

### Document Properties
- **Pages:** 27
- **Format:** PDF (198 KB)
- **Style:** Professional with color-coded sections
- **Structure:** Table of Contents + Indexed Sections
- **Compilation:** Double-pass pdfLaTeX with hyperref

### How to Use for Viva

1. **Quick Review:** Read Key Definitions (Section 8)
2. **Concept Preparation:** Study Sections 1-5 for explanations
3. **Scenario Analysis:** Review If/But boxes for troubleshooting
4. **Cross-Evaluation:** Use Section 6 for comparative questions
5. **Final Checklist:** Reference viva strategy section before exam

### Best Practices Highlighted

✓ Always use loopback interface for stable OSPF Router ID
✓ Match Hello/Dead timers on both sides of OSPF links
✓ Configure classful network addresses for RIP
✓ Verify clock rate on DCE side of serial links
✓ Test bidirectional connectivity for asymmetric routing
✓ Use static routes for stub networks, OSPF for enterprise
✓ Check area IDs match for OSPF neighbor adjacency

---
*Generated: April 22, 2026*
*Course: CPE314 - Data Communication and Computer Networks*
