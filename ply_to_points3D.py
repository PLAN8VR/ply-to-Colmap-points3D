import numpy as np
from plyfile import PlyData
import struct

# --- CONFIG ---
PLY_FILE = "clean.ply"  # Your input PLY file

# --- Ask user for output type ---
print("Choose output format:")
print("1 = points3D.txt")
print("2 = points3D.bin")
choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    OUTPUT_TYPE = "txt"
    OUTPUT_FILE = "points3D.txt"
elif choice == "2":
    OUTPUT_TYPE = "bin"
    OUTPUT_FILE = "points3D.bin"
else:
    print("Invalid choice. Defaulting to TXT.")
    OUTPUT_TYPE = "txt"
    OUTPUT_FILE = "points3D.txt"

# --- Load PLY ---
ply = PlyData.read(PLY_FILE)
vertex = ply['vertex']

x = vertex['x']
y = vertex['y']
z = vertex['z']

if {'red', 'green', 'blue'}.issubset(vertex.data.dtype.names):
    r = vertex['red']
    g = vertex['green']
    b = vertex['blue']
else:
    r = np.full_like(x, 128)
    g = np.full_like(y, 128)
    b = np.full_like(z, 128)

# --- Write output ---
if OUTPUT_TYPE == "txt":
    with open(OUTPUT_FILE, 'w') as f:
        for i in range(len(x)):
            f.write(f"{i+1} {x[i]} {y[i]} {z[i]} {r[i]} {g[i]} {b[i]} 0.0\n")
    print(f"✅ Saved COLMAP TXT: {OUTPUT_FILE}")

elif OUTPUT_TYPE == "bin":
    with open(OUTPUT_FILE, 'wb') as f:
        for i in range(len(x)):
            f.write(struct.pack('<QdddBBBd', i+1, x[i], y[i], z[i], r[i], g[i], b[i], 0.0))
    print(f"✅ Saved COLMAP BIN: {OUTPUT_FILE}")

# --- Print summary ---
print(f"Total points converted: {len(x)}")
