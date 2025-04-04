classDiagram
    class ModelHandler {
        -drivers_filename: str
        -parameter_filename: str
        -resource_pool_filename: str
        -latitude: float
        -log_thermal_age: list
        -log_assimilation: list
        -log_lai: list
        -log_rp: list
        -log_rp_demand: list
        -log_rp_rgr: list
        -log_carbon_pool: list
        -log_resource_pool_sizes: dict
        +__init__(drivers_filename, parameter_filename, resource_pool_filename)
        +read_input_files()
        +plot_and_save_outputs()
        +save_data_to_csv(output_dir)
        +initialize_logs(plant_instance)
        +update_logs(plant_instance)
        +run_simulation()
    }
    
    class Atmosphere {
        -__rad: float
        -__lat: float
        -__doy: int
        -__hour: int
        -__atmospheric_properties_dict: dict
        +__init__(DOY, latitude, hour)
        +compute_atmospheric_properties()
        +get_atmospheric_properties()
    }
    
    class Environment {
        #exogenous_inputs: dict
        #interface_inputs: dict
        +__init__(exogenous_inputs)
    }
    
    class AbovegroundEnvironment {
        -__environmental_variables: dict
        +__init__(exogenous_inputs)
        +KDR_Coeff(Solar_Elev_Sin, Leaf_Blade_Angle)
        +KDF_Coeff(Leaf_Area_Index, Leaf_Blade_Angle, Scattering_Coeff)
        +REFLECTION_Coeff(Leaf_Scattering_Coeff, Direct_Beam_Ext_Coeff)
        +LIGHT_ABSORB(...)
        +compute_canopy_light_environment(Leaf_Blade_Angle, Leaf_Area_Index)
        +get_environmental_variables()
    }
    
    class CarbonAssimilation {
        -parameters: dict
        +__init__(parameters)
        +compute_Ci(Leaf_Temp, VPD)
        +photosynthesis(Leaf_Temp, Absorbed_PAR, VPD)
        +sunlit_shaded_photosynthesis(environmental_variables)
    }
    
    class Plant {
        -resource_pool_params: list
        -__thermal_age: float
        -__assimilation_sunlit: float
        -__assimilation_shaded: float
        -__Leaf_Area_Index: float
        -__carbon_pool: float
        -__parameters: dict
        -__thermal_age_increment: float
        -latitude: float
        -__resource_pools: list
        +__init__(params_dict, resource_pool_params)
        +create_resource_pools()
        +update_thermal_age(environmental_variables)
        +carry_out_photosynthesis(environmental_variables)
        +compute_carbon_assimilated(environmental_variables)
        +allocate_carbon(environmental_variables)
        +update_leaf_area_index()
        +simulate_plant(environmental_variables)
        +get_parameters()
        +get_assimilation_sunlit()
        +get_assimilation_shaded()
        +get_carbon_pool()
        +get_leaf_area_index()
        +get_thermal_age_increment()
        +get_thermal_age()
        +get_resource_pools()
    }
    
    class ResourcePool {
        +name: str
        +is_initiated: bool
        +thermal_time_initiation: float
        +allocation_priority: int
        +max_size: float
        +growth_rate: float
        +initial_size: float
        +current_size: float
        +RP_thermal_age: float
        +demand: float
        +rgr: float
        +__init__(name, thermal_time_initiation, allocation_priority, max_size, initial_size, growth_rate)
        +update_initiation_status(plant_thermal_age)
        +compute_relative_growth_rate(RP_thermal_age, max_size, initial_size, growth_rate)
        +compute_demand(plant_thermal_time, thermal_time_increment)
        +receive_carbon(allocated_carbon)
    }
    
    Environment <|-- AbovegroundEnvironment
    ModelHandler --> Plant : creates
    ModelHandler --> Atmosphere : creates
    ModelHandler --> AbovegroundEnvironment : creates
    Plant --> ResourcePool : contains
    Plant --> CarbonAssimilation : uses
    Plant --> AbovegroundEnvironment : interacts with
