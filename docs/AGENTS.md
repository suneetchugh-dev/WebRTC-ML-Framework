# Agent Guidelines (Research Project)

## Goal
Build and document a reproducible WebRTC multi-cause degradation classification framework. Prioritize scientific rigor, clarity, and minimalism.

## Rules
1. **Reproducibility First**: Use fixed seeds, log versions, document commands/parameters
2. **Controlled Experiments**: One impairment per run with clear labels
3. **Lightweight Models**: Prefer interpretable models (Random Forest) over heavy DL
4. **Data Integrity**: Validate getStats parsing and feature extraction
5. **Documentation**: Update docs alongside code changes
6. **Clean Structure**: Follow the established directory layout
7. **No Secrets**: Never commit credentials/tokens

## Workflow
- Read `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/PHASES.md` first
- Update `docs/DEV_SESSION_STATE.md` at end of session
- Keep code modular and testable
- Generate results in `results/` with clear names

## Coding Standards
- Python: PEP 8, type hints where helpful
- Functions small and focused
- Config via `src/utils/config.py`
- Use pathlib for paths
- Add docstrings for key functions
