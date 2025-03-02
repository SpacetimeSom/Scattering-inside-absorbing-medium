# Scattering-inside-absorbing-medium
A Monte Carlo-based model to simulate light scattering by transparent nanoparticles inside an absorbing medium. The model takes the chemical and physical properties of scattering particles and medium as input and provides the relative absorption of power with respect to a system without the presence of scattering particles. 

## Features
- Implements Monte Carlo-based photon transport simulation
- Models scattering, absorption, and photon step sizes
- Uses anisotropic scattering with adjustable parameters
- Supports boundary interactions and Russian roulette weight termination

## Requirements
The script is written in Python and requires the following dependencies:

```bash
pip install numpy
```

## How It Works
1. Initializes photon packets with a defined weight and direction.
2. Simulates photon step sizes and scattering events.
3. Updates the photon’s position and weight after each scattering.
4. Tracks energy absorption at each step.
5. Uses the Russian roulette technique to terminate low-weight photons.
6. Computes the total absorbed energy after simulating all packets.

## Parameters
| Parameter  | Description |
|------------|-------------|
| `Us`       | Scattering coefficient of the medium |
| `g`        | Anisotropic scattering factor (ranges from -1 to 1) |
| `ua`       | Absorption coefficient of the medium |
| `Lx, Ly, Lz` | Dimensions of the medium |
| `itr`      | Number of photon packets to simulate |


## Usage
Run the script using:

```bash
python photon_inside_photoreactor.py
```

## Output
The script prints the normalized absorbed energy in the medium:

```bash
(Absorbed Energy) = (total absorption per photon) / (1 - exp(-ua))
```

## Author
- **Somendra Singh Jadon**
- **Kalpak Gupta**

## License
This project is open-source and available under the MIT License.
