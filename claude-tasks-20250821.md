# Goals for Today 20250821

# Who You Are
You are a scientific software engineer emphasizing plant modeling. You are a stickler for testing and beautiful code. You prefer simple, straightforward abstracts, clear and well-cited code with a lot of comments.

# This project
Because this project is a major refactor and test build out. You prioritize testing against past implementations to ensure a perfect fit. You refer to 'experiments/202505_model_intercomparison' for how to run these intercomparisons and treat each one as a unique experiment.

After you make a change, you should create a new experiment folder in /experiment follow the naming example already in that folder. Your experiments should have a 'compare_models.py', a plots folder, a README.md, and a results directory.

# Issues
[1] Environment - take atmosphere out of environment
Environment is an interface class. It should not contain atmosphere or soil. These are external to the environment which immediately surrounds the plant.

Solution: Create a general abstract class named: component. Before doing this work, come up with a clear spec for how this ABC will work across 'plant', 'environment', 'atmosphere', 'soil', 'greenhouse'. We will only implement plant (template exists), enviroronment (exists), and atmosphere (exists), but want to be sure interfaces will generalize to soil and greenhouse.

## Questions for clarification:
1. **Component ABC Design**: Should the Component ABC include:
   - Common initialization interface (e.g., from parameters dict)?
   - State update methods (e.g., step/update with timestep)?
   - Data exchange interfaces (get/set variables)?
   - Serialization/deserialization for state saving?

2. **Environment-Atmosphere Separation**: Currently AbovegroundEnvironment receives exogenous_inputs that include atmospheric properties. After refactoring:
   - Should Environment only handle the immediate plant jacket (temperature, humidity at leaf surface)?
   - Should Atmosphere compute solar angles/radiation and pass to Environment?
   - How should data flow between Atmosphere → Environment → Plant?

3. **Testing Strategy**: 
   - Should each refactoring step have its own experiment folder (e.g., 202508_component_abc, 202508_environment_refactor)?
   - What level of difference is acceptable in intercomparison (0.0% or some tolerance)?

[2] Refactor / design / update unit tests
- Start by coming up with a clear plan about public v private interface. 
- Then build unit tests for each public interface.
Process:
1) Create a csv of all interfaces within MPM. Propose a unit test for each. Make sure it has a column that I will fill out as "public" or "private"    
2) We will fill out whether it is public or private
3) Then, we will come up with a unit test for each.

## Questions for clarification:
4. **CSV Format**: Should the CSV include:
   - Module/Class name
   - Method/Property name
   - Current visibility (leading underscore convention)
   - Proposed test description
   - Dependencies/mocking requirements?

5. **Testing Scope**: Should unit tests cover:
   - Only the minimum_plant_model package?
   - Include visualization and utils modules?
   - Test both forward compatibility (old names) and new interfaces?


[3] Refactor / design / update integration tests 

