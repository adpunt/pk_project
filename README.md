

[![OS Tests](https://github.com/adpunt/pk_project/actions/workflows/environment_testing.yml/badge.svg)](https://github.com/adpunt/pk_project)
[![codecov](https://codecov.io/gh/adpunt/pk_project/branch/master/graph/badge.svg?token=73FHW8GEAI)](https://codecov.io/gh/adpunt/pk_project)
[![BCH compliance](https://bettercodehub.com/edge/badge/adpunt/pk_project?branch=master)](https://bettercodehub.com/)
[![Documentation Status](https://readthedocs.org/projects/pk-project-apunt/badge/?version=latest)](https://pk-project-apunt.readthedocs.io/en/latest/?badge=latest)


# SABS-R<sup>3</sup> Pharmokinetics Modelling Project

This library provides users with the tools to specify, solve, and visualise the solution of a pharmacokinetic model.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#sample-code">Sample Code</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#troubleshooting">Problems</a></li>
  </ol>
</details>

  
<!-- ABOUT THE PROJECT -->
## About The Project

We can use Pharmacokinetic (PK) models to analyse how a drug passes through a patient's body. We consider the drug through all stages, from delivery to diffusion to clearance. The patient's body is modelled by compartments through which the drug in question passes. Such models can be used to both determine dosing and delivery protocols, and to educate people on the process of drug delivery. 

These models rely on a central component into which the drug is administered and from which the drug is excreted from the body. There may be zero or more peripheral compartments to which the drug can be distributed to/from the central compartment. 

We consider two types of dosing types, *intravenous bolus*, or *I.V.* dosing, and *subcontaneous* dosing. 

The user can adjust the central and peripheral components, as well as the dosing protocol, as needed to model different scenarios. 

In a simple case of *I.V.* dosing with a single peripheral compartment, we have a two-compartment model describing a drug going through a patient's body. The rate of change of the quantity of drug in the central compartment, $\frac{dq_c}{dt}$, is defined by 
$$\frac{dq_c}{dt} = Dose(t) -\frac{q_c}{V_c}CL -Q_{p} ( \frac{q_{p}}{V_{p}}-\frac{q_c}{V_c})$$

Where $Dose(t)$ [$X$ ng] is a function describing the inflow of drug into the patient's body.$-\frac{q_c}{V_c}CL$ represents the rate of  flow of drug out of the body, where $q_c$ [ng] is the drug quantity in the central compartment, $V_c$ [mL] is the volume of the central component, and $CL$ [mL/h] is the clearance rate of the drug out of the body. $-Q_{p} ( \frac{q_{p}}{V_{p}}-\frac{q_c}{V_c})$ represents the rate of the drug out of the central compartment and into the peripheral compartment, where $q_{p}$ [ng] is the quantity of the drug in the peripheral compartment and $V_p$ [mL] is the volume of the peripheral component. Unsurprisingly, the rate of change of the quantity of the drug in the peripheral component is 
$$Q_{p} ( \frac{q_{p}}{V_{p}}-\frac{q_c}{V_c})$$
When we're working with subcontinuous dosing protocols, we need an additional input. The subcontinous dosing adds an additional compartment to our model. This compartment is where the drug gets absorbed into the central compartment. Therefore, we need to specify an absorption rate into the central compartment, represented by $k_a$ [/h]. This absorption rate gets used to modify the following equations: 
$$\frac{dq_c}{dt} = k_aq_0 -\frac{q_c}{V_c}CL -Q_{p} ( \frac{q_{p}}{V_{p}}-\frac{q_c}{V_c})$$ and 
$$\frac{dq_0}{dt} = Dose(t) - k_aq_0$$
where $k_aq_0$ represents the gradual flow of drug into the central compartment and $q_0$ [ng] is the initial dose of drug.
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- INSTALLATION -->
## Installation



~~This package can be installed using pip. 
```pip install https://test.pypi.org/simple/<INSERT_NAME>```~~

This package can be cloned from this repository.
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage


Here is an example of how you would set up some models and solve them using various dosing protocols.

```python
import pkmodel as pk

# Define compartments
central = pk.Compartment(v_p=1, q_p=1) # note that for central compartments, transition_rate represents clearance rate
peripheral1 = pk.Compartment(v_p=1, q_p=0.5)
peripheral2 = pk.Compartment(v_p=1, q_p=2)
peripheral3 = pk.Compartment(volume1=

# Two-compartment i.v. dosing model
model1 = pk.Model(central_compartment=central, peripheral=[peripheral1])

# Three-compartment subcontinuous dosing model
model2 = pk.Model(central_compartment=central, peripheral=[peripheral1, peripheral2], k_a=1.0)

# Standard dosing protocol with default dosing function (single dose in beginning)
protocol1 = pk.Protocol(initial_dose=100, time=1)

# Standard dosing protocol with defined dosing function
test_fn = lambda t, y: 1 / (t + 2)
protocol2 = pk.Protocol(initial_dose=100, time=1, dose_func=test_fn)

# Solve and plot the PK models
sol1 = model1.solve(protocol1)
sol2 = model2.solve(protocol2)
```


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Adelaide Punt - adelaide.punt@dtc.ox.ac.uk
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- Problems -->
## Problems

I ran into a few problems along the way, and due to my illness and lack of time I was unable to solve all of them. 

I'm having issues replicating tests in Github Actions. I can run `unittests` and `pytest` perfectly well on my local device, but I seem to be running into issues using Github Actions. I suspect I don't have everything set up the way it should be, because the errors I get always seem to relate to missing packages. As a result, my continuous integration tests are failing. 

I was unable to get `poetry` to  install my package so I had to resort to instructing users to clone my repository from Github.

Finally, I was able to just fix a bug that was preventing me from graphing at the last minute. Unfortunately, this did not leave me with much time to make many interesting graphing features or update the `README` thoroughly. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>
