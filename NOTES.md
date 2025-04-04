# Minimum Plant Model (MPM) Development Plan

## Current Issues

### Issue #1: Refactor code into python module
- Convert current flat script implementation into a proper Python package structure
- Target structure:
  ```
  mpm/
  ├── LICENSE
  ├── README.md
  ├── pyproject.toml
  ├── setup.py
  ├── setup.cfg
  ├── MANIFEST.in
  ├── .gitignore
  ├── docs/
  │   ├── conf.py
  │   ├── index.rst
  │   └── ...
  ├── mpm/
  │   ├── __init__.py
  │   ├── model_handler.py
  │   ├── plant.py
  │   ├── environment.py
  │   ├── atmosphere.py
  │   ├── resource_pool.py
  │   └── carbon_assimilation.py
  ├── tests/
  │   ├── __init__.py
  │   ├── test_model_handler.py
  │   ├── test_plant.py
  │   └── ...
  └── examples/
      ├── basic_simulation.py
      └── temperature_response.py
  ```

**Priority: HIGH**  
**Timeline: 2-3 weeks**  

#### Tasks:
1. Create initial package structure
2. Separate existing code into appropriate modules
3. Create `__init__.py` files with necessary imports
4. Set up packaging configuration (pyproject.toml, setup.py)
5. Write basic installation instructions
6. Create simple examples demonstrating usage

### Issue #2: Paper submission
- Prepare paper for scientific publication
- Link to draft: https://docs.google.com/document/d/1DLG_V2RcyrDHylOwcAgVX_8K0yg-51l8SAezRkkz0nM/edit

**Priority: HIGH**  
**Timeline: 1-2 months**  

#### Tasks:
1. Complete model validation against experimental data
2. Prepare figures showing model performance
3. Finalize model equations and descriptions
4. Write discussion section comparing to other models
5. Format paper according to target journal guidelines
6. Submit for internal review
7. Incorporate feedback and submit to journal

### Issue #3: Create object diagram
- Create comprehensive diagram showing class relationships and interactions

**Priority: MEDIUM**  
**Timeline: 1 week**  

#### Tasks:
1. Update existing UML diagram in Jupyter notebook
2. Create class relationship diagram showing inheritance and composition
3. Document data flow through the model
4. Add sequence diagram for key processes (photosynthesis, allocation)
5. Export diagrams in high-resolution format for paper

### Issue #4: Add readme
- Readme has been created but needs enhancements for publication
- Add badges and additional documentation

**Priority: MEDIUM**  
**Timeline: 1 week**  

#### Tasks:
1. Enhance existing README with badges once package is published
2. Add installation instructions for pip once package is available
3. Create more comprehensive examples
4. Add contributor guidelines
5. Include citation information for scientific users

## Additional Recommended Tasks

### Code Quality Improvements
- Add type hints throughout the codebase
- Implement proper docstrings in Google or NumPy format
- Add logging instead of print statements
- Create comprehensive test suite

### Feature Additions
- Add water limitation component
- Implement nitrogen dynamics
- Create visualization module for standard outputs
- Add sensitivity analysis tools

### Documentation
- Set up Read the Docs for comprehensive documentation
- Create tutorials for common use cases
- Add API documentation generated from docstrings

## Prioritized Timeline

### Phase 1 (1 month)
- Complete refactoring to Python module structure
- Enhance README with basic documentation
- Create initial object diagrams

### Phase 2 (2 months)
- Complete paper draft with finalized model validation
- Add core tests and type hints
- Set up basic CI/CD pipeline

### Phase 3 (3+ months)
- Submit paper to journal
- Publish package to PyPI
- Create comprehensive documentation
- Implement additional features (water, nitrogen)

## Regular Review Points
- Code reviews required for all PRs
- Monthly progress check on paper development
- Bi-weekly check-in on package structure and development